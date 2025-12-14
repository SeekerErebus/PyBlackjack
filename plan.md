Here's the plan on how to put this whole thing together.

- PlayingCard class defines a playing card from the deck, and will have some equation handling
- Deck class will handle the 52 card deck, and support reset, shuffle, and draw operations.
- Hand class will cover a player or dealer's hand, with current hand totals.
- Bank class will handle the account balances.
- Blackjack class will cover the game rules, and the viable actions that can be taken in-game.
- Actor class will be the super of the Dealer and the Player.
- Dealer class will handle the Dealer's actions, their hand, and their Bank.
- Player class will handle the Player's actions, their hand, and their Bank.
- main.py will link it all together, running the game, and determining when the player is out of the game cause they're broke, or pulls off the insane and takes the Dealer to zero.