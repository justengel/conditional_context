

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


if __name__ == '__main__':
    run_readme_condition()
    run_readme_class()
