import unittest
from io import StringIO
from unittest import mock

from components import ConsoleResultHandler, ConsoleUserChoice
from constants import Winner, EXIT_WORD
from engine import Engine
from rules import VanillaRPSRules, Symbols


class RulesTest(unittest.TestCase):
    def test_vanilla_rps_rules_different_symbols(self):
        vanilla_rps_rules = VanillaRPSRules()
        expected_results = [
            (Symbols.ROCK, Symbols.PAPER, Symbols.PAPER),
            (Symbols.ROCK, Symbols.SCISSORS, Symbols.ROCK),
            (Symbols.PAPER, Symbols.SCISSORS, Symbols.SCISSORS),
        ]
        for first, second, winner in expected_results:
            self.assertEqual(
                vanilla_rps_rules.get_winner(first, second), winner)

    def test_vanilla_rps_rules_same_symbol(self):
        symbols = [Symbols.ROCK, Symbols.PAPER, Symbols.PAPER]

        vanilla_rps_rules = VanillaRPSRules()
        for symbol in symbols:
            with self.assertRaises(AssertionError):
                vanilla_rps_rules.get_winner(symbol, symbol)


class ComponentsTest(unittest.TestCase):

    def test_console_result_handler(self):
        handler = ConsoleResultHandler()
        inputs = [
            Winner.DRAW, Winner.USER, Winner.COMPUTER,
        ]

        for inp in inputs:
            with mock.patch('sys.stdout', new=StringIO()) as m_stdout:
                handler.send(inp, mock.Mock(), mock.Mock())
            value = m_stdout.getvalue().strip()
            self.assertNotEqual(value, '')

    @mock.patch('components.print')
    @mock.patch('components.input')
    def test_console_user_choice_selection(self, m_input, m_print):
        m_input.side_effect = [
            'invalid1',
            'invalid2',
            'rock',
        ]
        user_choice = ConsoleUserChoice()
        choice = user_choice.get(valid_choices={'rock'})

        # Two invalid choices means two error messages
        self.assertEqual(m_print.call_count, 2)
        self.assertEqual(choice, 'rock')

    @mock.patch('components.input')
    def test_console_user_quits(self, m_input):
        m_input.return_value = EXIT_WORD
        user_choice = ConsoleUserChoice()

        with self.assertRaises(SystemExit):
            user_choice.get(valid_choices={'rock'})


class EngineTest(unittest.TestCase):

    @mock.patch('engine.choice')
    def _play_and_assert_one_round(
            self, m_choice, user_choice, computer_choice, expected_winner,
            expected_user_choice, expected_computer_choice,
            round_winner=None):
        m_choice.return_value = computer_choice

        game_rules = mock.Mock(
            defeats={}, get_winner=mock.Mock(return_value=round_winner))

        user_choice = mock.Mock(get=mock.Mock(return_value=user_choice))
        engine = Engine(
            1, game_rules, user_choice, result_handler=mock.Mock())
        winner, user_choice, computer_choice = engine.play_one_round()
        self.assertEqual(winner, expected_winner)
        self.assertEqual(user_choice, expected_user_choice)
        self.assertEqual(computer_choice, expected_computer_choice)

    def test_play_one_round_draw(self):
        self._play_and_assert_one_round(
            user_choice='rock', computer_choice='rock',
            expected_winner=Winner.DRAW, expected_user_choice=Symbols.ROCK,
            expected_computer_choice=Symbols.ROCK,
        )

    def test_play_one_round_user_wins(self):
        self._play_and_assert_one_round(
            user_choice='rock', computer_choice='scissors',
            expected_winner=Winner.USER, expected_user_choice=Symbols.ROCK,
            expected_computer_choice=Symbols.SCISSORS,
            round_winner=Symbols.ROCK,
        )

    def test_play_one_round_computer_wins(self):
        self._play_and_assert_one_round(
            user_choice='paper', computer_choice='scissors',
            expected_winner=Winner.COMPUTER,
            expected_user_choice=Symbols.PAPER,
            expected_computer_choice=Symbols.SCISSORS,
            round_winner=Symbols.SCISSORS,
        )

    @mock.patch.object(Engine, 'play_one_round')
    def test_n_rounds(self, m_play_one_round):
        # We play two rounds but since two of them ended up in a draw
        # we keep playing until we have two winners.
        m_play_one_round.side_effect = [
            (Winner.DRAW, Symbols.ROCK, Symbols.ROCK),
            (Winner.USER, Symbols.ROCK, Symbols.SCISSORS),
            (Winner.DRAW, Symbols.SCISSORS, Symbols.SCISSORS),
            (Winner.COMPUTER, Symbols.PAPER, Symbols.ROCK),
        ]
        m_send = mock.Mock()
        m_result_handler = mock.Mock(send=m_send)
        engine = Engine(
            1, mock.Mock(defeats={}), mock.Mock(),
            result_handler=m_result_handler)

        engine.play_n_rounds(2)
        actual_calls = m_send.call_args_list
        expected_calls = [
            mock.call(Winner.DRAW, Symbols.ROCK, Symbols.ROCK),
            mock.call(Winner.USER, Symbols.ROCK, Symbols.SCISSORS),
            mock.call(Winner.DRAW, Symbols.SCISSORS, Symbols.SCISSORS),
            mock.call(Winner.COMPUTER, Symbols.PAPER, Symbols.ROCK),
        ]
        self.assertEqual(actual_calls, expected_calls)


class VanillaRPSRulesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.rules = VanillaRPSRules()

    def test_get_winner_same_symbol(self):
        with self.assertRaises(AssertionError):
            self.rules.get_winner(Symbols.ROCK, Symbols.ROCK)

    def test_get_winner_different_symbols(self):
        winner = self.rules.get_winner(Symbols.ROCK, Symbols.SCISSORS)
        self.assertEqual(winner, Symbols.ROCK)

        # order doesn't matter
        winner = self.rules.get_winner(Symbols.SCISSORS, Symbols.ROCK)
        self.assertEqual(winner, Symbols.ROCK)


if __name__ == '__main__':
    unittest.main()
