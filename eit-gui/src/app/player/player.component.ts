import { Component, OnInit, Input, Output, EventEmitter, ElementRef, ViewChild, HostListener } from '@angular/core';
import { GameService } from '../game-service/game.service';

@Component({
  selector: 'player',
  templateUrl: './player.component.html',
  styleUrls: ['./player.component.scss']
})
export class PlayerComponent implements OnInit {

  @ViewChild('cardplayer')
  cardPlayerRef: ElementRef;

  @Input()
  seat: number;

  @Input()
  instructable: boolean;

  @Output()
  seatSelected = new EventEmitter<number>();

  seatingRequired: boolean = true;
  cardplayRequired: boolean = false;
  startingPlayer: boolean = false;
  active: boolean;
  bid: number | undefined;
  tricks: number | undefined;
  mainSuit?: string;
  name: string;
  visible: boolean = false;
  cards: string[];
  singleCandidateCard?: string;
  hiddenHandsInverted = false;

  @HostListener("document:keydown", ["$event"])
  handleEnter(event: KeyboardEvent) {
    if (event.key == "Enter" && this.singleCandidateCard) {
      this.playCard(this.singleCandidateCard);
    }
  }

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

      this.mainSuit = undefined;
      this.singleCandidateCard = undefined;
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
        this.cards = update.hand;
      } else {
        this.cards = new Array(update.hand.length);
        this.cards.fill("");
      }

      this.startingPlayer = update.startingPlayer == this.seat;
      this.tricks = undefined;
      this.bid = undefined;
      this.hiddenHandsInverted = false;
    });

    this.gameService.singleCardUpdate.subscribe(update => {
      if (this.seat in update) {
        this.cards = update[this.seat];
        this.hiddenHandsInverted = true;
        this.startingPlayer = 1 == this.seat;
      }
    });

    this.gameService.playUpdate.subscribe(update => {
      // Remove played card if it was played from this hand
      if ((update.seat == this.seat) && this.visible) {
        this.cards = this.cards.filter(item => item !== update.card);
        this.cardplayRequired = false;
      } else if (update.seat == this.seat) {
        this.cards.pop();
      }

      // Identify led suit and choose single play candidate if there is one
      if (this.mainSuit === undefined) {
        this.mainSuit = update.card.charAt(0)
        const cardsInMainSuit = this.cards.filter(c => c.charAt(0) == this.mainSuit);
        if (cardsInMainSuit.length === 1) {
          this.singleCandidateCard = cardsInMainSuit[0];
        }
      }
    });

    this.gameService.playTrigger.subscribe(update => {
      if (update) {
        this.cardplayRequired = true;
        if (this.cards.length == 1) {
          this.singleCandidateCard = this.cards[0];
        }
        setTimeout(() => this.cardPlayerRef.nativeElement.focus());
      }
    });
  }

  getImagePath(card: string) {
    if ((this.visible && !this.hiddenHandsInverted) || (!this.visible && this.hiddenHandsInverted)) {
      return "assets/cards/" + card[1] + card[0] + ".jpg";
    } else {
      return "assets/cards/back.jpg";
    }
  }

  playCard(card?: string) {
    if (this.instructable && this.cardplayRequired) {
      this.gameService.sendPlay(card);
    }
  }

  takeSeat() {
    if (this.name) {
      this.gameService.takeSeat(this.seat, this.name);
    }
  }

  getStyling() {
    return {
      'position': 'relative',
      'width.px': 100,
      'margin-right.px': -70
    }
  }

}
