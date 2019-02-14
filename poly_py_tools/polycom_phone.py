class PolycomPhone:

    registrations = None
    mac_address = None

    def __init__(self, mac_address):
        self.mac_address = mac_address
        self.registrations = []

    def add_registration(self, registration):
        self.registrations.add(registration)

    def sort_registrations(self):
        pass
