import sys,os
import atexit 

class Bump:
    class __Bump__:
        def __init__(self):
            self.fh = None
            self.counter = 0
            self.setup()

        __PROGRESS_FILE_PATH__ = './progress.txt'
        def setup(self):
            """
                setup()

                this opens a './progress.txt' file in append mode wherever the script happens
                to be launched. If it fails, then redirects the output to
                standard error.
            """
            if not self.fh:
                try:
                    self.fh = open(Bump.__Bump__.__PROGRESS_FILE_PATH__, 'a')
                except FileNotFoundError:
                    self.fh = sys.stderr
            atexit.register(self.fh.close)

        __COUNTER_RATE__ = 50
        def bump(self, ch = '.'):
            to_print = ch
            if self.counter != 0 and (self.counter % Bump.__Bump__.__COUNTER_RATE__) == 0:
                to_print = ' ' + str(self.counter) + ' '
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
