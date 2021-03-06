import io
import sys
import inspect


__all__ = ['ContextSkipError', 'ConditionalContext', 'condition', 'breakout']


class ContextSkipError(Exception):
    def __init__(self, msg='Skip context block'):
        super().__init__(msg)


class ConditionalContext(object):
    """Context manager that can skip running the body of the context.

    Modify the `should_skip()` method to determine if the body of the context will be skipped.

    Args:
        should_run (bool)[True]: If True the body of the context will run. If False the body of context will not run.
        should_skip (callable/function)[None]: If given this will replace the should_skip method.
    """
    _WARNING_IGNORED = False

    def __init__(self, should_run=True, should_skip=None):
        self.should_run = should_run
        self._orig_trace = None
        self.skipped = False
        if should_skip is not None:
            self.replace_should_skip(should_skip)

    def should_skip(self):
        """Return if the body of the context should be skipped."""
        return not self.should_run

    orig_should_skip = should_skip

    def replace_should_skip(self, func):
        """Function decorator to replace the should skip method."""
        if func is None:
            func = self.orig_should_skip
        self.should_skip = func
        return func

    @staticmethod
    def breakout(*args, **kwargs):
        """Break out of the body of a ConditionalContext without showing an error."""
        raise ContextSkipError()

    trace = breakout

    @staticmethod
    def settrace(func):
        # Pydev actually writes to stderr instead of using a warning...
        stderr, sys.stderr = sys.stderr, io.StringIO()
        sys.settrace(func)
        sys.stderr = stderr

    def __enter__(self):
        self.skipped = self.should_skip()
        if self.skipped:
            # Need to settrace to trigger the frame trace. Also need to reset trace after trace errors.
            self._orig_trace = sys.gettrace()
            if self._orig_trace is None:
                self.settrace(lambda *args, **keys: None)  # Note: custom "self."settrace

            # Set a stack trace that will raise an error to skip the context block
            frame = inspect.currentframe().f_back
            frame.f_trace = self.breakout
        return self

    def __exit__(self, etype, value, traceback):
        # Reset the original trace method to resume debugging
        if self.skipped:
            self.settrace(self._orig_trace)
            self._orig_trace = None
        return etype == ContextSkipError or etype is None


def condition(should_run=True, should_skip=None):
    """Context manager that can skip running the body of the context.

    Args:
        should_run (bool)[True]: If True the body of the context will run. If False the body of context will not run.
        should_skip (callable/function)[None]: If given this will replace the should_skip method.

    Returns:
        ctx (ConditionalContext): Context manager class that can skip running the body of the context.
    """
    return ConditionalContext(should_run, should_skip)


# Module level function to break out of the body of a context without showing an error
breakout = ConditionalContext.breakout
