import { Injectable } from '@angular/core';
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
        this.updateStatus("Leaderboard has been refreshed");
      } else if (incoming["function"] == "bid-info") {
        const seat = <number> incoming["seat"];
        const bid = <number> incoming["bid"];
        this.updateBid(seat, bid);
        this.updateStatus(`Player #${seat} bid ${bid}`);
      } else if (incoming["function"] == "play-info") {
        const seat = <number> incoming["seat"];
        const card = <string> incoming["card"];
        this.updatePlay(seat, card);
        this.updateStatus(`Player #${seat} played ${card}`);
      } else if (incoming["function"] == "deal") {
        if (incoming["card-on-forehead"]) {
          const hands = <any[]> incoming["hand"];
          this.updateSingleCards(hands);
        } else {
          const hand = <string[]> incoming["hand"];
          this.updateHand(hand);
        }
        this.updateStatus("A new hand has begun, you received new cards");
      } else if (incoming["function"] == "trick") {
        const taker = <number> incoming["taker"];
        const highCard = incoming["high-card"];
        this.updateTrick(taker);
        this.updateStatus(`Player #${taker} took the trick with ${highCard}`);
      } else if (incoming["function"] == "next-player") {
        const seat = <number> incoming["seat"];
        this.updateActivePlayer(seat);
        this.updateStatus(`It's player #${seat}'s turn`);
      } else if (incoming["function"] == "bid-trigger") {
        this.triggerBiddingPanel();
        this.updateStatus("It's your turn to bid!");
      } else if (incoming["function"] == "play-trigger") {
        this.triggerCardplayPanel();
        this.updateStatus("It's your turn to play a card!");
      } else if (incoming["function"] == "seat-trigger") {
        const players = <any[]> incoming["players"];
        this.triggerSeating(players);
        this.updateStatus("Please take a seat");
      } else if (incoming["function"] == "seat") {
        const success = incoming["status"] === "success";
        const seat = <number> incoming["seat"];
        if (success) {
          this.updateSeating(seat);
          this.updateStatus("Seating is successful, waiting for 4 players to join");
        } else {
          this.updateStatus("Something went wrong with seating");
        }
      } else if (incoming["function"] == "new-player") {
        const seat = <number> incoming["seat"];
        const name = <string> incoming["name"];
        this.addNewPlayer(seat, name);
        this.updateStatus(`A new player, ${name}, took seat #${seat}`);
      } else if (incoming["function"] == "lost-player") {
        const seat = <number> incoming["seat"];
        this.removeLostPlayer(seat);
        this.updateStatus(`The player in seat #${seat} left the game`);
      } else if (incoming["function"] == "error") {
        const msg = incoming["message"];
        this.updateStatus(msg);
      } else if (incoming["function"] == "round") {
        const updates = incoming["updates"];
        this.sendRoundUpdates(updates);
      }
    });
  }

  sendRoundUpdates(updates: any[]) {
    updates.forEach(update => {
      const player = <number> update["player"];
      const bid =  <number> update["bid"];
      const tricks = <number> update["tricks"];
      const points = <number> update["points"];
      this.updateStatus(`Player #${player} bid ${bid}, made ${tricks} tricks, got ${points} points`);
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

  updateStatus(message: string) {
    this.statusMessageBehaviorSubject.next(message);
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
