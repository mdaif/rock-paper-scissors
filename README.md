# About
This is a console-based game to simulate the Rock,Paper,Scissors game. It allows you to enter a choice of symbols (rock, paper, scissors), and randomly generate a symbol out of the allowed symbols, and based on the rules of the game, it'd determine who won and who lost.
The purpose of the game to brush up/ put my OOP design skills into action :-)

# Rules
- The n rounds is pre-determined. You specify the number of rounds you'd like to play when you run the game.
- As in real life, your opponent (the computer in this case) might pick the same symbol as you did. The behavior is to announce that it's a draw, continue playing and don't count this round. A round is done only when a user or the computer wins.

# Design
- The design follows the open-closed principle. Most of the classes are open to extension but close to modification.
- You can extend the game to allow two behaviors:
	1. You can create an extended version/ flavor of the same game, reusing the exact same logic but with different easy-to-define rules. As an example, I included the [Rock-Paper-Scissors-Lizard-Spock](https://bigbangtheory.fandom.com/wiki/Rock,_Paper,_Scissors,_Lizard,_Spock)
that have a slightly modified set of rules and it uses the same engine and user interface.
	2. I used Strategy Pattern to enable the client to change how to interact with the game. For simplicity I implemented a handler to accept user inputs interactively and to display the results on the console. This can be simply replaced by a handler that gets the input from a file/ sends the output to a file/ gets the input from network/ sends the output to a printer / or a combination of those ! More on how to do that later.
- I added some logging to reflect real life scenarios. In case of simple console-based handlers it has no real value, but if the handlers are placed with network based handlers, the loggers would be necessary to know what went on during a game. For simplicity, the loggers are console based but they can be configure to use other logging handlers as well.

# How to play
- The game is a console-based game.	You can run it from the command line as follows
 `python3 rock_paper_scissors.py --rounds 3`

- `--rounds` is required. It determines how many rounds you can play before the program terminates (Excluding the "draw" rounds.)
- There's an optional `--flavor` argument. It lets you play another flavor of the game. The second flavor that I implemented as a proof of extensiblity is  Rock-Paper-Scissors-Lizard-Spock but you can define other flavors with crazy rules (like inverting who can win after 9 O'clock !), more on how to do that later.
- If you wish to exit you can write STOP (this value can be changed in the code)
- User choices are validated automatically based on the flavor's defined rules.
- Wrong inputs are handled via argparse and there are useful help messages.
```
    $ python3 rock_paper_scissors.py --rounds 3 --flavos
    usage: rock_paper_scissors.py [-h] --rounds ROUNDS [--flavor {vanilla,rpsls}]
    rock_paper_scissors.py: error: unrecognized arguments: --flavos
```
```
    $ python3 rock_paper_scissors.py --rounds 3 --flavor somethingelse
    usage: rock_paper_scissors.py [-h] --rounds ROUNDS [--flavor {vanilla,rpsls}]
    rock_paper_scissors.py: error: argument --flavor: invalid choice: 'somethingelse' (choose from 'vanilla', 'rpsls')
```
```
    $ python3 rock_paper_scissors.py
    usage: rock_paper_scissors.py [-h] --rounds ROUNDS [--flavor {vanilla,rpsls}]
    rock_paper_scissors.py: error: the following arguments are required: --rounds
```
- Vanilla Rock Paper Scissors example:
```
    $ python3 rock_paper_scissors.py --rounds 3
    2019-09-22 14:12:57,138 Initializing engine for 3 rounds and VanillaRPSRules game
    Choose your symbol ['scissors', 'paper', 'rock'] [Enter STOP to exit]: paepr
    Invalid choice, please try again
    Choose your symbol ['scissors', 'paper', 'rock'] [Enter STOP to exit]: paper
    2019-09-22 14:14:05,252 Computer choice: scissors
    2019-09-22 14:14:05,253 Computer won
    And I choose scissors
    Tough luck scissors beats paper!
    Choose your symbol ['scissors', 'paper', 'rock'] [Enter STOP to exit]: paper
    2019-09-22 14:14:07,199 Computer choice: rock
    2019-09-22 14:14:07,199 User won
    And I choose rock
    You win !
    Choose your symbol ['scissors', 'paper', 'rock'] [Enter STOP to exit]: paepr
    Invalid choice, please try again
    Choose your symbol ['scissors', 'paper', 'rock'] [Enter STOP to exit]: paper
    2019-09-22 14:14:10,812 Computer choice: rock
    2019-09-22 14:14:10,812 User won
    And I choose rock
    You win !
    That was fun ! bye !
```
- Rock Paper Scissors Lizard Spock Example
```
    (venv)$ python3 rock_paper_scissors.py --rounds 3 --flavor rpsls
    2019-09-22 14:22:20,135 Initializing engine for 3 rounds and RockPaperScissorsLizardSpockRules game
    Choose your symbol ['spock', 'lizard', 'scissors', 'paper', 'rock'] [Enter STOP to exit]: spock
    2019-09-22 14:22:23,149 Computer choice: lizard
    2019-09-22 14:22:23,150 Computer won
    And I choose lizard
    Tough luck lizard beats spock!
    Choose your symbol ['spock', 'lizard', 'scissors', 'paper', 'rock'] [Enter STOP to exit]: paper
    2019-09-22 14:22:27,105 Computer choice: paper
    2019-09-22 14:22:27,105 DRAW ! Another round ...
    And I choose paper
    DRAW ! Another round ...
    Choose your symbol ['spock', 'lizard', 'scissors', 'paper', 'rock'] [Enter STOP to exit]: rock
    2019-09-22 14:22:30,114 Computer choice: rock
    2019-09-22 14:22:30,115 DRAW ! Another round ...
    And I choose rock
    DRAW ! Another round ...
    Choose your symbol ['spock', 'lizard', 'scissors', 'paper', 'rock'] [Enter STOP to exit]: scissors
    2019-09-22 14:22:33,222 Computer choice: scissors
    2019-09-22 14:22:33,222 DRAW ! Another round ...
    And I choose scissors
    DRAW ! Another round ...
    Choose your symbol ['spock', 'lizard', 'scissors', 'paper', 'rock'] [Enter STOP to exit]: lizard
    2019-09-22 14:22:37,375 Computer choice: spock
    2019-09-22 14:22:37,375 User won
    And I choose spock
    You win !
    Choose your symbol ['spock', 'lizard', 'scissors', 'paper', 'rock'] [Enter STOP to exit]: lizard
    2019-09-22 14:22:40,920 Computer choice: paper
    2019-09-22 14:22:40,920 User won
    And I choose paper
    You win !
    That was fun ! bye !
```

