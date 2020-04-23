import { Component, OnInit } from '@angular/core';
import { GameService } from './game-service/game.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'eit-gui';
  numOfCards: number; // TODO: Move to bid-slider
  seatOfActivePlayer: number;
  biddingPanelEnabled: boolean;

  constructor(private gameService: GameService) {}

  ngOnInit() {
    this.gameService.biddingTrigger.subscribe(update => {
      if (update) {
        this.biddingPanelEnabled = true;
      }
    });

    this.gameService.bidUpdate.subscribe(update => {
      if (update.seat == this.seatOfActivePlayer) {
        this.biddingPanelEnabled = false;
      }
    });

    this.gameService.handUpdate.subscribe(update => {
      this.numOfCards = update.length;
    });

    this.gameService.singleCardUpdate.subscribe(_ => {
      this.numOfCards = 1;
    })
  }

  bidHandler(bid: number) {
    this.gameService.sendBid(bid);
  }

  setSeatOfActivePlayer(seat: number) {
    this.seatOfActivePlayer = seat;
  }
}