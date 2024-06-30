"use strict";

class Main {
  constructor() {
    this.setSetsubunIns = new SetSetsubun();
    new SelectFourEvents(this.setSetsubunIns);
  }
}

new Main();