# Testing
- I didn't use any external testing frameworks, only the standard Python unittest. All tests live under tests.py module.
- You can run the tests by issuing the command

    `python3 -m unittest`

under the project's root directory

# How to extend

## To extend the symbols
You add new values to Symbols enumeration (under rules.py)

## To extend the rules (Define a new flavor)
### Simple Extension
If the goal is to change who beats whom or adding new symbols then defining which symbol wins over what, you can simply create a new child class of BaseRPSRules and override _defeats attribute. In this case the get_winner super method takes care of returning the winning symbol for the clients.

### More elaborate rules
If you'd like to have more freedom (like determining different rules based on the time of the day), you can override the get_winner method.

### After defining the rules
The console-based game needs to map user inputs to flavors and give a meaningful description. That's why you'll have to also extend the SUPPORTED_GAME_FLAVORS (under constants.py) with a user friendly name, the new flavor class, and a human-readable description.

## To create a new handler
All handlers live under components.py. A new handler for user choices should extend UserChoice and override get method. If you would like to create a new handler for responses, you should extend ConsoleResultHandler and override the send method.

## Initializing the engine.
As previously mentioned, I separated what might vary, in a strategy pattern fashion. Determining which handler is used and which game flavor to play are done while initializing the Engine object.
set game_rules to one of BaseRPSRules implementations.
set user_choice to one of UserChoice implementations.
set result_handler to one of ResultHandler implementations.
