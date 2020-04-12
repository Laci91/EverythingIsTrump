import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { MatGridListModule } from '@angular/material/grid-list';

import { AppComponent } from './app.component';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    MatGridListModule,
    NoopAnimationsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
