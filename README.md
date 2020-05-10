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

The application has a 2-tier architecture, a server implemented in Python, and a GUI implemented in Angular

### Backend

The server is implemented in Python 3.7 (also compatible with similar version numbers, should be 3.4+)
Game interactions happen via websocket communication, using the Autobahn framework (version 20)
The server expects messages with JSON format, with one mandatory tag "function" which describes the intention of the message.
Each message type has different mandatory parameters (details are currently embedded into `server_factory.py`, 
but probably should be extracted into a separate class.
The server is deployed to an AWS EC2 instance.

#### Downloading and starting up the server on a Linux machine

Get the codebase, install the required libraries and start up a server on port 8765.

`git clone https://github.com/Laci91/EverythingIsTrump.git src`
`sudo apt-get install python3-pip (Skip is you have pip3 installed)`
`cd src/game`
`pip3 install -r requirements.txt`
`python3 server.py`

### Frontend

The frontend runs on Angular 7, using several components from the Angular Material UI framework as well as some
directives from FX Layout and the TableModule from Angular Bootstrap.

#### Serving the UI locally

This assumes you downloaded the codebase and running a server on localhost as described above.
These steps will run the UI on localhost:9000.

`cd src/eit-gui`
`npm install`
`ng serve --port 9000`

#### Build UI code

These steps will compile the source files into minified JS files, CSS files, card pictures and an index.htlm page.
These will be placed in the `src/eit-gui/dist/eit-gui` folder.

`cd src/eit-gui`
`npm install`
`ng build --prod`