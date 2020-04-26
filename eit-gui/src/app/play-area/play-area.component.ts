import { Component, OnInit } from '@angular/core';
import { GameService } from '../game-service/game.service';

@Component({
  selector: 'play-area',
  templateUrl: './play-area.component.html',
  styleUrls: ['./play-area.component.scss']
})
export class PlayAreaComponent implements OnInit {

  playedCard = {
    "1": "",
    "2": "",
    "3": "",
    "4": ""
  }

  nextCardWillClearArea = false;

  constructor(private gameService: GameService) { }

  ngOnInit() {
    // We don't want to clear it as soon as the last card is played, people wouldn't be able to see it.
    // The next card play will clear the area...
    this.gameService.trickUpdate.subscribe(update => {
      this.nextCardWillClearArea = true;
    });

    this.gameService.playUpdate.subscribe(update => {
      if (this.nextCardWillClearArea) {
        for (let seat in this.playedCard) {
          this.playedCard[seat] = "";
        }
        this.nextCardWillClearArea = false;
      }

      this.playedCard[update.seat] = update.card;
    });

    this.gameService.bidUpdate.subscribe(_ => {
      if (this.nextCardWillClearArea) {
        for (let seat in this.playedCard) {
          this.playedCard[seat] = "";
        }
        this.nextCardWillClearArea = false;
      }
    });
  }

  getPlayedCard(seat: number) {
    let card = this.playedCard[seat];
    if (card === "") {
      return "assets/cards/back.jpg";
    } else {
      return "assets/cards/" + card[1] + card[0] + ".jpg"
    }
  }

  isCardHidden(seat: number) {
    return this.playedCard[seat] === "";
  }

}
