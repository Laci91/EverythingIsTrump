import { Component, OnInit, ViewChild } from '@angular/core';
import { GameService } from '../game-service/game.service';
import { ScrollToBottomDirective } from '../scroll-to-bottom.directive';

@Component({
  selector: 'status-panel',
  templateUrl: './status-panel.component.html',
  styleUrls: ['./status-panel.component.scss']
})
export class StatusPanelComponent implements OnInit {

  @ViewChild(ScrollToBottomDirective)
  scroll: ScrollToBottomDirective;

  statusMessages: string[] = [];

  constructor(private gameService: GameService) { }

  ngOnInit() {
    this.gameService.statusMessage.subscribe(update => {
      this.statusMessages = this.statusMessages.concat(update);
      this.scroll.scrollToBottom();
    });
  }

}
