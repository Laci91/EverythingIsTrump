import { Injectable, OnInit } from '@angular/core';
import { Observable, BehaviorSubject } from 'rxjs';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { LeaderboardUpdate, LeaderboardEntry } from '../model/leaderboard-update';
import { BidUpdate } from '../model/bid-update';
import { PlayUpdate } from '../model/play-update';
import { NewPlayerUpdate } from '../model/new-player';

@Injectable({
  providedIn: 'root'
})
export class GameService {
  myWebSocket: WebSocketSubject<any> = webSocket('ws://localhost:8765');

  leaderboardBehaviorSubject = new BehaviorSubject<LeaderboardUpdate>(new LeaderboardUpdate());
  leaderboardUpdate: Observable<LeaderboardUpdate> = this.leaderboardBehaviorSubject.asObservable();

  statusMessageBehaviorSubject = new BehaviorSubject<string>("");
  statusMessage: Observable<string> = this.statusMessageBehaviorSubject.asObservable();

  bidUpdateBehaviorSubject = new BehaviorSubject<BidUpdate>(new BidUpdate());
  bidUpdate: Observable<BidUpdate> = this.bidUpdateBehaviorSubject.asObservable();

  playUpdateBehaviorSubject = new BehaviorSubject<PlayUpdate>(new PlayUpdate());
  playUpdate: Observable<PlayUpdate> = this.playUpdateBehaviorSubject.asObservable();

  trickUpdateBehaviorSubject = new BehaviorSubject<number>(-1);
  trickUpdate: Observable<number> = this.trickUpdateBehaviorSubject.asObservable();

  activePlayerBehaviorSubject = new BehaviorSubject<number>(-1);
  activePlayer: Observable<number> = this.activePlayerBehaviorSubject.asObservable();

  successfulSeatingBehaviorSubject = new BehaviorSubject<number>(-1);
  successfulSeating: Observable<number> = this.successfulSeatingBehaviorSubject.asObservable();

  handUpdateBehaviorSubject = new BehaviorSubject<string[]>([]);
  handUpdate: Observable<string[]> = this.handUpdateBehaviorSubject.asObservable();

  singleCardUpdateBehaviorSubject = new BehaviorSubject<any[]>([]);
  singleCardUpdate: Observable<any[]> = this.singleCardUpdateBehaviorSubject.asObservable();

  // This feels wrong
  biddingTriggerBehaviorSubject = new BehaviorSubject<boolean>(false);
  biddingTrigger: Observable<boolean> = this.biddingTriggerBehaviorSubject.asObservable();

  playTriggerBehaviorSubject = new BehaviorSubject<boolean>(false);
  playTrigger: Observable<boolean> = this.playTriggerBehaviorSubject.asObservable();
  // End of feeling wrong

  seatingTriggerBehaviorSubject = new BehaviorSubject<any[]>([]);
  seatingTrigger: Observable<any[]> = this.seatingTriggerBehaviorSubject.asObservable();

  newPlayerBehaviorSubject = new BehaviorSubject<NewPlayerUpdate>(new NewPlayerUpdate());
  newPlayer: Observable<NewPlayerUpdate> = this.newPlayerBehaviorSubject.asObservable();

  lostPlayerBehaviorSubject = new BehaviorSubject<number>(-1);
  lostPlayer: Observable<number> = this.lostPlayerBehaviorSubject.asObservable();

  constructor() { 
    this.init()
  }

