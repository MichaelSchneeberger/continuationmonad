from abc import abstractmethod

from donotation import do

import continuationmonad
from continuationmonad.typing import ContinuationMonad


# define abstract operations implemented by an interpreter
class IOOperations:
    @abstractmethod
    def readln(self, prompt: str) -> ContinuationMonad[str]: ...

    @abstractmethod
    def println(self, line: str) -> ContinuationMonad[None]: ...


# define the program that is executed by an interpreter
@do()
def program_(op: IOOperations):
    name = yield op.readln("What is your name? ")
    age = yield op.readln("What is your age? ")
    return op.println(f"Your name is {name} and you are {age} years old!")


# define an interpreter that perform IO actions
class IOOperationsInterpreter(IOOperations):
    def readln(self, prompt: str):
        return continuationmonad.from_(prompt).map(lambda msg: input(msg))

    def println(self, line: str):
        def fn(msg):
            print(msg)
            return msg

        return continuationmonad.from_(line).map(fn)


interpreter = IOOperationsInterpreter()

# run the program with the IO interpreter
continuationmonad.run(program_(interpreter))
