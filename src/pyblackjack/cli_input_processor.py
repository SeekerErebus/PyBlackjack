from .blackjack import PossibleActions
from . import constants


NUMBER_ERROR_STRING = "Please enter a valid number."
OVER_BALANCE_STRING = "You don't have enough money."

def prompt_bet(balance: float) -> float:
    """
    Gets the bet placed by the player from CLI for the round.
    
    :param balance: The balance ie. bank.balance
    :type balance: float
    :return: Description
    :rtype: float
    """
    min_bet = constants.MINIMUM_BET
    while True:
        print(f"\nYour current balance: {balance:,.2f}.")
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

def prompt_insurance(balance: float, current_bet: float) -> float:
    """
    Gets the insurance the player wishes to get on the hand. If returns 0, no insurance is purchased.
    
    :param balance: Player's balance
    :type balance: float
    :param current_bet: The bet on the hand.
    :type current_bet: float
    :return: The amount the player chooses to insure.
    :rtype: float
    """
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
        round_state_str: str,
        allowed_actions: set[PossibleActions]
) -> PossibleActions:
    valid_options: list[str] = []
    display_options: list[str] = []
    for action in allowed_actions:
        match action:
            case PossibleActions.HIT:
                valid_options.extend(['h'])
                display_options.append("h = Hit")
            case PossibleActions.STAND:
                valid_options.extend(['s'])
                display_options.append("s = Stand")
            case PossibleActions.DOUBLE:
                valid_options.extend(['d', 'dd'])
                display_options.append("d/dd = Double Down")
            case PossibleActions.SPLIT:
                valid_options.extend(['sp', 'split'])
                display_options.append("sp/split = Split")
    
    print(f"{round_state_str}\n")
    print(f"Options: " + ', '.join(display_options))

    while True:
        raw = input("Your move: ").strip().lower()
        result: PossibleActions
        if raw in valid_options:
            for option in valid_options:
                match raw:
                    case 'h':
                        result = PossibleActions.HIT
                    case 's':
                        result = PossibleActions.STAND
                    case 'd' | 'dd':
                        result = PossibleActions.DOUBLE
                    case 'sp' | 'split':
                        result = PossibleActions.SPLIT
            return result # type: ignore
        else:
            print("Invalid input. Use one of the listed options.")