  init() {
    this.myWebSocket.subscribe(incoming => {
      console.log(incoming);
      if (incoming["function"] === "standings") {
        let standings = <any[]> incoming["standings"];
        this.updateLeaderboard(standings);
      } else if (incoming["function"] == "bid-info") {
        const seat = <number> incoming["seat"];
        const bid = <number> incoming["bid"];
        this.updateBid(seat, bid);
      } else if (incoming["function"] == "play-info") {
        const seat = <number> incoming["seat"];
        const card = <string> incoming["card"];
        this.updatePlay(seat, card);
      } else if (incoming["function"] == "deal") {
        if (incoming["card-on-forehead"]) {
          const hands = <any[]> incoming["hand"];
          this.updateSingleCards(hands);
        } else {
          const hand = <string[]> incoming["hand"];
          this.updateHand(hand);
        }
      } else if (incoming["function"] == "trick") {
        const taker = <number> incoming["taker"];
        this.updateTrick(taker);
      } else if (incoming["function"] == "next-player") {
        const seat = <number> incoming["seat"];
        this.updateActivePlayer(seat);
      } else if (incoming["function"] == "bid-trigger") {
        this.triggerBiddingPanel();
      } else if (incoming["function"] == "play-trigger") {
        this.triggerCardplayPanel();
      } else if (incoming["function"] == "seat-trigger") {
        const players = <any[]> incoming["players"];
        this.triggerSeating(players);
      } else if (incoming["function"] == "seat") {
        const success = incoming["status"] === "success";
        const seat = <number> incoming["seat"];
        if (success) {
          this.updateSeating(seat);
        }
      } else if (incoming["function"] == "new-player") {
        const seat = <number> incoming["seat"];
        const name = <string> incoming["name"];
        this.addNewPlayer(seat, name);
      } else if (incoming["function"] == "lost-player") {
        const seat = <number> incoming["seat"]
        this.removeLostPlayer(seat);
      }
    });
  }

  updateLeaderboard(standings: any[]) {
    let update = new LeaderboardUpdate();
    let entries: LeaderboardEntry[] = [];
    standings.forEach(element => {
      let entry = new LeaderboardEntry();
      entry.playerNumber = Number(element["player"]);
      entry.score = Number(element["points"]);
      entries.push(entry);
    });
    update.scores = entries;
    this.leaderboardBehaviorSubject.next(update);
  }

  updateBid(seat: number, bid: number) {
    let update = new BidUpdate();
    update.seat = seat;
    update.bid = bid;
    this.bidUpdateBehaviorSubject.next(update);
  }

  updatePlay(seat: number, card: string) {
    let update = new PlayUpdate();
    update.seat = seat;
    update.card = card;
    this.playUpdateBehaviorSubject.next(update);
  }

  updateTrick(taker: number) {
    this.trickUpdateBehaviorSubject.next(taker);
  }

  updateActivePlayer(seat: number) {
    this.activePlayerBehaviorSubject.next(seat);
  }

  updateSeating(seat: number) {
    this.successfulSeatingBehaviorSubject.next(seat);
  }

  updateHand(hand: string[]) {
    this.handUpdateBehaviorSubject.next(hand);
  }

  updateSingleCards(hands: any[]) {
    this.singleCardUpdateBehaviorSubject.next(hands);
  }

  triggerBiddingPanel() {
    this.biddingTriggerBehaviorSubject.next(true);
  }

  triggerCardplayPanel() {
    this.playTriggerBehaviorSubject.next(true);
  }

  triggerSeating(players: any[]) {
    this.seatingTriggerBehaviorSubject.next(players);
  }

  addNewPlayer(seat: number, name: string) {
    let update = new NewPlayerUpdate();
    update.seat = seat;
    update.player = name;
    this.newPlayerBehaviorSubject.next(update);
  }

  removeLostPlayer(seat: number) {
    this.lostPlayerBehaviorSubject.next(seat);
  }

  sendStatusMessage(message: string) {
    this.statusMessageBehaviorSubject.next(message);
  }

  sendBid(bid: number) {
    const message = {"function": "bid", "bid": bid};
    this.myWebSocket.next(message);
  }

  sendPlay(card: string) {
    const message = {"function": "play", "card": card};
    this.myWebSocket.next(message);
  }

  takeSeat(seat: number, name: string) {
    const message = {"function": "seat", "name": name, "seat": seat};
    this.myWebSocket.next(message);
  }
}
