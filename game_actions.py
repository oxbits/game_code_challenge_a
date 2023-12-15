import random

import inquirer

from game_state import *


def income(game, turn_player, action, target_player, block_action_player, block_action_type, block_counter_player):

    game.treasury -= 1

    turn_player.coins += 1

    game.player_turn = (game.player_turn + 1) % game.player_count


def foreign_aid(game, turn_player, action, target_player, block_action_player, block_action_type, block_counter_player):

    game.treasury -= 2

    turn_player.coins += 2

    game.player_turn = (game.player_turn + 1) % game.player_count


def coup(game, turn_player, action, target_player, block_action_player, block_action_type, block_counter_player):

    turn_player.coins -= 7

    game.treasury += 7

    down_cards = [card for card in target_player.cards if card.face.value == 'down']

    if target_player.is_bot:
        target_card = random.choice(down_cards)

    else:
        card_choices = list(set([card.card.name for card in down_cards]))

        if len(card_choices) == 2:

            card_options = [
                inquirer.List(
                    'card_option',
                    message="Choose card to reveal",
                    choices=card_choices,
                    carousel=True,
                ),
            ]
            
            card_option = inquirer.prompt(card_options)
            
            print('card_option :', card_option['card_option'])

            card_option = card_option['card_option']

            target_card = [card for card in down_cards if card.card.name == card_option][0]

        else:
            target_card = down_cards[0]

    target_card.face = Face.UP

    if len([card for card in target_player.cards if card.face.value == 'down']) == 0:

        game.treasury += target_player.coins
        target_player.coins = 0
        target_player.is_out = True

    game.player_turn = (game.player_turn + 1) % game.player_count


def tax(game, turn_player, action, target_player, block_action_player, block_action_type, block_counter_player):

    game.treasury -= 3

    turn_player.coins += 3

    game.player_turn = (game.player_turn + 1) % game.player_count


def assassinate(game, turn_player, action, target_player, block_action_player, block_action_type, block_counter_player):

    turn_player.coins -= 3

    game.treasury += 3

    down_cards = [card for card in target_player.cards if card.face.value == 'down']

    if target_player.is_bot:
        target_card = random.choice(down_cards)

    else:
        card_choices = list(set([card.card.name for card in down_cards]))

        if card_choices == 2:

            card_options = [
                inquirer.List(
                    'card_option',
                    message="Choose card to reveal",
                    choices=card_choices,
                    carousel=True,
                ),
            ]
            
            card_option = inquirer.prompt(card_options)
            
            card_option = card_option['card_option']

            target_card = [card for card in down_cards if card.card.name == card_option][0]

        else:
            target_card = down_cards[0]

    target_card.face = Face.UP

    if len([card for card in target_player.cards if card.face.value == 'down']) == 0:

        game.treasury += target_player.coins
        target_player.coins = 0
        target_player.is_out = True

    game.player_turn = (game.player_turn + 1) % game.player_count


def exchange(game, turn_player, action, target_player, block_action_player, block_action_type, block_counter_player):

    down_cards = [card for card in turn_player.cards if card.face.value == 'down']

    down_card_count = len(down_cards)

    card_choices = []

    for card in down_cards:
        card_choices.append(turn_player.cards.pop(turn_player.cards.index(card)))
    
    for i in range(2):
        card_choices.append(game.court_deck.cards.pop())

    random.shuffle(card_choices)

    if turn_player.is_bot:

        turn_player.cards += card_choices[:down_card_count]
        game.court_deck.cards += card_choices[down_card_count:]
        random.shuffle(game.court_deck.cards)

    else: # non bot player

        card_choices_names = [card.card.name for card in card_choices]

        chosen_cards = []

        for i in range(down_card_count):

            card_options = [
                inquirer.List(
                    'card_option',
                    message="Select cards to keep",
                    choices=card_choices_names,
                    carousel=True,
                ),
            ]
            
            card_option = inquirer.prompt(card_options)

            card_option = card_option['card_option']

            target_card = [card for card in card_choices if card.card.name == card_option][0]
            
            chosen_cards.append(card_choices.pop(card_choices.index(target_card)))

        turn_player.cards += chosen_cards
        game.court_deck.cards += card_choices
        random.shuffle(game.court_deck.cards)

    game.player_turn = (game.player_turn + 1) % game.player_count


def steal(game, turn_player, action, target_player, block_action_player, block_action_type, block_counter_player):

    turn_player.coins += 2 if target_player.coins >= 2 else target_player.coins

    target_player.coins -= 2 if target_player.coins >= 2 else target_player.coins

    game.player_turn = (game.player_turn + 1) % game.player_count
