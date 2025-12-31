from .player import Player
from .deck import Deck
from .playing_card import PlayingCard
from .blackjack import PossibleActions
from .cli_input_processor import prompt_bet, prompt_insurance, prompt_action
from . import constants
from . import cli_output_processor

def player_ante(player: Player) -> float:
    """
    Gets the player's bet for the round.
    
    :param player: Player object
    :type player: Player
    :return: The bet the player makes.
    :rtype: float
    """
    return prompt_bet(player.bank.balance)

def player_insurance(player: Player, bet_value: float) -> float:
    """
    Docstring for player_insurance
    
    :param player: The Player
    :type player: Player
    :param bet_value: The value of the bet, representing the maximum insurance
    :type bet_value: float
    :return: The insurance bet
    :rtype: float
    """
    return prompt_insurance(player.bank.balance, bet_value)

def player_turn(player: Player, dealer_upcard: PlayingCard, deck: Deck) -> None:
    """
    Runs the player turn.
    
    :param player: The Player
    :type player: Player
    :param dealer_upcard: The Dealer's visible card
    :type dealer_upcard: PlayingCard
    :param deck: The deck.
    :type deck: Deck
    """
    while player.current_hand_index < len(player.split_hands):
        while not player.hand.has_stood:
            round_state_str = cli_output_processor.get_round_state_str(dealer_upcard, player, deck)
            current_hand = player.hand
            player_action_set: set[PossibleActions] = { PossibleActions.HIT, PossibleActions.STAND }
            if len(current_hand.cards) == 2:
                player_action_set.add(PossibleActions.DOUBLE)
                if (current_hand.cards[0].rank == current_hand.cards[1].rank and 
                    deck.get_deck_percentage() > constants.DECK_REFRESH_PERCENTAGE and
                    player.bank.balance > current_hand.bet.balance):
                    player_action_set.add(PossibleActions.SPLIT)
            choice = prompt_action(round_state_str, player_action_set)
            match choice:
                case PossibleActions.HIT:
                    new_card = deck.drawCard()
                    cli_output_processor.print_new_card(new_card, player.name)
                    current_hand.add_card(new_card)
                case PossibleActions.DOUBLE:
                    new_card = deck.drawCard()
                    cli_output_processor.print_new_card(new_card, player.name)
                    current_hand.double_down(new_card)
                case PossibleActions.SPLIT:
                    drawn_cards: list[PlayingCard] = []
                    for _ in range(2):
                        new_card = deck.drawCard()
                        cli_output_processor.print_new_card(new_card, player.name)
                        drawn_cards.append(new_card)
                    player.split(drawn_cards)
                case PossibleActions.STAND:
                    current_hand.has_stood = True
        player.next_hand()