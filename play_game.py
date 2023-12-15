import time
import random
from enum import Enum

import inquirer
from rich.console import Console

import card_table
import game_actions
from game_state import *


console = Console()

CARD_BACK = 'card_back'

CARD_STYLES = {
    CARD_BACK: "#000000 on #ffffff",
    CardType.AMBASSADOR.name: "#ff00ff on #00ff00",
    CardType.ASSASSIN.name: "#ffffff on #000000",
    CardType.CAPTAIN.name: "#ff0000 on #00ffff",
    CardType.CONTESSA.name: "#00ffff on #ff0000",
    CardType.DUKE.name: "#00ff00 on #ff00ff",
}

PLAYER_TURN_STYLE = {
    True: "#0000ff on #ffff00",
    False: "#ffff00 on #0000ff",
}


class Action(Enum):
    INCOME = 'Income'
    FOREIGN_AID = 'Foreign Aid'
    COUP = 'Coup'
    TAX = 'Tax'
    ASSASSINATE = 'Assassinate'
    EXCHANGE = 'Exchange'
    STEAL = 'Steal'

    LIST = [
        INCOME,
        FOREIGN_AID,
        COUP,
        TAX,
        ASSASSINATE,
        EXCHANGE,
        STEAL,
    ]

    ACTION_FUNCTIONS = {
        INCOME: game_actions.income,
        FOREIGN_AID: game_actions.foreign_aid,
        COUP: game_actions.coup,
        TAX: game_actions.tax,
        ASSASSINATE: game_actions.assassinate,
        EXCHANGE: game_actions.exchange,
        STEAL: game_actions.steal,
    }


class Counteraction(Enum):
    INCOME = 'Income'
    FOREIGN_AID = 'Foreign Aid'
    COUP = 'Coup'
    TAX = 'Tax'
    ASSASSINATE = 'Assassinate'
    EXCHANGE = 'Exchange'
    STEAL = 'Steal'

    LIST = [
        INCOME,
        FOREIGN_AID,
        COUP,
        TAX,
        ASSASSINATE,
        EXCHANGE,
        STEAL,
    ]


def bot_choose_action(game, turn_player):

    time.sleep(1)

    target_player = None

    if turn_player.coins >= 10:

        action = Action.COUP.value

        print(f"{turn_player.name} must choose coup.")

    else:

        action_list = list(Action.LIST.value)

        if turn_player.coins < 7:
            del action_list[action_list.index(Action.COUP.value)]

        if turn_player.coins < 3:
            del action_list[action_list.index(Action.ASSASSINATE.value)]

        if turn_player.is_bot:

            action = random.choice(action_list)

        else:

            actions = [
                inquirer.List(
                    'action',
                    message="Choose an action",
                    choices=action_list,
                    carousel=True,
                ),
            ]

            action = inquirer.prompt(actions)
            action = action['action']

    if action in [Action.COUP.value, Action.ASSASSINATE.value, Action.STEAL.value]:

        player_list = [player for player in game.players if (
            player != turn_player
            and
            not player.is_out
            and (
                action != Action.STEAL.value
                or
                player.coins > 0
            )
        )]

        if turn_player.is_bot:

            target_player = random.choice(player_list)

        else:

            target_players = [
                inquirer.List(
                    'target_player',
                    message="Choose target player",
                    choices=player_list,
                    carousel=True,
                ),
            ]

            target_player = inquirer.prompt(target_players)
            target_player = target_player['target_player']

    return action, target_player

def get_counter_challenge_list(action):
    
    return {
        Action.INCOME.value: [],
        Action.FOREIGN_AID.value: ['duke blocks'],
        Action.COUP.value: [],
        Action.TAX.value: ['challenge'],
        Action.ASSASSINATE.value: ['contessa blocks', 'challenge'],
        Action.EXCHANGE.value: ['challenge'],
        Action.STEAL.value: ['ambassador or captain blocks', 'challenge'],        
    }[action]
    

def choose_block_action(game, action, target_player, counter_challenge_list):

    time.sleep(1)

    counteraction_challenge = []

    player_reactions = [player for player in game.players if player.position != game.player_turn and not player.is_out]
    random.shuffle(player_reactions)

    if counter_challenge_list != []:

        for player in player_reactions:
            if player.is_bot:

                if random.choice(range(game.player_count + 1)) == 0:
                    if len(counter_challenge_list) > 1:
                        choice = random.choice(counter_challenge_list)
                    else:
                        choice = counter_challenge_list[0]

                    counteraction_challenge.append(
                        [player, choice]
                    )
                    print(f"\n{player.name} counteracts/challenges: {choice}")
                    break
            
            if not player.is_bot:

                non_bot_counter_challenges = [
                    inquirer.List(
                        'counter_challenge',
                        message="Choose an option",
                        choices=["pass"] + counter_challenge_list,
                        carousel=True,
                    ),
                ]
                
                non_bot_counter_challenge = inquirer.prompt(non_bot_counter_challenges)

                choice = non_bot_counter_challenge['counter_challenge']
                
                counteraction_challenge.append(
                    [player, choice]
                )

                if counteraction_challenge[-1][1] != 'pass':
                    print(f"\nYou counteracted/challenged: {choice}")
                    break
                print("\nYou do not counteract or challenge.")
                time.sleep(1)

    if counteraction_challenge != [] and counteraction_challenge[-1][1] != 'pass':
        return counteraction_challenge[-1] 
    else:
        return None, None


