from dataclasses import dataclass


@dataclass
class ContinuationMonadOperatorException(Exception):
    message: str
