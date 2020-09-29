import sys
import inspect


__all__ = ['ContextSkipError', 'ConditionalContext', 'condition']


class ContextSkipError(Exception):
    @classmethod
    def trace(cls, frame, event, arg):
        raise cls('Skip context block')


class ConditionalContext(object):
    """Context manager that can skip running the body of the context.

    Modify the `should_skip()` method to determine if the body of the context will be skipped.

    Args:
        should_run (bool)[True]: If True the body of the context will run. If False the body of context will not run.
    """
    def __init__(self, should_run=True):
        self.should_run = should_run

    def should_skip(self):
        """Return if the body of the context should be skipped."""
        return not self.should_run

    def __enter__(self):
        if self.should_skip():
            # Set a stack trace that will raise an error to skip the context block
            sys.settrace(lambda *args, **keys: None)
            frame = inspect.currentframe()
            frame = frame.f_back  # frame = inspect.currentframe(1)
            frame.f_trace = ContextSkipError.trace

    def __exit__(self, type, value, traceback):
        return type == ContextSkipError or type is None


def condition(should_run=True):
    """Context manager that can skip running the body of the context.

    Args:
        should_run (bool)[True]: If True the body of the context will run. If False the body of context will not run.

    Returns:
        ctx (ConditionalContext): Context manager class that can skip running the body of the context.
    """
    return ConditionalContext(should_run)
