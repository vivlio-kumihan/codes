"use strict";

class SelectFourEvents {
  constructor(setSetsubunIns) {
    this.currentYear = new Date().getFullYear();
    this.nowDate = new Date();
    this.setSetsubunIns = setSetsubunIns;
    this.events = [
      { year: this.currentYear, month: 0, agendaDay: [1],
        title: "巻藁射礼",
        catch: "弓道の神髄に触れる",
        description: "巻藁射礼（まきわらじゃれい）は、弓道の鍛錬と儀礼の一環として行われる儀式です。巻藁は、鍛錬用の藁束で作られた的のことを指します。この儀式は、弓道における八つの基本動作（足踏み、胴作り、弓構え、打起し、引分け、会、離れ、残心）の精緻な動作を通して、射手の技術と精神の統一を追求します​。その歴史は戦国時代や江戸時代に遡り、戦国時代は戦闘技術として発展し、江戸時代には精神修養と美的表現を重視する武道として進化しました​​。",
        image: "./images/event_makiwara.jpg" 
      },
      { year: this.currentYear, month: 0, agendaDay: [2],
        title: "釿初め",
        catch: "匠の安全を祈る",
        description: "番匠（ばんしょう）と呼ばれる御所出入りの宮大工たちが、正月に一年の安全を祈願する儀式です。京都市の無形民俗文化財に指定されている京木遣（きやり）音頭が流れるなか、古式の衣裳を身にまとった番匠保存会の会員によって厳粛に執り行われます。江戸時代には、「聚楽」「川東」「六条」「城下」などの大工組が、それぞれ特色ある木遣音頭を伝えていましたが、現在では二条城界隈の「城下」地域の大工衆を中心とした番匠保存会が、その保存と継承に努めています。2020年までは広隆寺で行われていましたが、2022年からは千本釈迦堂で釿始めが行われています。",
        image: "./images/event_chouna-hajime@0.25x.jpg" 
      },
      { year: this.currentYear, month: 1, agendaDay: [this._setStsubunDay()],
        title: "おかめ福節分会",
        catch: "厄除け鬼追いと福豆まきの伝統行事",
        description: "当山本堂建立について内助の功のあった棟梁、長井飛騨守高次の妻「阿亀（おかめ）」にちなむもので、当山境内にのこる「おかめ塚」と共に780年前より当寺に伝承されてきたものです。江戸時代末期に中絶、昭和26年（1951）からの本堂解体修理、昭和30年（1955）完成を記念して復活し今日に至ります。「おかめ」に由来するところから当日、年男は（婦人も行事に参加）男女共おかめの装束をして、おかめの貞淑と福徳円満、御多福招来等の祈願を受け、1年間の厄除けをするのが古くからのならわしになっています。近年、年男はそれぞれおかめの面をつけ、おかめの袈裟をかけて本堂宝前に於いて加持を受け、法要終了後、古式厄除鬼追いの儀、最後に一斉に福豆まきがおこなわれます。又、法要に先だって木遣音頭の奉納があります。",
        image: "./images/event_setsubune@0.25x.jpg" 
      },
      { year: this.currentYear, month: 2, agendaDay: [22],
        title: "千本の釈迦念仏",
        catch: "一語一語に込められた祈りを共に",
        description: "当山第二世如輪上人によってはじめられ（如輪入寂、文永8年［1271］）約750年前から当山に伝えられてきた法要で、お釈迦さまの涅槃の日（旧暦2月15日）に釈迦の最後の遺教経をわかり易く一語一語訓読みにて大原声明千本式によって律づけで奉詠（お唱え）するところから名付けられたものです。お経の終わりに「南無釈迦牟尼仏」と本尊お釈迦様の名号を初重、二重、三重の古律によって唱えられる念佛です。この行事は、兼好法師の『徒然草』にも記され、当時は多くの女官の参詣（聴聞）の様子がうかがわれます。毎年お釈迦さまの遺徳をしのんで非常にありがたい又、独特のお念仏でもあり、多くの信徒の参詣があります。",
        image: "./images/event_shaka-nembutsu@0.25x.jpg" 
      },
      { year: this.currentYear, month: 5, agendaDay: [8],
        title: "釈尊花祭",
        catch: "甘茶をかけてお釈迦様の誕生祝い",
        description: "正式名称は灌仏会（かんぶつえ）と呼ぶこのお祭りは、お釈迦様の誕生をお祝いし「子どもの身体健全・所願成就」を祈る仏教行事です。当寺では毎年5月8日に、花御堂と呼ばれる誕生仏（釈迦像）を囲った小さなお堂を安置して、参拝の方々には誕生仏に甘茶をかけてお祝していただきます。",
        image: "./images/event_hana-matsuri.jpg" 
      },
      { year: this.currentYear, month: 6, agendaDay: [9, 10, 11, 12],
        title: "陶器供養会と陶器市",
        catch: "初夏の風物詩–陶器に日ごろの感謝をこめる",
        description: "当山、本尊釈迦如来の方便化身とする地天尊を勧進し、日常生活に欠くことの出来ない瀬戸物の類を祀り感謝の誠を捧げ、家内安全・健康増進を祈り、併せて陶器業界発展のための祈願法要をおこないます。期間中は日没頃まで境内一帯で陶器市が開催され、境内いっぱいに各地からの陶器が並んで終日にぎわいます。10日には本堂で陶器への感謝と業界の発展を祈る法要をおこないます。",
        image: "./images/event_touki-iti@0.25x.jpg" 
      },
      { year: this.currentYear, month: 7, agendaDay: [8, 9, 10, 11, 12, 13, 14, 15, 16],
        title: "六道参り精霊むかえ",
        catch: "全国唯一、六道全ての生命や存在の受容と救済",
        description: "当山に安置されている六観音菩薩像は、六道信仰にもとづいて造立された聖観音、千手観音、馬頭観音、十一面観音、准胝観音、如意輪観音の六躯で、生命の転生の六つの世界である六道（地獄道、餓鬼道、畜生道、修羅道、人間道、天道）において、仏の智慧や力のあらわれである観音様により、迷えるご先祖・縁者のすべての精霊をお迎えして供養を施し、御仏の救いの力を功徳によってその滅罪追福を祈る行事です。精霊迎えは8月8～12日、精霊送り8月16日で執り行います。尚、期間中（8日〜16日）本尊釈迦如来像（秘仏）も御開帳となります。",
        image: "./images/event_rokudou-mairi@0.25x.jpg" 
      },
      { year: this.currentYear, month: 11, agendaDay: [7, 8],
        title: "成道会と大根だき",
        catch: "無病息災を願い、あつあつの大根をいただく",
        description: "当山第三世慈禅上人によってはじめられ、お釈迦さま「さとりの日」を慶讃して毎年12月7日と8日において盛大、かつ荘厳な「成道会」を営んでおいでになりました。お釈迦さまはさとりの修行中、悪魔、諸鬼神、羅刹等の妨害と悪魔の誘惑に屈せず、12月8日暁天の明星出現と同時に遂に「おさとり」を開かれた偉大なる行果にあやかるため、上人は法要を修するに際し、丸い大根4本をたて半分に切って8箇として、それぞれの切り口の半面に釈迦の種子（梵字）を書き大壇の上にお供えして、法を修して参詣者への「悪魔除け」とされました。上人はさらにこの悪魔除けの大根を他の大根とともに炊き上げ、参詣者に供養されたのが「大根だき」のはじめといわれています。この行事は代々続けられ、江戸中期頃、弘法大師により伝えられる加持法により「中風、諸病除け」の祈祷会とともに修したるところ「中風封じ、大根だき」の風習が盛んになり、江戸末期頃まで続けられました。近年「中風、悪病」を除かんがため、又健康増進を願う信徒のあつい信心によって復活し今日に至っています。大根一本一本に梵字をしるして「中風、諸病除け、健康増進」の祈祷法要を厳修し、大根を切り味付けのため煮込んで7日、8日の両日参詣者に授与しております。",
        image: "./images/event_daikon-daki@0.25x.jpg" 
      },
    ];
    this._init();
  }

  _init() {
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
    console.log(sortedEvents.slice(0, 4));
    this.selectEvents = sortedEvents.slice(0, 4);
    this._renderEvents();
  }

  _renderEvents() {
    const eventList = document.querySelector(".latest-event-schedule");
    eventList.innerHTML = "";
    this.selectEvents.forEach(event => {
      const listItem = document.createElement("li.event");
      const truncatedDescription = event.description.length > 75 
        ? event.description.substring(0, 75) + '...' 
        : event.description;
      listItem.innerHTML = `
        <div class="event__image"><img src="${ event.image }"></div>
        <div class="event__date">${ event.year }年${ event.month + 1 }月${ event.agendaDay }日</div>
        <div class="event__title">${ event.title }</div>
        <div class="event__catch">${ event.catch }</div>
        <div class="event__description">${ truncatedDescription }</div>      
      `;
      eventList.appendChild(listItem);
    })
  }

  _setStsubunDay() {
    for (const setsubun of this.setSetsubunIns.yearsObj) {
      if (setsubun.year === this.currentYear) {
        return setsubun.day;
      }
    }
  };  
}