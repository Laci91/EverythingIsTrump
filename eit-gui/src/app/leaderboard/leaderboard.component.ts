import { Component, OnInit } from '@angular/core';
import { GameService } from '../game-service/game.service';

@Component({
  selector: 'leaderboard',
  templateUrl: './leaderboard.component.html',
  styleUrls: ['./leaderboard.component.scss']
})
export class LeaderboardComponent implements OnInit {

  displayedColumns = ["Round", "1", "2", "3", "4"];

  pointCounts: any[];
  lastRound: number = 0;

  constructor(private gameService: GameService) { }

  ngOnInit() {
    this.pointCounts = [{"round": 0, "scores": [0, 0, 0, 0]}];
    this.gameService.leaderboardUpdate.subscribe(update => {
        let newScores = [0, 0, 0, 0]
        if (!update.scores) {
          return;
        }
        update.scores.forEach(entry => {
          const playerNum = entry.playerNumber;
          const points = entry.score;
          newScores[playerNum - 1] = points;
        });
        this.pointCounts.unshift({"round": this.lastRound + 1, "scores": newScores});
        this.lastRound += 1;
    });
    
    this.gameService.newPlayer.subscribe(update => {
      this.displayedColumns[update.seat] = update.player;
    });

    this.gameService.seatingTrigger.subscribe(update => {
      for (let key in update) {
        this.displayedColumns[Number(key)] = update[key];
      }
    })
  }

}
