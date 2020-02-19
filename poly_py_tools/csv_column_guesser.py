import csv
import json


class ColumnGuesser:
    verbosity = 0
    first = None
    last = None
    exten = None
    vm = None
    mac = None
    email = None
    device = None
    cid_number = None
    startrow = None
    priority = None
    label = None
    save = False
    column_letters = []
    base_map = '{"first":"","last":"","exten":"","vm":"","mac":"","email":"","cid_number":"","device":"","label":"","priority":""}'

    guessing_dictionary = None

    def __init__(self, guessing_dictionary):
        self.guessing_dictionary = guessing_dictionary
        self.column_letters = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()

    def set_verbosity(self, verbosity):
        self.verbosity = verbosity

    def log(self, message, required_verbosity=1):
        if self.verbosity >= required_verbosity:
            print(message)

    def score_header_row(self, row):
        score = 0
        for key in self.guessing_dictionary:
            for item in self.guessing_dictionary[key]:
                if item in row:
                    score = score + 1
        return score

    def guess_columns(self, csv_file):
        guess_success = True
        map = json.loads(self.base_map)
        column_counter = -1
        with open(csv_file) as csv_file:
            csv_reader = csv.reader(csv_file)
            header_row = next(csv_reader)
            for column in header_row:
                column_counter = column_counter + 1
                if len(column) == 0:
                    continue
                for dict in self.guessing_dictionary:
                    for value in self.guessing_dictionary[dict]:
                        self.log("Analyzing column: {}. Trying to match {} with {}".format(column, dict, value), 10)
                        if column.lower().strip() == value.lower().strip():
                            self.log("MATCHED!", 10)
                            if map[dict] != "":
                                print("Was trying to match [{}], but I have already matched it. I think this column is "
                                      "duplicated, which will cause issues. Check the CSV file, and re-run me.".format(value))
                                print(map)
                                exit(1)

                            map[dict] = column_counter

        for k in map:
            if map[k] == "":
                guess_success = False
                print("Could not guess which column is used for: {}".format(k))

        if not guess_success:
            print("\nCould not guess all the columns. Column map not created.")
            print("Either update the dictionary, or re-name the columns to comply with the column guesser.")

        if not self.save:
            print("I have found the following columns. Re-run the command with the --save option to write the map.")
            for k in map:
                # print("{} => {} [{}]".format(k, map[k]), self.column_letters[map[k]])
                print("{} => Column {} ({})".format(k, self.column_letters[map[k]], map[k]))

        if self.save:
            if self.startrow is None:
                print("You must specify a start row with --startrow=<rownumber> in order to save this map.")
                exit(1)

            map['startrow'] = self.startrow
            f = open('csv_columns.map', 'w')
            f.write(json.dumps(map))
            f.close()
            print("Map saved to csv_columns.map.")

    def __str__(self):
        buffer = []
        buffer.append("first: {}".format(self.first))
        buffer.append("last: {}".format(self.last))
        buffer.append("exten: {}".format(self.exten))
        buffer.append("vm: {}".format(self.vm))
        buffer.append("mac: {}".format(self.mac))
        buffer.append("email: {}".format(self.email))
        buffer.append("device: {}".format(self.device))
        buffer.append("cid_number: {}".format(self.cid_number))
        buffer.append("startrow: {}".format(self.startrow))
        buffer.append("priority: {}".format(self.priority))
        buffer.append("label: {}".format(self.label))
        buffer.append("")
        buffer.append("<Guessing Dictionary>")
        for key in self.guessing_dictionary:
            buffer.append("  -{} : {}".format(key,",".join(self.guessing_dictionary[key])))
        buffer.append("</Guessing Dictionary>")

        return "\n".join(buffer)