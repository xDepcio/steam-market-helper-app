async function sellFunc() {
    for(let i = 0; i < cards.length; i++) {
        let card = cards.item(i);
        let eleId = card.firstChild.id;
        let [appid, contextid, assetid] = eleId.split('_');
        console.log(appid, contextid, assetid);

        let params = new URLSearchParams({
              sessionid: "aa8e7fc6707a9921e589df1a", // || g_sessionID;
              appid: appid,
              contextid: contextid,
              assetid: assetid,
              amount: 1,
              price: 98
          });
        let paramsStr = params.toString();
        // console.log(params.toString());

        let res = await fetch("https://steamcommunity.com/market/sellitem/", {
          "headers": {
            "accept": "*/*",
            "accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sec-ch-ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\", \"Google Chrome\";v=\"108\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
          },
          "referrer": "https://steamcommunity.com/profiles/76561198462126877/inventory/",
          "referrerPolicy": "strict-origin-when-cross-origin",
          "body": paramsStr,
          "method": "POST",
          "mode": "cors",
          "credentials": "include"
        });
        let data = await res.json();
        console.log(data);
    };
};
