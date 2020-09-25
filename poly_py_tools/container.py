import hashlib
import importlib


class Container:

    dict = {}
    constructors = {}

    def __init__(self):
        self.dict = {}
        self.constructors = {}

    def add(self, library : str, classname: str, constructor_args=None) -> None:
        classlist = [library, classname]
        m = hashlib.md5()
        m.update(".".join(classlist).encode("ascii"))
        m.digest()
        self.dict[m.hexdigest()] = classlist
        self.constructors[m.hexdigest()] = constructor_args

    def get(self, classname):
        for key, classlist in self.dict.items():
            if classname in classlist:
                lib = classlist[0]
                target_class = classlist[1]
                constructor_args = self.constructors[key]
                return_class = getattr(importlib.import_module(lib), target_class)
                if constructor_args is None:
                    return return_class()
                else:
                    return return_class(constructor_args)
