from enum import Enum

class Rank(Enum):
    """
    An Enum covering the available card ranks. Ace is default 1.
    """
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    def __repr__(self) -> str:
        return f"{self.name.title().capitalize()}"

class Suit(Enum):
    """
    An Enum covering the 4 suits.
    """
    SPADES = 1
    HEARTS = 2
    CLUBS = 3
    DIAMONDS = 4

    def __repr__(self) -> str:
        return f"{self.name.title().capitalize()}"

class PlayingCard:
    """
    A single playing card from a 52 card deck.
    
    Attributes:
        rank (Rank): The rank of the card.
        suit (Suit): The suit of the card.
        value (Literal [1 - 10]): The value of the card, Ace is 1, Face card is 10.
    """
    def __init__(self, rank: Rank, suit: Suit) -> None:
        self.suit = suit
        self.rank = rank
        self.value = 10 if rank.value > 10 else rank.value

    def __repr__(self) -> str:
        return f"{repr(self.rank)} of {repr(self.suit)}"