def choose_challenge_counteraction(game, action, counteraction, block_action_player, target_player):

    time.sleep(1)

    counteraction_challenge = []

    player_reactions = [player for player in game.players if player.position != game.player_turn and player != block_action_player and not player.is_out]
    random.shuffle(player_reactions)

    for player in player_reactions:
        if player.is_bot:

            if random.choice(range(game.player_count + 1)) == 0:
                return player
                break
        
        if not player.is_bot:

            non_bot_counter_challenges = [
                inquirer.List(
                    'counter_challenge',
                    message="Choose an option",
                    choices=["pass", "challenge"],
                    carousel=True,
                ),
            ]
            
            non_bot_counter_challenge = inquirer.prompt(non_bot_counter_challenges)

            if non_bot_counter_challenge['counter_challenge'] == 'challenge':
                return player

            time.sleep(1)

    return None


def play():

    print('''
  /██████   /██████  /██   /██ /███████
 /██__  ██ /██__  ██| ██  | ██| ██__  ██
| ██  \__/| ██  \ ██| ██  | ██| ██  \ ██
| ██      | ██  | ██| ██  | ██| ███████/
| ██      | ██  | ██| ██  | ██| ██____/
| ██    ██| ██  | ██| ██  | ██| ██
|  ██████/|  ██████/|  ██████/| ██
 \______/  \______/  \______/ |__/
''')
    
    won = False
    play_game = True
    
    name = input('\nWhat is your first name or nick name?\nWhat should we call you?:\n\n> ').strip()

    if not name:
        name = "nobody"

    print(f'\nNice to meet you {name}!\n')

    while play_game:

        player_count_input = [
            inquirer.List(
                "player_count",
                message="How many players?",
                choices=[
                    6,
                    5,
                    4,
                    3,
                    2,
                ],
                carousel=True,
            ),
        ]
        
        player_count_result = inquirer.prompt(player_count_input)

        player_count = player_count_result['player_count']
        
        print(f"Number of players: {player_count}\n")

        game = Game(name=name, player_count=player_count, won=won)

        card_table.display(game)

        while not game.game_over:

            turn_player = game.players[game.player_turn]

            action = None
            target_player = None
            block_action_player = None
            block_action_type = None
            block_counter_player = None

            print(f'''
It is {turn_player.name}'s turn...
''')

            action, target_player = bot_choose_action(game, turn_player)

            action_string = f"{turn_player.name} chooses action: {action}"
            if target_player is not None:
                action_string += f"\n{turn_player.name}'s action targets: {target_player}"

            print(action_string)

            counter_challenge_list = get_counter_challenge_list(action)

            if counter_challenge_list != []:
                block_action_player, block_action_type = choose_block_action(game, action, target_player, counter_challenge_list)

                if block_action_type is None:
                    input(f'\nNo one counteracted or challenged.\nPress enter/return to continue...')
                else:
                    input(f'\n{block_action_player.name} counteraction/challenge: {block_action_type}\nPress enter/return to continue...')

                    if block_action_type != 'challenge':
                        block_counter_player = choose_challenge_counteraction(game, action, block_action_type, block_action_player, target_player)
                        if block_counter_player is not None:
                            input(f"\n{block_counter_player.name} challenges {block_action_player.name}'s counter.\nPress enter/return to continue...")
                        else:
                            input(f"\nNo one challenges {block_action_player.name}'s counter.\nPress enter/return to continue...")
                    else:
                        block_counter_player = None
                    
            else:
                input(f'\nAction performed.\nPress enter/return to continue...')

            Action.ACTION_FUNCTIONS.value[action](
                game=game,
                turn_player=turn_player,
                action=action,
                target_player=target_player,
                block_action_player=block_action_player,
                block_action_type=block_action_type,
                block_counter_player=block_counter_player,
            )

            while game.players[game.player_turn].is_out:
                game.player_turn = (game.player_turn + 1) % game.player_count

            card_table.display(game)

            remaining_players = [player for player in game.players if not player.is_out]
            if len(remaining_players) == 1:
                game.game_over = True
                if not remaining_players[0].is_bot:
                    won = True
                input(f"PLAYER {remaining_players[0].name} WINS !!!!\nPress enter/return to continue...")

        play_again_options = [
            inquirer.List(
                'play_again',
                message="Play again?",
                choices=[
                    False,
                    True,
                ],
                carousel=True,
            ),
        ]

        play_again = inquirer.prompt(play_again_options)
        
        print('Play again?:', play_again['play_again'])

        play_game = play_again['play_again']

if __name__ == '__main__':
    play()
