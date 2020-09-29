

def run_readme_condition():
    import conditional_context

    print('start')
    value = True
    with conditional_context.condition(False):
        value = False
        print('here')  # Will not print
    print('end')

    assert value


def run_readme_class():
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


def run_readme_replace_decorator():
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


def run_readme_breakout():
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


if __name__ == '__main__':
    run_readme_condition()
    run_readme_class()
    run_readme_replace_decorator()
    run_readme_breakout()
