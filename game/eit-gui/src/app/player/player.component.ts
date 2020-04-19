import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { GameService } from '../game-service/game.service';

@Component({
  selector: 'player',
  templateUrl: './player.component.html',
  styleUrls: ['./player.component.scss']
})
export class PlayerComponent implements OnInit {

  @Input()
  seat: number;

  @Input()
  instructable: boolean;

  @Output()
  seatSelected = new EventEmitter<number>();

  seatingRequired: boolean = true;
  cardplayRequired: boolean = false;
  active: boolean;
  bid: number | undefined;
  tricks: number | undefined;
  name: string;
  visible: boolean = false;
  cards: string[];
  hiddenHandsInverted = false;

  constructor(private gameService: GameService) { }

  ngOnInit() {
    this.gameService.bidUpdate.subscribe(update => {
      if (update.seat == this.seat) {
        this.bid = update.bid;
      }
    });

    this.gameService.trickUpdate.subscribe(update => {
      if (this.tricks === undefined) {
        this.tricks = 0;
      }
      if (update == this.seat) {
        this.tricks += 1;
      }
    });

    this.gameService.activePlayer.subscribe(update => {
      if (update == this.seat) {
        this.active = true;
      } else if (this.active) {
        this.active = false;
      }
    });

    this.gameService.successfulSeating.subscribe(update => {
      if (update == this.seat) {
        this.visible = true;
        this.instructable = true;
        this.seatSelected.emit(this.seat);
      } else {
        this.visible = false;
        this.instructable = false;
      }

      // -1 is the default value for these BehaviorSubjects
      // I'm pretty sure there is a better solution for this
      if (update !== -1) {
        this.seatingRequired = false;
      }
    });

    this.gameService.seatingTrigger.subscribe(update => {
      if (this.seat in update) {
        this.name = update[this.seat];        
        this.seatingRequired = false;
      }
    });

    this.gameService.newPlayer.subscribe(update => {
      if (update.seat == this.seat) {
        this.name = update.player;
        this.seatingRequired = false;
      }
    });

    this.gameService.lostPlayer.subscribe(update => {
      if (update == this.seat) {
        this.name = "";
        this.seatingRequired = true;
      }
    });

    this.gameService.handUpdate.subscribe(update => {
      if (this.instructable) {
        this.cards = update;
      } else {
        this.cards = new Array(update.length);
        this.cards.fill("");
      }
      this.tricks = undefined;
      this.bid = undefined;
      this.hiddenHandsInverted = false;
    });

    this.gameService.singleCardUpdate.subscribe(update => {
      if (this.seat in update) {
        this.cards = update[this.seat];
        this.hiddenHandsInverted = true;
      }
    });

    this.gameService.playUpdate.subscribe(update => {
      if ((update.seat == this.seat) && this.visible) {
        this.cards = this.cards.filter(item => item !== update.card);
        this.cardplayRequired = false;
      } else if (update.seat == this.seat) {
        this.cards.pop();
      }
    });

    this.gameService.playTrigger.subscribe(update => {
      if (update) {
        this.cardplayRequired = true;
      }
    })
  }

  getImagePath(card: string) {
    if ((this.visible && !this.hiddenHandsInverted) || (!this.visible && this.hiddenHandsInverted)) {
      return "assets/cards/" + card[1] + card[0] + ".jpg";
    } else {
      return "assets/cards/back.jpg";
    }
  }

  playCard(card: string) {
    if (this.instructable && this.cardplayRequired) {
      this.gameService.sendPlay(card);
    }
  }

  takeSeat() {
    this.gameService.takeSeat(this.seat, this.name);
  }

  getStyling(index: number) {
    return {
      'position': 'relative',
      'width.px': 75,
      'margin-right.px': -50
    }
  }

}
