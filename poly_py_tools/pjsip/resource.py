class SipResource:

    section = None
    section_name = None
    type = None

    # These are for testing only.
    attr1 = None
    attr2 = None

    def __init__(self, section):
        self.section = section
        self.section_name = None
        self.type = None

    def set_attributes(self):
        for line in self.section:
            if line is None:
                continue

            if "[" in line and "]" in line:
                start = str(line).find("[") + 1
                end = str(line).find("]")
                self.section_name = line[start:end]
                
            if not "=" in line:
                continue

            attribute, value = line.split("=")
            attribute = attribute.strip()
            value = value.strip()
            if not hasattr(self, attribute):
                raise ValueError("Cannot set attribute {} of class {}. Seems to not have that one.".format(attribute, self.__class__))

            setattr(self, attribute, value)

    def __str__(self):
        buffer = []
        for attr, value in self.__dict__.items():
            buffer.append("{}: {}".format(attr,value))
        return "\n".join(buffer)
