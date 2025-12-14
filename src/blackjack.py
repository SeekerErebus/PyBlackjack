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
from enum import Enum

BLACKJACK_PAYOUT = 3 / 2
STANDARD_PAYOUT = 1
INSURANCE_PAYOUT = 2

class RoundResults(Enum):
    DEALER_WON = 1
    PLAYER_WON = 2
    PLAYER_WON_BLACKJACK = 3
    PUSH = 4

def determine_winner(dealer: Hand, player: Hand, dealer_blackjack: bool = False, player_blackjack: bool = False) -> RoundResults:
    """
    Determines the winner of the round based on the dealer and player's hands. 
    
    :param dealer: Dealer's hand.
    :type dealer: Hand
    :param player: Player's hand.
    :type player: Hand
    :return: True if the player won, False if the dealer won.
    :rtype: bool
    """
    if dealer_blackjack and not player_blackjack:
        return RoundResults.DEALER_WON
    dealer_result = dealer.get_hand_value()
    player_result = player.get_hand_value()
    if player_result > dealer_result and player_blackjack:
        return RoundResults.PLAYER_WON_BLACKJACK
    elif player_result > dealer_result:
        return RoundResults.PLAYER_WON
    elif dealer_result > player_result:
        return RoundResults.DEALER_WON
    return RoundResults.PUSH
    
def settle_bets(dealer: Bank, player: Bank, pot: Bank, results: RoundResults) -> None:
    pot.refresh()
    match results:
        case RoundResults.DEALER_WON:
            dealer.add_transaction("Won Round", pot.balance)
        case RoundResults.PLAYER_WON:
            dealer.add_transaction("Lost Round", -pot.balance * STANDARD_PAYOUT)
            player.add_transaction("Won Round", pot.balance * STANDARD_PAYOUT)
        case RoundResults.PLAYER_WON_BLACKJACK:
            dealer.add_transaction("Lost Round", -pot.balance * BLACKJACK_PAYOUT)
            player.add_transaction("Won Round", pot.balance * BLACKJACK_PAYOUT)
        case RoundResults.PUSH:
            player.add_transaction("Pushed Round", pot.balance)

def settle_insurance(dealer: Bank, player: Bank, pot: Bank, dealer_blackjack: bool) -> None:
    pot.refresh()
    if dealer_blackjack:
        dealer.add_transaction("Insurance Payout", -pot.balance * INSURANCE_PAYOUT)
        player.add_transaction("Insurance Payout", pot.balance * INSURANCE_PAYOUT)
    else:
        dealer.add_transaction("Insurance Payout", pot.balance)