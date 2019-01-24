import re


class PasswordStrengthCalculator:

    verbosity = 0
    password = None
    search_space_depth = 0
    search_space_length = 0
    search_space_size = 0
    n = 1
    m = 0
    search_space_e_size = None

    def __init__(self, password):
        self.password = password

    def evaluate(self):
        self.calculate_search_space_depth()
        self.calculate_search_space_length()

        search_space_size = 0
        for i in range(self.search_space_length, 0, -1):
            self.search_space_size = self.search_space_size + pow(self.search_space_depth, i)

        self.computer_power_of_ten()

        if self.verbosity > 0:
            print("Search space depth: %s " % self.search_space_depth)
            print("Search space length: %s " % self.search_space_length)
            print("Search space size: %s " % self.search_space_size)
            print("Search space size (e): %s " % self.search_space_e_size)

        return self.cracking_improbable()

    def cracking_improbable(self):
        speed = 100000000000000
        seconds = self.search_space_size / 2 / speed
        if self.verbosity > 0:
            if self.verbosity > 3:
                print("Analysis for: %s" % self.password)
            print("Time to crack (in seconds) %s" % seconds)
            print("Time to crack (in minutes) %s" % (seconds / 60))
            print("Time to crack (in hours) %s" % (seconds / 60**2))
            print("Time to crack (in days) %s" % (seconds / ((60**2) * 24 )))
            print("Time to crack (in weeks) %s" % (seconds / ((60**2) * 24 * 7)))
            print("Time to crack (in years) %s" % (seconds / ((60**2) * 24 * 7 * 365)))

        return True if (seconds / ((60**2) * 24 * 7 * 365)) > 100 else False

    def computer_power_of_ten(self):
        big_number = float(self.search_space_size)
        string_number = str(big_number).split('e')
        if "e" not in string_number:
            self.search_space_e_size = self.search_space_size
            return True

        self.n = string_number[1][1:]
        self.m = round(float(string_number[0]), 3)

        self.search_space_e_size = "%s x 10^%s" % (self.m, self.n)

    def calculate_search_space_depth(self):
        self.search_space_depth = 0

        # Check if contains at least one digit
        if re.search(r'\d', self.password):
            self.search_space_depth = self.search_space_depth + 10

        # Check if contains at least one uppercase letter
        if re.search(r'[A-Z]', self.password):
            self.search_space_depth = self.search_space_depth + 26

        # Check if contains at least one lowercase letter
        if re.search(r'[a-z]', self.password):
            self.search_space_depth = self.search_space_depth + 26

        if re.search(r'[-!$%^&*()_+|~=`{}\[\]:";\'<>?,.\\/]', self.password):
            self.search_space_depth = self.search_space_depth + 33

    def calculate_search_space_length(self):
        self.search_space_length = len(self.password)


