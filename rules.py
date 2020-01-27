from abc import ABCMeta
from enum import Enum


class Symbols(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    # Extended
    LIZARD = 3
    SPOCK = 4


class BaseRPSRules(metaclass=ABCMeta):
    """Base class for all Flavors"""
    _defeats = None

    @property
    def defeats(self):
        return self._defeats

    def get_winner(self, first, second):
        assert first != second

        if second in self.defeats[first]:
            return first
        return second


class VanillaRPSRules(BaseRPSRules):
    _defeats = {
        Symbols.ROCK: {Symbols.SCISSORS},
        Symbols.PAPER: {Symbols.ROCK},
        Symbols.SCISSORS: {Symbols.PAPER},
    }


class RockPaperScissorsLizardSpockRules(BaseRPSRules):
    _defeats = {
        Symbols.ROCK: {Symbols.SCISSORS, Symbols.LIZARD},
        Symbols.LIZARD: {Symbols.PAPER, Symbols.SPOCK},
        Symbols.SPOCK: {Symbols.SCISSORS, Symbols.ROCK},
        Symbols.SCISSORS: {Symbols.LIZARD, Symbols.PAPER},
        Symbols.PAPER: {Symbols.SPOCK, Symbols.ROCK},
    }
