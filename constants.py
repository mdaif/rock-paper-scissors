from collections import OrderedDict
from enum import Enum

from rules import VanillaRPSRules, RockPaperScissorsLizardSpockRules

SUPPORTED_GAME_FLAVORS = OrderedDict(
    {
        'vanilla': (
            VanillaRPSRules,
            """Vanilla Rock-Paper-Scissors:
                Scissors cuts Paper
                Paper covers Rock
                Rock crushes Scissors.
            """,
        ),
        'rpsls': (
            RockPaperScissorsLizardSpockRules,
            """Rock-Paper-Scissors-Lizard-Spock:
                Scissors cuts Paper
                Paper covers Rock
                Rock crushes Lizard
                Lizard poisons Spock
                Spock smashes Scissors
                Scissors decapitates Lizard
                Lizard eats Paper
                Paper disproves Spock
                Spock vaporizes Rock
                (and as it always has) Rock crushes Scissors
            """

        ),
    },
)

EXIT_WORD = 'STOP'


class Winner(Enum):
    USER = 0
    COMPUTER = 1
    DRAW = 2
