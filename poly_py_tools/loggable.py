class Loggable:

    debug_mode = None
    verbosity = None
    message = None

    def __init__(self):
        self.debug_mode = False
        self.verbosity = 0
        self.message = ""

    def set_debug(self):
        self.debug_mode = True
        self.verbosity = 10

    def set_verbosity(self, verbosity):
        self.verbosity = verbosity

    def log(self, message, required_verbosity = 1):
        if self.verbosity >= required_verbosity:
            print(message)