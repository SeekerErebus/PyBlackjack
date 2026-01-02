from .hand import Hand
from .deck import Deck
from .dealer import Dealer
from .player import Player
from .actor import Actor
from .playing_card import PlayingCard
from .blackjack import RoundResults


def get_hand_str(hand: Hand) -> str:
    result_str = f''
    delimiter = ", "
    for card in hand.cards:
        result_str += repr(card) + delimiter
    result_str += f"Value: {hand.get_hand_value()}"
    return result_str

def print_bank_balance(actor: Actor) -> None:
    bank = actor.bank
    bank.refresh()
    print(f"{actor.name} bank balance is: {bank.balance:,.2f}")

def show_round_start(dealer: Dealer, player: Player, deck: Deck) -> None:
    print(get_round_state_str(dealer.get_visible_card(), player, deck))
    print_bank_balance(player)
    print_bank_balance(dealer)

def show_end_of_round_state(dealer: Dealer, player: Player, end_state_str: str) -> None:
    print(end_state_str)
    print(f"Dealer Bank: {dealer.bank.balance}")
    print(f"Player Bank: {player.bank.balance}")

def get_round_state_str(dealer_upcard: PlayingCard, player: Player, deck: Deck) -> str:
    output_str = f"\nDealer Card is: {dealer_upcard}\n"
    output_str += get_player_hand_str(player)
    output_str += f"Deck has {deck.get_deck_percentage():.0%} remaining cards.\n"
    return output_str

def get_player_hand_str(player: Player) -> str:
    total_hands = len(player.split_hands)
    output_str = f""
    if total_hands > 1:
        for i in range(total_hands):
            current_hand = player.split_hands[i]
            output_str += f"Player Hand #{i + 1}: {get_hand_str(current_hand)}\n"
            if i == player.current_hand_index:
                output_str += f"Status: Active"
            elif current_hand.has_busted:
                output_str += f"Status: Busted"
            elif current_hand.has_stood:
                output_str += f"Status: Stood"
            else:
                output_str += f"Status: Waiting"
            output_str += f"\n\n"
    else:
        output_str += f"Player Hand is: {get_hand_str(player.hand)}\n"
    return output_str

def print_new_card(card: PlayingCard, whose_card: str) -> None:
    print(f"{whose_card} added {card}.")
