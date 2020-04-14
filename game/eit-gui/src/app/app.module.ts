import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatSliderModule } from '@angular/material/slider';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { MatInputModule } from '@angular/material/input';
import { FlexLayoutModule } from '@angular/flex-layout';

import { AppComponent } from './app.component';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { BidSliderComponent } from './bid-slider/bid-slider.component';
import { LeaderboardComponent } from './leaderboard/leaderboard.component';
import { GameService } from './game-service/game.service';
import { PlayerComponent } from './player/player.component';
import { PlayAreaComponent } from './play-area/play-area.component';

@NgModule({
  declarations: [
    AppComponent,
    BidSliderComponent,
    LeaderboardComponent,
    PlayerComponent,
    PlayAreaComponent
  ],
  imports: [
    BrowserModule,
    MatGridListModule,
    MatSliderModule,
    MatTableModule,
    NoopAnimationsModule,
    MatButtonModule,
    MatInputModule,
    FlexLayoutModule
  ],
  providers: [GameService],
  bootstrap: [AppComponent]
})
export class AppModule { }
