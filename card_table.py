import inquirer
from rich.console import Console

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


def display(game):

        for player_pair in [game.players[p:p + 2] for p in range(0, len(game.players), 2)]:

            console.print(
                f" {'{:28.28}'.format(player_pair[0].name.upper())}",
                end='  ',
                style=PLAYER_TURN_STYLE[player_pair[0].is_turn()],
            )
            if len(player_pair) == 2:
                console.print(
                    f" {'{:30.30}'.format(player_pair[1].name.upper())}",
                    style=PLAYER_TURN_STYLE[player_pair[1].is_turn()],
                )
            else:
                print()

            console.print(
                f" COINS: {str(player_pair[0].coins).rjust(2)[:2]} {'{:18.18}'.format('●' * player_pair[0].coins)}",
                end='  ',
                style=PLAYER_TURN_STYLE[player_pair[0].is_turn()],
            )
            if len(player_pair) == 2:
                console.print(
                    f" COINS: {str(player_pair[1].coins).rjust(2)[:2]} {'{:19.19}'.format('●' * player_pair[1].coins)} ",
                    style=PLAYER_TURN_STYLE[player_pair[1].is_turn()],
                )
            else:
                print()

            console.print(
                ' ',
                style=PLAYER_TURN_STYLE[player_pair[0].is_turn()],
                end='',
            )
            for card in player_pair[0].cards:
                if card.face == Face.DOWN:
                    console.print(
                        '┌────────────┐',
                        style=CARD_STYLES[CARD_BACK],
                        end='',
                    )
                    console.print(
                        ' ',
                        style=PLAYER_TURN_STYLE[player_pair[0].is_turn()],
                        end='',
                    )

                else:
                    console.print(
                        '┌────────────┐',
                        style=CARD_STYLES[card.card.name],
                        end='',
                    )
                    console.print(
                        ' ',
                        style=PLAYER_TURN_STYLE[player_pair[0].is_turn()],
                        end='',
                    )

            if len(player_pair) == 2:

                console.print(
                    ' ',
                    style=PLAYER_TURN_STYLE[player_pair[1].is_turn()],
                    end='',
                )

                for card in player_pair[1].cards:
                    if card.face == Face.DOWN:
                        console.print(
                            '┌────────────┐',
                            style=CARD_STYLES[CARD_BACK],
                            end='',
                        )
                    else:
                        console.print(
                            '┌────────────┐',
                            style=CARD_STYLES[card.card.name],
                            end='',
                        )
                    console.print(
                        ' ',
                        style=PLAYER_TURN_STYLE[player_pair[1].is_turn()],
                        end='',
                    )
            
            print()
            console.print(
                ' ',
                style=PLAYER_TURN_STYLE[player_pair[0].is_turn()],
                end='',
            )
            for card in player_pair[0].cards:
                if card.face == Face.DOWN and not player_pair[0].is_bot:
                    console.print(
                        f'│ {(card.card.name.lower() + " " * 10)[:10]} │',
                        style=CARD_STYLES[CARD_BACK],
                        end='',
                    )
                elif card.face == Face.DOWN:
                    console.print(
                        '│    coup    │',
                        style=CARD_STYLES[CARD_BACK],
                        end='',
                    )
                else:
                    console.print(
                        f'│ {(card.card.name + " " * 10)[:10]} │',
                        style=CARD_STYLES[card.card.name],
                        end='',
                    )
                console.print(
                    ' ',
                    style=PLAYER_TURN_STYLE[player_pair[0].is_turn()],
                    end='',
                )

            if len(player_pair) == 2:

                console.print(
                    ' ',
                    style=PLAYER_TURN_STYLE[player_pair[1].is_turn()],
                    end='',
                )

                for card in player_pair[1].cards:
                    if card.face == Face.DOWN and not player_pair[1].is_bot:
                        console.print(
                            f'│ {(card.card.name.lower() + " " * 10)[:10]} │',
                            style=CARD_STYLES[CARD_BACK],
                            end='',
                        )
                    elif card.face == Face.DOWN:
                        console.print(
                            '│    coup    │',
                            style=CARD_STYLES[CARD_BACK],
                            end='',
                        )
                    else:
                        console.print(
                            f'│ {(card.card.name + " " * 10)[:10]} │',
                            style=CARD_STYLES[card.card.name],
                            end='',
                        )
                    console.print(
                        ' ',
                        style=PLAYER_TURN_STYLE[player_pair[1].is_turn()],
                        end='',
                    )

            print()
            console.print(
                ' ',
                style=PLAYER_TURN_STYLE[player_pair[0].is_turn()],
                end='',
            )


            for card in player_pair[0].cards:
                if card.face == Face.DOWN:
                    console.print(
                        '└────────────┘',
                        style=CARD_STYLES[CARD_BACK],
                        end='',
                    )
                    console.print(
                        ' ',
                        style=PLAYER_TURN_STYLE[player_pair[0].is_turn()],
                        end='',
                    )

                else:
                    console.print(
                        '└────────────┘',
                        style=CARD_STYLES[card.card.name],
                        end='',
                    )
                    console.print(
                        ' ',
                        style=PLAYER_TURN_STYLE[player_pair[0].is_turn()],
                        end='',
                    )

            if len(player_pair) == 2:

                console.print(
                    ' ',
                    style=PLAYER_TURN_STYLE[player_pair[1].is_turn()],
                    end='',
                )

                for card in player_pair[1].cards:
                    if card.face == Face.DOWN:
                        console.print(
                            '└────────────┘',
                            style=CARD_STYLES[CARD_BACK],
                            end='',
                        )

                    else:
                        console.print(
                            '└────────────┘',
                            style=CARD_STYLES[card.card.name],
                            end='',
                        )
                    console.print(
                        ' ',
                        style=PLAYER_TURN_STYLE[player_pair[1].is_turn()],
                        end='',
                    )
        
            print()
            console.print(
                ' ' * 31,
                style=PLAYER_TURN_STYLE[player_pair[0].is_turn()],
                end='',
            )
            if len(player_pair) == 2:
                console.print(
                    ' ' * 31,
                    style=PLAYER_TURN_STYLE[player_pair[1].is_turn()],
                    end='',
                )
            print()
        print()

        input("Press enter/return to continue...")

        print()