import inspect
from dataclasses import dataclass, field
import typing


@dataclass
class Func:
    name: str
    desc: str
    signature: inspect.Signature

    def __str__(self):
        return f"{self.name}{self.signature}\n\t{self.desc}"

    @property
    def icon(self):
        return "F"


@dataclass
class Class:
    name: str
    desc: str
    signature: inspect.Signature

    def __str__(self):
        return f"{self.name}{self.signature}\n\t{self.desc}"

    @property
    def icon(self):
        return "C"


@dataclass
class Datum:
    name: str
    desc: str
    value: typing.Any
    type_name: str

    def __str__(self):
        return f"{self.name} = {self.value} ({self.type_name})\n\t{self.desc}"

    @property
    def icon(self):
        return "G"


@dataclass
class Mod:
    name: str
    desc: str
    functions: list[Func] = field(default_factory=list)
    classes: list[Class] = field(default_factory=list)
    data: list[Datum] = field(default_factory=list)

    @property
    def icon(self):
        return "M"


def parse_function(func):
    try:
        signature = inspect.signature(func)
    except ValueError:
        signature = "..."
    return Func(name=func.__name__, desc=func.__doc__, signature=signature)


def parse_class(cls):
    try:
        signature = inspect.signature(cls)
    except ValueError:
        signature = "..."
    return Class(name=cls.__name__, desc=cls.__doc__, signature=signature)


def parse_module(mod):
    info = Mod(mod.__name__, mod.__doc__)

    for name, member in inspect.getmembers(mod):
        if inspect.isclass(member):
            info.classes.append(parse_class(member))
        elif inspect.isroutine(member):
            info.functions.append(parse_function(member))
        elif not name.startswith("__"):
            info.data.append(Datum(name, member.__doc__, member, type(member).__name__))

    return info


if __name__ == "__main__":
    import math

    parsed = parse_module(math)
    for f in parsed["functions"]:
        print(f)

    for d in parsed["data"]:
        print(d)
