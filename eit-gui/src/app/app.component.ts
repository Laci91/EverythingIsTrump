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
  player: number;
  activePlayer: number;
  biddingPanelEnabled: boolean;

  constructor(private gameService: GameService) {}

  ngOnInit() {
    this.gameService.biddingTrigger.subscribe(update => {
      if (update) {
        this.biddingPanelEnabled = true;
      }
    });

    this.gameService.bidUpdate.subscribe(update => {
      if (update.seat == this.player) {
        this.biddingPanelEnabled = false;
      }
    });

    this.gameService.activePlayer.subscribe(update => {
      this.activePlayer = update;
    });
  }

  setSeatOfActivePlayer(seat: number) {
    this.player = seat;
  }
}
