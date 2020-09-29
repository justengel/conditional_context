===================
conditional_context
===================

Context manager that will skip the body on a condition.

All code is in `conditional_context/__init__.py`

.. code-block:: python

    from conditional_context import condition

    print('start')
    value = True
    with condition(False):
        value = False
        print('here')  # Will not print
    print('end')

    assert value


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
