from .dealer import Dealer
from .player import Player
from .deck import Deck
from .playing_card import Rank
from . import blackjack, player_turn
from .cli_input_processor import prompt_continue_game
from .cli_output_processor import show_end_of_round_state, show_game_end_score

def main():
    deck = Deck()
    player = Player()
    starting_player_balance = player.bank.balance
    dealer = Dealer()

    while (player.bank.balance > 0 and
           dealer.bank.balance > 0):
        starting_bet = player_turn.player_ante(player)
        # Debug
        #print(f"DEBUG: Post ante, starting_bet: {starting_bet}")
        blackjack.start_round(dealer, player, deck, starting_bet)
        insurance: float = 0.0
        dealer_upcard = dealer.get_visible_card()
        if dealer_upcard.rank == Rank.ACE:
            insurance = player_turn.player_insurance(player, starting_bet)
        player_turn.player_turn(player, dealer_upcard, deck)
        blackjack.process_dealer_turn(dealer, deck)
        blackjack.settle_insurance(dealer, player, insurance, dealer.hand.has_blackjack)
        end_state_str = f""
        # Debug
        #debug_count = 0
        for hand in player.split_hands:
            # Debug
            #print(f"DEBUG: main, for hand in player.split_hands")
            #print(f"    hand number: {debug_count}")
            #debug_count += 1
            #print(f"    bet: {hand.bet.balance}")
            # End Debug
            result = blackjack.determine_winner(
                dealer_hand=dealer.hand, 
                player_hand=hand, 
                dealer_blackjack=dealer.hand.has_blackjack,
                player_blackjack=hand.has_blackjack)
            end_state_str += blackjack.settle_bets(dealer, player, hand.bet.balance, result)
        show_end_of_round_state(dealer, player, end_state_str)
        player.bank.refresh()
        dealer.bank.refresh()
        if not prompt_continue_game():
            break
        deck.confirm_deck_health()
    show_game_end_score(starting_player_balance, player.bank.balance, dealer.bank.balance)
    print("Thanks for Playing!")


if __name__ == "__main__":
    main()
