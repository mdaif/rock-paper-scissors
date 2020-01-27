import logging
from random import choice

from components import UserChoice, ResultHandler
from constants import Winner
from rules import BaseRPSRules, Symbols

log = logging.getLogger(__name__)


class Engine:
    def __init__(
            self,
            rounds: int,
            game_rules: BaseRPSRules,
            user_choice: UserChoice,
            result_handler: ResultHandler,
    ):
        log.debug(
            'Initializing engine for %d rounds and %s game',
            rounds, game_rules.__class__.__name__)

        self.defeating_rules = game_rules
        self.rounds = rounds
        self.valid_choices = set(
            choice.name.lower() for choice in self.defeating_rules.defeats)
        self.user_choice = user_choice
        self.result_handler = result_handler

    def play_one_round(self):
        user_choice = self.user_choice.get(self.valid_choices)

        computer_choice = choice(list(self.valid_choices))

        log.info('Computer choice: %s', computer_choice)

        user_choice = Symbols[user_choice.upper()]
        computer_choice = Symbols[computer_choice.upper()]

        if user_choice == computer_choice:
            log.info('DRAW ! Another round ... ')
            return Winner.DRAW, user_choice, computer_choice

        winner = self.defeating_rules.get_winner(
            user_choice, computer_choice)

        if winner == user_choice:
            log.info('User won')
            return Winner.USER, user_choice, computer_choice
        else:
            log.info('Computer won')
            return Winner.COMPUTER, user_choice, computer_choice

    def play_n_rounds(self, rounds):
        count = 0
        while count < rounds:
            winner, user_choice, computer_choice = self.play_one_round()
            if winner == Winner.DRAW:
                self.result_handler.send(winner, user_choice, computer_choice)
                continue
            self.result_handler.send(winner, user_choice, computer_choice)
            count += 1
