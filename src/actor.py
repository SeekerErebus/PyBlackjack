from .bank import Bank
from .playing_card import PlayingCard
from .hand import Hand
from .blackjack import RoundResults
from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class RoundRecord:
    outcome: RoundResults
    bet: float

class RoundHistory:
    def __init__(self) -> None:
        self.records: list[RoundRecord] = []
    
    def add_round(self, outcome: RoundResults, bet: float | int):
        self.records.append(RoundRecord(outcome, float(bet)))

class Actor:
    """
    An Actor superclass for Dealers and Players.
    Attributes:
        name (str): The Actor Name
        bank (Bank): The Actor's Bank
        hand (Hand): The Actor's Hand
    """
    def __init__(self, name: str, starting_balance: float | int = 0.0) -> None:
        """
        Actor constructor
        
        :param name: Name of the Actor
        :type name: str
        :param starting_balance: The starting bank balance of the Actor
        :type starting_balance: float | int
        """
        self.name = name
        self.bank = Bank(balance=starting_balance)
        self.split_hands: list[Hand] = [Hand([])]
        self.current_hand_index: int = 0
        self.hand: Hand = self.split_hands[self.current_hand_index]
        self.history = RoundHistory()

    def reset_hand(self) -> None:
        """
        Reset the hand to nothing.
        """
        self.hand = Hand([])
    
    def start_hand(self, starting_cards: list[PlayingCard], bet_value: float | int = 0) -> None:
        """
        Starts a new hand.
        
        :param starting_cards: The new cards for the hand.
        :type starting_cards: list[PlayingCard]
        :param bet_value: The bet value of the hand.
        :type bet_value: float | int
        """
        self.hand = Hand(starting_cards=starting_cards, bet_value=bet_value)