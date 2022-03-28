import io
import sys
import inspect


__all__ = ['ContextSkipError', 'breakout', 'ConditionalContext', 'condition', 'wrap']


class ContextSkipError(Exception):
    def __init__(self, msg='Skip context block'):
        super().__init__(msg)


# Module level function to break out of the body of a context without showing an error.
def breakout(*args, **kwargs):
    """Break out of the body of a ConditionalContext without showing an error."""
    raise ContextSkipError()


def _settrace(func):
    # Pydev actually writes to stderr instead of using a warning...
    stderr, sys.stderr = sys.stderr, io.StringIO()
    sys.settrace(func)
    sys.stderr = stderr


_required_attrs = [
    # Required for ConditionalContext to work.
    "_WARNING_IGNORED",
    "__init__",
    "__enter__",
    "__exit__",
    "should_skip",
    "replace_should_skip",
    "breakout",
    "should_run",
    "_context",
    "_orig_trace",
    "_skipped"
]


class ConditionalContext(object):
    """Context manager that can skip running the body of the context.

    Modify the `should_skip()` method to determine if the body of the context will be skipped.

    Args:
        should_run (bool)[True]: If True the body of the context will run. If False the body of context will not run.
        should_skip (callable/function)[None]: If given this will replace the should_skip method.
        context (class/context manager)[None]: If given, ConditionalContext will wrap this context.
    """
    _WARNING_IGNORED = False

    def __init__(self, should_run=True, should_skip=None, context=None):
        self.should_run = should_run
        self.replace_should_skip(should_skip)
        self._context = context
        self.breakout = breakout
        self._orig_trace = None
        self._skipped = False

    def should_skip(self):
        """Return if the body of the context should be skipped."""
        return not self.should_run

    def replace_should_skip(self, func):
        """Function decorator to replace the should_skip method."""
        if func is not None:
            self.should_skip = func
        return self.should_skip

    def __enter__(self):
        # Get return of wrapped __enter__, if we are wrapping.
        # We get this before skipping to avoid issues with tracebacks.
        if self._context is None:
            context_enter = self
        else:
            context_enter = self._context.__enter__()

        if self.should_skip():
            # Need to settrace to trigger the frame trace. Also need to reset trace after trace errors.
            self._orig_trace = sys.gettrace()
            if self._orig_trace is None:
                _settrace(lambda *args, **keys: None)

            # Set a stack trace that will raise an error to skip the context block.
            frame = inspect.currentframe().f_back
            frame.f_trace = self.breakout
            self._skipped = True

        return context_enter

    def __exit__(self, etype, value, traceback):
        # Reset the original trace method to resume debugging.
        if self._skipped:
            _settrace(self._orig_trace)
            self._orig_trace = None

        # Get return of wrapped __exit__, if we are wrapping.
        if self._context is None:
            context_exit = None
        else:
            context_exit = self._context.__exit__(etype, value, traceback)

        if etype == ContextSkipError:
            # Truthy return from __exit__ suppresses the error.
            return True
        else:
            # Otherwise we return the wrapped __exit__ result.
            return context_exit

    def __getattribute__(self, name):
        """Passthrough all other attributes from wrappped context."""
        # We can't just get self.context, will run into recursion.
        try:
            context = super().__getattribute__("_context")
        except AttributeError:
            context = None

        if context is None or name in _required_attrs:
            # Get actual attribute when not wrapping or when it is required.
            return super().__getattribute__(name)
        else:
            # Get attribute from context when wrapping and when it is not required.
            return context.__getattribute__(name)


def condition(should_run=True, should_skip=None):
    """Context manager that can skip running the body of the context.

    Args:
        should_run (bool)[True]: If True the body of the context will run. If False the body of context will not run.
        should_skip (callable/function)[None]: If given this will replace the should_skip method.

    Returns:
        ctx (ConditionalContext): Context manager class that can skip running the body of the context.
    """
    return ConditionalContext(should_run=should_run, should_skip=should_skip)


def wrap(context, should_run=True, should_skip=None):
    """Context manager that can skip running the body of the context.

    Args:
        context (class/context manager): The context to be wrapped in a ConditionalContext.
        should_run (bool)[True]: If True the body of the context will run. If False the body of context will not run.
        should_skip (callable/function)[None]: If given this will replace the should_skip method.

    Returns:
        ctx (ConditionalContext): Context manager class that can skip running the body of the context. Keeps the context functionality of wrapped context.
    """
    return ConditionalContext(should_run=should_run, should_skip=should_skip, context=context)
