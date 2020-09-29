===================
conditional_context
===================

Context manager that will skip the body on a condition.

All code is in `conditional_context/__init__.py`

Examples
========

Condition function example

.. code-block:: python

    from conditional_context import condition

    print('start')
    value = True
    with condition(False):
        value = False
        print('here')  # Will not print
    print('end')

    assert value


Custom class replacing the `should_skip` method example

.. code-block:: python

    import conditional_context

    class MyContext(conditional_context.ConditionalContext):
        def should_skip(self):
            return True

    print('start')
    value = True
    with MyContext():
        value = False
        print('here')  # Will not print
    print('end')

    assert value

Replace the `should_skip` method with a decorator

.. code-block:: python

    import conditional_context

    ctx = conditional_context.ConditionalContext()

    @ctx.replace_should_skip
    def my_should_skip():
        return True

    print('start')
    value = True
    with ctx:
        value = False
        print('here')  # Will not print
    print('end')

    assert value, 'ConditionalContext class did not skip properly'

Breakout function to stop running the context without showing an error.

.. code-block:: python

    from conditional_context import condition

    value1 = True
    value2 = True
    value3 = True
    with condition() as ctx:
        value1 = False
        value2 = False
        ctx.breakout()  # Should raise an error to break out of the context.
        value3 = False

    assert value1 is False
    assert value2 is False
    assert value3 is True, 'The breakout feature did not work as expected!'
