"use strict";

class SelectFourEvents {
  constructor(setSetsubunIns) {
    this.currentYear = new Date().getFullYear();
    this.nowDate = new Date(2024, 1, 1);
    this.setSetsubunIns = setSetsubunIns;
    this.events = [
      { year: this.currentYear, month: 0, agendaDay: [1], evnentTitle: "マキハシャレイ", image: "" },
      { year: this.currentYear, month: 0, agendaDay: [2], evnentTitle: "釿（ちょうな）初め", image: "" },
      { year: this.currentYear, month: 1, agendaDay: [this._setStsubunDay()], evnentTitle: "おかめ福節分会", image: "" },
      { year: this.currentYear, month: 2, agendaDay: [22], evnentTitle: "千本の釈迦念仏", image: "" },
      { year: this.currentYear, month: 5, agendaDay: [8], evnentTitle: "釈尊花祭", image: "" },
      { year: this.currentYear, month: 6, agendaDay: [9, 10, 11, 12], evnentTitle: "初夏の風物詩 陶器供養会と陶器市", image: "" },
      { year: this.currentYear, month: 7, agendaDay: [8, 9, 10, 11, 12, 13, 14, 15, 16], evnentTitle: "六道参り 精霊むかえ", image: "" },
      { year: this.currentYear, month: 11, agendaDay: [7, 8], evnentTitle: "京の師走の名物行事 成道会と大根だき", image: "" },
    ];
    this._init();
  }

  _init() {
    console.log(this.setSetsubunIns.yearsObj);
    // イベントの日付が過ぎている場合、yearを1年増やす
    for (const event of this.events) {
      const { year, month, agendaDay } = event;
      // 定型処理
      function incrementYearAndResetDay(event) {
        event.year += 1;
        event.agendaDay = month === 1 ? 2 : event.agendaDay[0];
      };

      if (month === this.nowDate.getMonth() && agendaDay.includes(this.nowDate.getDate())) {
        let getIndex = agendaDay.indexOf(this.nowDate.getDate());
        getIndex + 1 < agendaDay.length
          ? event.agendaDay = agendaDay[getIndex + 1]
          : incrementYearAndResetDay(event);
      } else {
        const futureDays = agendaDay.filter(day => new Date(year, month, day) >= this.nowDate);
        futureDays.length > 0
          ? event.agendaDay = futureDays[0]
          : incrementYearAndResetDay(event);
      }
    }    

    // 日付が一番若いイベントから4つを選んで配列に格納
    const sortedEvents = this.events.sort((a, b) => {
      const dateA = new Date(a.year, a.month, a.agendaDay);
      const dateB = new Date(b.year, b.month, b.agendaDay);
      return dateA - dateB;
    });
    console.log(sortedEvents);
    console.log(sortedEvents.slice(0, 4));
    return sortedEvents.slice(0, 4);
  }

  _setStsubunDay() {
    for (const setsubun of this.setSetsubunIns.yearsObj) {
      if (setsubun.year === this.currentYear) {
        return setsubun.day;
      }
    }
  };  
}