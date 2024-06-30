"use strict";

class SetSetsubun {
  constructor() {
    this._init();
  }

  _init() {
    // 2021年から45年分の年を配列にする。
    const years = [...Array(45)].map((_, idx) => 2021 + idx);
    // 節分の日付が2日になる年を配列にする。
    const feb2 = years.filter((_, idx) => idx % 4 === 0);
    // まとめ作業
    this.yearsObj = years.reduce((acc, year) => {
      if (feb2.includes(year) || year === 2058) {
        acc.push({ year: year, month: 1, day: 2 });
      } else {
        acc.push({ year: year, month: 1, day: 3 });
      }
      return acc;
    }, []);
  }
}