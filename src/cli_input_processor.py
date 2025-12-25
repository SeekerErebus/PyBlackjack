from .playing_card import PlayingCard

NUMBER_ERROR_STRING = "Please enter a valid number."
OVER_BALANCE_STRING = "You don't have enough chips."

class CLIInputProcessor:
    
    ACTION_ABBREVS = {
        'h': 'hit',
        's': 'stand',
        'd': 'double',
        'dd': 'double',
        'sp': 'split',
        'sur': 'surrender',
    }
    def prompt_bet(self, balance: float, min_bet: float | int = 1.0) -> float:
        while True:
            print(f"\nYour current balance: {balance} chips.")
            try:
                raw = input(f"Place your bet (minimum {min_bet}): ").strip()
                bet = float(raw)
                if bet < min_bet:
                    print(f"Bet must be at least {min_bet}.")
                elif bet > balance:
                    print(OVER_BALANCE_STRING)
                else:
                    return bet
            except ValueError:
                print(NUMBER_ERROR_STRING)

    def prompt_insurance(self, balance: float, current_bet: float) -> float:
        min_insurance = current_bet * 0.1
        if min_insurance > balance:
            print(f"Dealer shows Ace, but you cannot afford minimum insurance.")
            return 0.0
        while True:
            print(f"Dealer shows Ace. You can take insurance up to {current_bet} and minimum is {min_insurance}.")
            raw = input("Take Insurance? (y/n): ").strip().lower()
            if raw in ('y', 'yes'):
                while True:
                    try:
                        raw = input(f"Amount (max {current_bet}): ").strip()
                        insurance = float(raw)
                        if insurance < min_insurance:
                            print(f"Amount must be at least {min_insurance}")
                        elif insurance > balance:
                            print(OVER_BALANCE_STRING)
                        else:
                            return insurance
                    except ValueError:
                        print(NUMBER_ERROR_STRING)
            elif raw in ('n', 'no'):
                return 0.0
            else:
                print("Please answer y or n.")
    
    def prompt_action(
            self,
            player_hand_value: int,
            player_cards: list[PlayingCard],
            dealer_upcard: PlayingCard
    ):
        pass