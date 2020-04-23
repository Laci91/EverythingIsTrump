import { Component, OnInit } from '@angular/core';
import { GameService } from '../game-service/game.service';

@Component({
  selector: 'status-panel',
  templateUrl: './status-panel.component.html',
  styleUrls: ['./status-panel.component.scss']
})
export class StatusPanelComponent implements OnInit {

  statusMessages: string[] = [];

  constructor(private gameService: GameService) { }

  ngOnInit() {
    this.gameService.statusMessage.subscribe(update => {
      this.statusMessages = this.statusMessages.concat(update);
    })
  }

}
