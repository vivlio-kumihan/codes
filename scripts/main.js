"use strict";

class SelectFourEvents {
  constructor() {
    this.currentYear = new Date().getFullYear();
    this._init();
  }

  _init() {
    const events = [
      { year: this.currentYear, month: 1 - 1, day: 1, evnentTitle: "マキハシャレイ", image: "" },
      { year: this.currentYear, month: 1 - 1, day: 2, evnentTitle: "釿（ちょうな）初め", image: "" },
      { year: this.currentYear, month: 2 - 1, day: 1, evnentTitle: "おかめ福節分会", image: "" },
      { year: this.currentYear, month: 3 - 1, day: 22, evnentTitle: "千本の釈迦念仏", image: "" },
      { year: this.currentYear, month: 6 - 1, day: 8, evnentTitle: "釈尊花祭", image: "" },
      { year: this.currentYear, month: 7 - 1, day: 9, evnentTitle: "初夏の風物詩 陶器供養会と陶器市", image: "" },
      { year: this.currentYear, month: 8 - 1, day: 8, evnentTitle: "六道参り 精霊むかえ", image: "" },
      { year: this.currentYear, month: 12 - 1, day: 7, evnentTitle: "京の師走の名物行事 成道会と大根だき", image: "" },
    ];

    // イベントの日付が過ぎている場合、yearを1年増やす
    for (const event of Object.values(events)) {
      const { year, month, day, ...items } = event;
      const eventDate = new Date(year, month, day);
      let nowDate = new Date();
      event.year = eventDate < nowDate ? event.year + 1 : event.year;
    }

    // 日付が一番若いイベントから4つを選んで配列に格納
    const sortedEvents = events.sort((a, b) => {
      const dateA = new Date(a.year, a.month, a.day);
      const dateB = new Date(b.year, b.month, b.day);
      return dateA - dateB;
    });

    // 最新の4つのイベントを返す。
    return sortedEvents.slice(0, 4);
  }
}

new SelectFourEvents();
