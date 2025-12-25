"""
Planning setup
Each player is trying to get as close to 21 without going over, and plays against the dealer directly.
If the player beats the dealer without busting, the player wins, if the dealer beats the player, the dealer wins.
Jack, Queen, and King are 10 points, 2 through 10 is the value listed, Ace is 11 unless the hand exceeds 21, in which case it is 1.
Step 1: All players place bets with their chips, there is a minimum value.
Step 2: The dealer deals one card face up to all players and themselves. They then deal a second card face up to all players, and one card face down to themselves.
Step 3: The player takes their turn, see Player Actions.
Step 4: The dealer reveals their second card. If they don't have a blackjack, and their total is 16 or less, they hit. If they are 17 or higher, they stay.
Step 5: Settle bets, see Settling Bets

Player Actions:
- Stay: End turn
- Hit: Be dealt another card, decide next action (Hit or Stay)
- Double down: Hit one more card and end turn, double initial bet.
- Split: If the two cards are the same value, a split can be done. Put down the same amount of the initial bet, turn the initial hand into two hands, handle each hand separately from there.
- Insurance: If the dealer card is an Ace, the player may place an insurance bet equal or less than the original bet, see Settling Bets

Settling Bets:
- If the dealer gets a blackjack, the player automatically loses even if they hit to 21. Unless they also had a blackjack, then a push as noted below.
- If the player and dealer both have the same value, then there is a push, with the player getting their original bet back.
- If the player wins against the dealer, the hand is paid out 1 to 1. If the player got a blackjack, the player gets paid out 3 to 2.
- If there is an insurance bet, and the dealer has a blackjack, the original bet loses, but the insurance bet pays out 2 to 1. If the dealer does not have a blackjack, the insurance bet is lost.
"""

from .hand import Hand
from .bank import Bank
from .dealer import Dealer
from .player import Player
from .playing_card import PlayingCard
from .deck import Deck
from enum import Enum

BLACKJACK_PAYOUT = 3 / 2
STANDARD_PAYOUT = 1
INSURANCE_PAYOUT = 2

class RoundResults(Enum):
    DEALER_WON = 1
    PLAYER_WON = 2
    PLAYER_WON_BLACKJACK = 3
    PUSH = 4

def determine_winner(dealer_hand: Hand, player_hand: Hand, dealer_blackjack: bool = False, player_blackjack: bool = False) -> RoundResults:
    """
    Determines the winner of the round based on the dealer and player's hands. 
    
    :param dealer_hand: The Dealer's hand
    :type dealer_hand: Hand
    :param player_hand: The Player's hand
    :type player_hand: Hand
    :param dealer_blackjack: Whether the Dealer had a blackjack.
    :type dealer_blackjack: bool
    :param player_blackjack: Whether the player had a blackjack.
    :type player_blackjack: bool
    :return: The result of the round.
    :rtype: RoundResults
    """
    if dealer_blackjack and not player_blackjack:
        return RoundResults.DEALER_WON
    dealer_result = dealer_hand.get_hand_value()
    player_result = player_hand.get_hand_value()
    if player_result > dealer_result and player_blackjack:
        return RoundResults.PLAYER_WON_BLACKJACK
    elif player_result > dealer_result:
        return RoundResults.PLAYER_WON
    elif dealer_result > player_result:
        return RoundResults.DEALER_WON
    return RoundResults.PUSH
    
def settle_bets(dealer: Player, player: Player, pot: Bank, results: RoundResults) -> None:
    """
    Settles the bet between the bank and the player, adjusting bank balances accordingly.
    
    :param dealer_bank: The Dealer's bank
    :type dealer_bank: Bank
    :param player_bank: The Player's bank
    :type player_bank: Bank
    :param pot: The bet
    :type pot: Bank
    :param results: Who won the round and how.
    :type results: RoundResults
    """
    pot.refresh()
    bet = pot.balance
    match results:
        case RoundResults.DEALER_WON:
            dealer.bank.add_transaction("Won Round", bet)
        case RoundResults.PLAYER_WON:
            dealer.bank.add_transaction("Lost Round", -bet * STANDARD_PAYOUT)
            player.bank.add_transaction("Won Round", bet * STANDARD_PAYOUT)
        case RoundResults.PLAYER_WON_BLACKJACK:
            dealer.bank.add_transaction("Lost Round", -bet * BLACKJACK_PAYOUT)
            player.bank.add_transaction("Won Round", bet * BLACKJACK_PAYOUT)
        case RoundResults.PUSH:
            player.bank.add_transaction("Pushed Round", bet)
    dealer.history.add_round(results, bet)
    player.history.add_round(results, bet)

def settle_insurance(dealer: Dealer, player: Player, pot: Bank, dealer_blackjack: bool) -> None:
    """
    Settles insurance payouts when Insurance is used.
    
    :param dealer_bank: The Dealer's bank
    :type dealer_bank: Bank
    :param player_bank: The Player's bank
    :type player_bank: Bank
    :param pot: The bet
    :type pot: Bank
    :param dealer_blackjack: Whether the dealer got a blackjack and thus insurance is owed.
    :type dealer_blackjack: bool
    """
    pot.refresh()
    if dealer_blackjack:
        dealer.bank.add_transaction("Insurance Payout", -pot.balance * INSURANCE_PAYOUT)
        player.bank.add_transaction("Insurance Payout", pot.balance * INSURANCE_PAYOUT)
    else:
        dealer.bank.add_transaction("Insurance Payout", pot.balance)

def start_round(dealer: Dealer, player: Player, deck: Deck, bet_value: float | int) -> None:
    """
    Starts a round of blackjack.
    
    :param dealer: The Dealer
    :type dealer: Dealer
    :param player: The Player
    :type player: Player
    :param deck: The Deck
    :type deck: Deck
    :param bet_value: The value of the bet.
    :type bet_value: float | int
    """
    dealer.reset_hand()
    player.reset_hand()
    player_hand: list[PlayingCard] = []
    dealer_hand: list[PlayingCard] = []
    for _ in range(2):
        player_hand.append(deck.drawCard())
        dealer_hand.append(deck.drawCard())
    dealer.start_hand(dealer_hand, bet_value)
    player.start_hand(player_hand, bet_value)
    if dealer.hand.get_hand_value() == 21:
        dealer.hand.has_blackjack = True
    if player.hand.get_hand_value() == 21:
        player.hand.has_blackjack = True

def process_dealer_turn(dealer: Dealer, deck: Deck) -> int:
    """
    Runs the dealer's turn. 
    
    :param dealer: The Dealer
    :type dealer: Dealer
    :param deck: The Deck
    :type deck: Deck
    :return: The final hand value.
    :rtype: int
    """
    if dealer.hand.has_blackjack == True:
        return dealer.hand.get_hand_value()
    while dealer.hand.get_hand_value() < 17:
        dealer.hand.add_card(deck.drawCard())
    return dealer.hand.get_hand_value()
