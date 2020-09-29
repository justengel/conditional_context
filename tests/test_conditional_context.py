

def test_condition():
    import conditional_context

    print('start')
    value = True
    with conditional_context.condition(False):
        value = False
        print('here')  # Will not print
    print('end')

    assert value, 'The condition function did not skip properly'


def test_conditional_context_class():
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

    assert value, 'ConditionalContext class did not skip properly'


if __name__ == '__main__':
    test_condition()
    test_conditional_context_class()
