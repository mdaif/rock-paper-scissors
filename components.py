from abc import ABCMeta

from constants import EXIT_WORD, Winner


class UserChoice(metaclass=ABCMeta):
    def get(self, valid_choices):
        raise NotImplementedError()


class ResultHandler(metaclass=ABCMeta):
    def send(self, result, user_choice, computer_choice):
        raise NotImplementedError()


class ConsoleUserChoice(UserChoice):
    def get(self, valid_choices):
        msg = f'Choose your symbol {list(valid_choices)}' \
              f' [Enter {EXIT_WORD} to exit]: '

        user_choice = input(msg)
        while user_choice not in valid_choices:
            if user_choice == EXIT_WORD:
                print("Bye !")
                exit()

            print('Invalid choice, please try again')
            user_choice = input(msg)
            continue
        return user_choice


class ConsoleResultHandler(ResultHandler):
    def send(self, winner, user_choice, computer_choice):
        print(f'And I choose {computer_choice.name.lower()}')
        if winner == Winner.DRAW:
            print('DRAW ! Another round ... ')
        elif winner == Winner.USER:
            print('You win !')
        else:
            print(
                f'Tough luck {computer_choice.name.lower()}'
                f' beats {user_choice.name.lower()}!')
