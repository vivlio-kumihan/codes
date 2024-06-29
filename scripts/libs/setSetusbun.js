"use strict";

class SetSetusbun {
  constructor() {
    this._init();
  }

  _init() {
    const years = [...Array(45)].map((_, idx) => 2021 + idx);
    const feb2 = years.filter((_, idx) => idx % 4 === 0);
    
    const yearsObj = years.reduce((acc, year) => {
      if (feb2.includes(year) || year === 2058) {
        acc.push({ year: year, month: 1, day: 2 });
      } else {
        acc.push({ year: year, month: 1, day: 3 });
      }
      return acc;
    }, []);
    console.log(yearsObj);
  }
}

new SetSetusbun();