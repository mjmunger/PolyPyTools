class PolycomPhone:

    registrations = None
    mac_address = None
    type = None
    verbosity = 0

    def __init__(self, mac_address):
        self.mac_address = mac_address
        self.registrations = []
        self.type = "Polycom"

    def set_verbostiy(self, verbosity):
        self.verbosity = verbosity

    def add_registration(self, registration):
        self.registrations.add(registration)

    def log(self, message, minimum_level=1):
        if self.verbosity < minimum_level:
            return True

        print("%s" % message)

    def set_verbosity(self, level):
        self.verbosity = level
        self.log("Verbosity set to: %s" % level)

    def sort_registrations(self):
        buffer = []
        unordered = []

        reg_count = len(self.registrations)

        self.log("Sorting %s registrations." % reg_count, 3)

        for registration in self.registrations:
            if registration.order is None:
                unordered.append(registration)

        self.log("%s unordered registrations." % len(unordered), 3)

        for index in range(0, reg_count+1):
            for registration in self.registrations:
                self.log("Registration %s is set to order %s" % (registration.name, registration.order), 2)
                if int(registration.order) == index:
                    buffer.append(registration)
                    self.log("Sorted registration: %s to index %i" % (registration.name, index), 3)

        index = len(self.registrations)

        for registration in unordered:
            registration.order = index
            buffer.append(registration)
            index = index + 1

        self.registrations = buffer

        if self.verbosity > 3:
            print("Final registration order:")
            index = 0
            for reg in self.registrations:
                index = index + 1
                print("%i. (%s)%s" % (index, reg.label, reg.name))

    def __str__(self):
        print("Mac: %s" % self.mac_address)
