# EverythingIsTrump

This project contains a multiplayer implementation of this game: https://en.wikipedia.org/wiki/Oh_Hell, 
the "Devil's Bridge" variant in particular.

## Rules of the game

The game is played with a (full) French card deck.
Each player is dealt an increasing, and then decreasing amount of cards.
In the first round, everyone gets 1 card, then 2, 3, ..., 12, 13, 12, ... and 1 card again.
This means the game consists of 25 rounds in total.

### Bidding

In every round, players have to guess the number of tricks they are going to take and then try to make the same number of tricks.
The bidding goes sequentially, starting from the leading player, 
with the restriction that the last person cannot make a bid that would allow everyone to succeed. 
The sum of all bids can't be equal to the number of tricks in that round.

One extra modification: Card visibility is reversed in the one-card rounds. You can see the cards of everyone else but not yours!

### Cardplay

The play has similar rules to bridge - turn goes clockwise, you have to follow suit but not obliged to take a trick if you don't want to.
The only difference is that nature of the trump suit - there is no particular trump, every card count as a trump other than the suit that was actually led.
The strength of trumps follows the number first, suit (bridge order) second.
This means that a 6 is higher than any 5, lower than any 7 and the 6 of diamonds is stronger than the 6 of clubs.

**Examples:** <br/>
C6 - C7 - CA - CK: Everyone followed suit, the highest card (CA) takes the trick <br/>
C6 - S2 - CA - CK: S2 takes the trick as this is the only non-club (so in this case, trump) played <br/>
C6 - S2 - CA - D3: D3 takes the trick, as this is the highest numbered non-club played <br/>
C6 - S2 - H3 - D3: H3 takes the trick as 3 is the highest non-club played and Hearts are higher ranked than diamonds

### Round evaluation, scoring

If the bid is successful (same amount of tricks made in the play), you are awarded 10 points, plus the number of tricks taken times 2.
If you fail, you lose the difference between the bid and your tricks times 2.

**Examples**: <br/>
Bid 0, took 0 tricks: 10 pts <br/>
Bid 0, took 1 trick: -2 pts <br/>
Bid 3, took 3 tricks: 10 + 3*2 = 16 pts <br/>
Bid 3, took 1 trick: -2 * 2 = -4 pts

## Technology stack

TBC
