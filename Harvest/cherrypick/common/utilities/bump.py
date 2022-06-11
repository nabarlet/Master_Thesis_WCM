import sys,os
import atexit 

class Bump:
    class __Bump__:
        def __init__(self):
            self.fh = None
            self.counter = 0
            self.setup()

        def setup(self):
            if not self.fh:
                #
                # NOTE: this is guaranteed to work only on GNU Linux, on other
                # operating systems YMMV
                #
                self.fh = open('/proc/self/fd/6', 'w') # open a third file descriptor for writing
            atexit.register(self.fh.close)

        __COUNTER_RATE__ = 10
        def bump(self, ch = '.'):
            to_print = ch
            if self.counter != 0 and (self.counter % Bump.__Bump__.__COUNTER_RATE__) == 0:
                to_print = str(self.counter)
            print(to_print, end='', file=self.fh)
            self.counter += 1
            self.fh.flush()

    instance = None

    def __new__(cls):
        if not Bump.instance:
            Bump.instance = Bump.__Bump__()
        return Bump.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
