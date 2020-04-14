import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'bid-slider',
  templateUrl: './bid-slider.component.html',
  styleUrls: ['./bid-slider.component.scss']
})
export class BidSliderComponent {

  @Input()
  numberOfCards: number

  @Output()
  sendBid = new EventEmitter();

  proposedBid: number = 0

  constructor() { }

  makeBid() {
    console.log(this.proposedBid);
    this.sendBid.emit(this.proposedBid);
  }

}
