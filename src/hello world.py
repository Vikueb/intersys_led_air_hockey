class main:

    s = ''

    def __init__(self):
        s = 'hello world'

    def hello(self) :
        print('hello world!')

    pass


m = main
m.__init__(m)
m.hello(m)