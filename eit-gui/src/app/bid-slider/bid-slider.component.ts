import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { MatSlider } from '@angular/material';
import { GameService } from '../game-service/game.service';

@Component({
  selector: 'bid-slider',
  templateUrl: './bid-slider.component.html',
  styleUrls: ['./bid-slider.component.scss']
})
export class BidSliderComponent implements OnInit {

  @ViewChild(MatSlider)
  sliderElement: MatSlider;
  numberOfCards: number;
  proposedBid: number = 0;

  constructor(private gameService: GameService) { }

  ngOnInit() {
    this.gameService.biddingTrigger.subscribe(_ => {
      console.log(this.sliderElement);
      setTimeout(() => this.sliderElement.focus());
    });

    this.gameService.handUpdate.subscribe(update => {
      this.numberOfCards = update.length;
    });

    this.gameService.singleCardUpdate.subscribe(_ => {
      this.numberOfCards = 1;
    });
  }

  onKeyDown(event) {
    const key = Number(event.key);
    if (key >= 0 && key <= this.numberOfCards) {
      this.proposedBid = key;
    }
  }

  makeBid() {
    this.gameService.sendBid(this.proposedBid);
  }

}
