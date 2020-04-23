import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatSliderModule } from '@angular/material/slider';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { MatInputModule } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card';
import { FlexLayoutModule } from '@angular/flex-layout';
import { TableModule } from 'angular-bootstrap-md';

import { AppComponent } from './app.component';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { BidSliderComponent } from './bid-slider/bid-slider.component';
import { LeaderboardComponent } from './leaderboard/leaderboard.component';
import { GameService } from './game-service/game.service';
import { PlayerComponent } from './player/player.component';
import { PlayAreaComponent } from './play-area/play-area.component';
import { StatusPanelComponent } from './status-panel/status-panel.component';

@NgModule({
  declarations: [
    AppComponent,
    BidSliderComponent,
    LeaderboardComponent,
    PlayerComponent,
    PlayAreaComponent,
    StatusPanelComponent
  ],
  imports: [
    BrowserModule,
    MatGridListModule,
    MatSliderModule,
    MatTableModule,
    NoopAnimationsModule,
    MatButtonModule,
    MatInputModule,
    FlexLayoutModule,
    TableModule,
    MatCardModule
  ],
  providers: [GameService],
  bootstrap: [AppComponent]
})
export class AppModule { }
