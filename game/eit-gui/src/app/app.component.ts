import { Component, OnInit } from '@angular/core';
import { GameService } from './game-service/game.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'eit-gui';
  statusInfo: string;
  numOfCards: number; // TODO: Move to bid-lider
  seatOfActivePlayer: number;
  biddingPanelEnabled: boolean;
  cardplayPanelEnabled: boolean;

  constructor(private gameService: GameService) {}

  ngOnInit() {
    this.gameService.biddingTrigger.subscribe(update => {
      if (update) {
        this.biddingPanelEnabled = true;
      }
    });

    this.gameService.playTrigger.subscribe(update => {
      if (update) {
        this.cardplayPanelEnabled = true;
      }
    });

    this.gameService.bidUpdate.subscribe(update => {
      if (update.seat == this.seatOfActivePlayer) {
        this.biddingPanelEnabled = false;
      }
    });

    this.gameService.playUpdate.subscribe(update => {
      if (update.seat == this.seatOfActivePlayer) {
        this.cardplayPanelEnabled = false;
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
    this.statusInfo = "You made this bid: " + bid
    this.gameService.sendBid(bid);
  }

  setSeatOfActivePlayer(seat: number) {
    this.seatOfActivePlayer = seat;
  }
}
