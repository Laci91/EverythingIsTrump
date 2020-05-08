import { Component, OnInit } from '@angular/core';
import { GameService } from '../game-service/game.service';

@Component({
  selector: 'warning',
  templateUrl: './warning.component.html',
  styleUrls: ['./warning.component.scss']
})
export class WarningComponent implements OnInit {

  bids: number[] = [];
  numberOfCards: number = 0;
  excludedBid: number;
  overUnder: number;
  mainSuit: string;

  constructor(private gameService: GameService) { }

  ngOnInit() {
    this.gameService.bidUpdate.subscribe(update => {
      console.log(`Got an update, ${update.bid}`);
      this.bids = this.bids.concat(update.bid);
      if (this.bids.length == 3) {
        this.excludedBid = this.numberOfCards - this.bids.reduce((acc, curr) => acc + curr, 0);
        console.log(`Processed 3 bids, excluded is ${this.excludedBid}`)
      } else if (this.bids.length == 4) {
        this.overUnder = this.numberOfCards - this.bids.reduce((acc, curr) => acc + curr, 0);
        console.log(`Processed 4 bids, over/under is ${this.overUnder}`)
      } else {
        this.excludedBid = undefined;
      }
    });

    this.gameService.singleCardUpdate.subscribe(_ => {
      this.numberOfCards = 1;
      this.bids = [];
      this.excludedBid = undefined;
      this.overUnder = undefined;
    });

    this.gameService.handUpdate.subscribe(update => {
      this.numberOfCards = update.length
      this.bids = [];
      this.excludedBid = undefined;
      this.overUnder = undefined;
    });

    this.gameService.playUpdate.subscribe(update => {
      console.log(update.card + "; " + update.card.charAt(0));
      if (this.mainSuit === undefined) {
        switch(update.card.charAt(0)) {
          case "S": 
            this.mainSuit = "Spades";
            console.log("Sp");
            break;
          case "H":
            this.mainSuit = "Hearts";
            console.log("H");
            break;
          case "D":
            this.mainSuit = "Diamonds";
            console.log("D");
            break;
          case "C":
            this.mainSuit = "Clubs";
            console.log("Cl");
            break;
          default:
            break;
        }
      }
    });

    this.gameService.trickUpdate.subscribe(_ => {
      this.mainSuit = undefined;
    });
  }

  getOverUnderText() {
    return !this.overUnder ? "" : Math.abs(this.overUnder) + " " + (this.overUnder > 0 ? "Under" : "Over");
  }

}