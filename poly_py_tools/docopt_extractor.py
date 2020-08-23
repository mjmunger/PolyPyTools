import os

class DocoptExtractor():
    lib_path = None

    def __init__(self, lib_path):
        self.lib_path = lib_path

    def docopt(self, file_under_test):
        target_file = os.path.join(self.lib_path, file_under_test)
        f = open(target_file, 'r')
        buffer = f.read()
        f.close()

        buffer = buffer.split("\n")

        output = []
        in_docopt = False

        for line in buffer:
            if line.lower().startswith('"""'):
                in_docopt = not in_docopt
                continue #skip the first line.

            if in_docopt:
                output.append(line)

        return "\n".join(output)
