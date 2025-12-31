from .dealer import Dealer
from .player import Player
from .deck import Deck
from .playing_card import Rank
from . import blackjack, player_turn

def main():
    deck = Deck()
    player = Player()
    dealer = Dealer()

    while (player.bank.balance > 0 and
           dealer.bank.balance > 0):
        starting_bet = player_turn.player_ante(player)
        blackjack.start_round(dealer, player, deck, starting_bet)
        insurance: float = 0.0
        dealer_upcard = dealer.get_visible_card()
        if dealer_upcard.rank == Rank.ACE:
            insurance = player_turn.player_insurance(player, starting_bet)
        player_turn.player_turn(player, dealer_upcard, deck)
        blackjack.process_dealer_turn(dealer, deck)
        blackjack.settle_insurance(dealer, player, insurance, dealer.hand.has_blackjack)
        for hand in player.split_hands:
            result = blackjack.determine_winner(
                dealer_hand=dealer.hand, 
                player_hand=hand, 
                dealer_blackjack=dealer.hand.has_blackjack,
                player_blackjack=hand.has_blackjack)


if __name__ == "__main__":
    main()
