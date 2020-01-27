import argparse
import logging.config

from components import ConsoleUserChoice, ConsoleResultHandler
from constants import SUPPORTED_GAME_FLAVORS
from engine import Engine


def get_game_rules(flavor):
    return SUPPORTED_GAME_FLAVORS[flavor][0]()


def get_game_description(flavor):
    return SUPPORTED_GAME_FLAVORS[flavor][1]


def get_supported_flavors_choices():
    return list(SUPPORTED_GAME_FLAVORS.keys())


def get_supported_flavors_descriptions():
    return "".join([val[1] for val in SUPPORTED_GAME_FLAVORS.values()])


def _configure_logging():
    configs = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'local': {
                'format': '%(asctime)s %(message)s',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'local',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
            }
        }
    }

    logging.config.dictConfig(configs)


def main(rounds: int, flavor: str):
    flavor_rules = get_game_rules(flavor)
    engine = Engine(
        rounds=rounds,
        game_rules=flavor_rules,
        user_choice=ConsoleUserChoice(),
        result_handler=ConsoleResultHandler(),
    )
    engine.play_n_rounds(rounds)
    print('That was fun ! bye !')


if __name__ == '__main__':
    _configure_logging()

    parser = argparse.ArgumentParser(
        description='Play a game of Rock-Paper-Scissors')
    parser.add_argument(
        '--rounds', type=int, help='Number of rounds to play', required=True)

    parser.add_argument(
        '--flavor', default=get_supported_flavors_choices()[0],
        help=f'Game flavors: {get_supported_flavors_descriptions()}',
        choices=get_supported_flavors_choices(),
    )
    args = parser.parse_args()
    main(args.rounds, args.flavor)
