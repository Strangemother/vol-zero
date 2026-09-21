
def main():
    foo = Foo()
    result = foo.bar(b=2)
    print("result {}".format(result))


class Foo(object):

    def __init__(self):
        print('loaded Foo')

    def bar(self, a=1, b=4):
        return a + b
