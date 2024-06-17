const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

// const backend_IP = "http://172.30.248.54:5000";
const backend = "http://" + lanIP + "/api/v1";
let username = "";
let lightSensorData = [];
let temperatuursensordata = [];
let usergamemode = "";
let user1name = "";
let user2name = "";
let gamemode = "";
let finishmode = "";
let chartlight;
let charttemp;
let jsonstartgameusernames = [];
let jsonstartgameusernamesteam1 = [];
let jsonstartgameusernamesteam2 = [];
let jsonstartgameusermode = "single";
let jsonstartgamegamemode = "301";
let jsonstartgameoutmode = "doubleout";
// let loggedin = false;
// let loggedinuser = "no user";
let loggingin = false;
let dailyChart; // Global variable to hold the daily chart instance
let updatinguser = false;
let updatinguserid = 0;
let weeklyChart; // Global variable to hold the daily chart instance
let loggedin = localStorage.getItem("loggedin") === "true";
let loggedinuser = localStorage.getItem("loggedinuser") || "no user";
let loggedinuserid = localStorage.getItem("loggedinuserid");

// ***********************************************************************************************************************
// ********************************************GET************************************************************************
// ***********************************************************************************************************************

const getusers = function () {
  const url = backend + `/users/`;
  handleData(url, show_users, null, "GET");
  console.log("handledatadone");
};
// const gettemperature = function () {
//   console.log(lanIP);
//   console.log(backend);
//   const url = backend + "/temperatuur/"; //http://172.30.248.54:5000/api/v1/temperatuur/
//   handleData(url, show_temperature, null, "GET");
//   // console.log("getemperature")
// };
const get_scoreboard = function (stats, mode) {
  let username = "";

  if (stats === true) {
    if (loggedinuser !== "no user") {
      username = loggedinuser;
      console.log("loggedinuser is not (nouser): " + username);
      const url = backend + `/throws/${username}/`; //http://172.30.248.54:5000/api/v1/throws/<username>/
      handleData(url, show_scoreboard, null, "GET");
    } else {
      console.log("stats = true but loggedinuser is nouser");
    }
  } else {
    const url2 = backend + `/throws/`; //http://172.30.248.54:5000/api/v1/throws/
    console.log("worldwidescore");
    handleData(url2, show_scoreboard, null, "GET");
  }
};

// ***********************************************************************************************************************
// ***********************************************SHOW********************************************************************
// ***********************************************************************************************************************
show_error_fetchusers = function (Jsonresponse) {
  console.log("errorbij fetch users" + Jsonresponse);
};
// **********************scoreboard****************************************************
const show_users = function (Jsonresponse) {
  // console.log(Jsonresponse)
  console.log(Jsonresponse.length + "aantalusers");
  let amountofplayers = document.querySelector(".js-playercount");
  amountofplayers.innerHTML = Jsonresponse.length;
};
const show_scoreboard = function (Jsonresponse) {
  console.log(Jsonresponse.daily);

  const dailyData = Jsonresponse.daily;
  const weeklyData = Jsonresponse.weekly;
  console.log(dailyData);
  console.log(weeklyData);
  const dailyDates = dailyData.map((entry) => entry.date);
  const dailyValues = dailyData.map((entry) => entry.daily_highest_score);

  const weeklyDates = weeklyData.map((entry) => entry.week_of_year);
  const weeklyValues = weeklyData.map((entry) => entry.weekly_highest_score);

  renderscoreboarddailychart(dailyDates, dailyValues);
  renderscoreboardweeklychart(weeklyDates, weeklyValues);
};

// **********************sensors****************************************************

// const show_temperature = function (Jsonresponse) {
//   console.log("temperaturen" + Jsonresponse);
//   const dates = Jsonresponse.map((item) => item.date);
//   const avgTemperatures = Jsonresponse.map((item) => item.avg_temperature);

//   console.log(dates);
//   console.log(avgTemperatures);
//   renderTemperatureChart(dates, avgTemperatures);
// };
const show_stepmotordistance = function (Jsonresponse) {
  console.log("SHOWING STEPMOTORDISTANCE");
  console.log(Jsonresponse);
  const progress_text = document.querySelector(".js-distance");
  progress_text.innerHTML = Jsonresponse.record_count;
};
const show_stepmotorposition = function (Jsonresponse) {
  console.log(Jsonresponse);
};
const show_gamesboules = function (Jsonresponse) {
  console.log("in de gameboules pagina");
  console.log("gameboules" + Jsonresponse);

  const boules = document.querySelector(".js-user-boules");
  const games = document.querySelector(".js-user-games");

  boules.innerHTML = Jsonresponse.boules;
  games.innerHTML = Jsonresponse.games;
};
const show_delete_user = function (Jsonresponse) {
  console.log("dit is de response de showdelete" + Jsonresponse);
  let loginbuttondelete1 = document.querySelector(".js-login");
  let loginbuttondelete2 = document.querySelector(".js-login2");
  loginbuttondelete2.innerHTML = "log in";
  loginbuttondelete1.innerHTML = "log in";
  document.querySelector(".js-header--username").innerHTML = "no user";
  loginbuttondelete2.classList.add("c-button--nonactive");
  loginbuttondelete1.classList.add("c-button--nonactive");
  loggedin = false;
  document.querySelector(".js-update-user").classList.add("o-hidden");
  document.querySelector(".js-delete-user").classList.add("o-hidden");
  document.querySelector(".js-create-user").classList.remove("o-hidden");

  document.querySelector(".js-user-boules").innerHTML = "/";
  document.querySelector(".js-user-games").innerHTML = "/";
};
const show_create_user = function (Jsonresponse) {
  console.log("dit is de creatue user response " + Jsonresponse);
  let loginbuttondelete1 = document.querySelector(".js-login");
  let loginbuttondelete2 = document.querySelector(".js-login2");
  loginbuttondelete2.innerHTML = "logged in";
  loginbuttondelete1.innerHTML = "logged in";
  document.querySelector(".js-header--username").innerHTML = loggedinuser;
  loginbuttondelete2.classList.remove("c-button--nonactive");
  loginbuttondelete1.classList.remove("c-button--nonactive");
  loggedin = true;
  document.querySelector(".js-user-boules").innerHTML = "0";
  document.querySelector(".js-user-games").innerHTML = "0";
};
const show_updateuser_form = function (Jsonresponse) {
  console.log(Jsonresponse);
  updatinguserid = Jsonresponse.IDuser;
  updatingname = Jsonresponse.name;
  updatingsurname = Jsonresponse.surname;
  updatingage = Jsonresponse.age;
  updatinglength = Jsonresponse.length;
  updatingusername = Jsonresponse.username;
  updatingcountry = Jsonresponse.country;

  document.getElementById("nameformcreate").value = updatingname;
  document.getElementById("surnameformcreate").value = updatingsurname;
  document.getElementById("ageformcreate").value = updatingage;
  document.getElementById("lengthformcreate").value = updatinglength;
  document.getElementById("usernameformcreate").value = updatingusername;
  document.getElementById("countryformcreate").value = updatingcountry;

  // invullen in form
};
// *************************lampen******************************************************
// showlampen

// *************************playerdetails + gemasettings*******************************
// show users plusklik
// show users gamemode

// ****************************livegame*************************************************
// show livegame(gamemode, usernames, standard points)
const start_game = function (jsonData) {
  fetch(backend + "/games/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(jsonData),
  })
    .then((response) => response.json())
    .then((result) => {
      console.log("Success:", result);
      // Handle success response as needed
    })
    .catch((error) => {
      console.error("Error:", error);
      // Handle error response as needed
    });
  // const url = backend + "/games/";
  // handleData(url,JSON(jsonData), null, "POST");

  console.log(jsonData);

  const finishMode = jsonData.finishMode;
  const gamemode = jsonData.gameMode;

  const gameliveteamselect = document.querySelector(".js-gamelive-teamselect");
  const team1div = document.querySelector(".js-gamelive-team1");
  const team2div = document.querySelector(".js-gamelive-team2");

  let playerteamHTML = "";

  if (jsonData.userGameMode === "single") {
    gameliveteamselect.classList.add("o-hidden");
    team1div.classList.remove("--1of2");
    team1div.classList.add("--1of1");
    team2div.classList.add("o-hidden");

    playerteamHTML = `
      <div class="c-GameLive--player">
        <div class="c-GameLive--player--info">
          <div class="c-GameLive--player--info--name js-gamelive--extra--username">${jsonData.username}</div>
          <div class="c-GameLive--player--info--score js-gamelive--extra--score">${gamemode}</div>
        </div>
        <div class="c-GameLive--player--points">
          <div class="c-GameLive--player--points--throw js-gamelive--extra--throw1">0</div>
          <div class="c-GameLive--player--points--throw js-gamelive--extra--throw2">0</div>
          <div class="c-GameLive--player--points--throw js-gamelive--extra--throw3">0</div>
        </div>
      </div>`;
    team1div.innerHTML = playerteamHTML;
  } else if (jsonData.userGameMode === "team") {
    gameliveteamselect.classList.remove("o-hidden");

    team1div.classList.add("--1of2");
    team1div.classList.remove("--1of1");
    team2div.classList.remove("o-hidden");

    const team1PlayersHTML = jsonData.usernames.team1
      .map(
        (username) => `
        <div class="c-GameLive--player">
          <div class="c-GameLive--player--info">
            <div class="c-GameLive--player--info--name js-gamelive--extra--username">${username}</div>
            <div class="c-GameLive--player--info--score js-gamelive--extra--score">${gamemode}</div>
          </div>
          <div class="c-GameLive--player--points">
            <div class="c-GameLive--player--points--throw js-gamelive--extra--throw1">0</div>
            <div class="c-GameLive--player--points--throw js-gamelive--extra--throw2">0</div>
            <div class="c-GameLive--player--points--throw js-gamelive--extra--throw3">0</div>
          </div>
        </div>`
      )
      .join("");

    const team2PlayersHTML = jsonData.usernames.team2
      .map(
        (username) => `
        <div class="c-GameLive--player">
          <div class="c-GameLive--player--info c-GameLive--player--info--reverse">
            <div class="c-GameLive--player--info--name js-gamelive--extra--username">${username}</div>
            <div class="c-GameLive--player--info--score js-gamelive--extra--score">${gamemode}</div>
          </div>
          <div class="c-GameLive--player--points">
            <div class="c-GameLive--player--points--throw js-gamelive--extra--throw1">0</div>
            <div class="c-GameLive--player--points--throw js-gamelive--extra--throw2">0</div>
            <div class="c-GameLive--player--points--throw js-gamelive--extra--throw3">0</div>
          </div>
        </div>`
      )
      .join("");

    team1div.innerHTML = team1PlayersHTML;
    team2div.innerHTML = team2PlayersHTML;
  }
};

// livegame via socketio

// ***********************************************************************************************************************
// **************************************************CHARTS***************************************************************
// ***********************************************************************************************************************

// *****************************sensors*************************

const initializetempsensor = function () {
  let optionstemp = {
    chart: {
      type: "line",
      height: 350,
      animations: {
        enabled: true,
        easing: "linear",
        dynamicAnimation: {
          speed: 1000,
        },
      },
    },
    series: [
      {
        name: "temp Sensor",
        data: temperatuursensordata,
      },
    ],
    xaxis: {
      type: "datetime",
      labels: {
        formatter: function (value, timestamp) {
          // Format date and time
          let date = new Date(timestamp);
          let hours = date.getHours().toString().padStart(2, "0");
          let minutes = date.getMinutes().toString().padStart(2, "0");
          let time = `${hours}:${minutes}`;
          return time;
        },
        datetimeFormatter: {
          day: "MMM dd", // Show date once per day
          hour: "HH:mm",
        },
      },
    },
    yaxis: {
      max: 100,
      min: 0,
    },
  };
  charttemp = new ApexCharts(
    document.getElementById("temperatureChart"),
    optionstemp
  );
  charttemp.render();
};
// Update chart with new data
function updateGraphtemperatuursensor(Jsonresponse) {
  var newValue = {
    x: new Date().getTime(), // Use current timestamp
    y: Number(Math.round(Jsonresponse.waarde + "e" + 2) + "e-" + 2),
  };

  temperatuursensordata.push(newValue);

  // Limit the data to a certain length if necessary
  if (temperatuursensordata.length > 50) {
    temperatuursensordata.shift();
  }

  charttemp.updateSeries([
    {
      data: temperatuursensordata,
    },
  ]);
}

// Initialize ApexCharts chart for lightsensor
const initializelichtsensor = function () {
  let optionslight = {
    chart: {
      type: "line",
      height: 350,
      animations: {
        enabled: true,
        easing: "linear",
        dynamicAnimation: {
          speed: 1000,
        },
      },
    },
    series: [
      {
        name: "Light Sensor",
        data: lightSensorData,
      },
    ],
    xaxis: {
      type: "datetime",
      labels: {
        formatter: function (value, timestamp) {
          // Format date and time
          let date = new Date(timestamp);
          let hours = date.getHours().toString().padStart(2, "0");
          let minutes = date.getMinutes().toString().padStart(2, "0");
          let time = `${hours}:${minutes}`;
          return time;
        },
        datetimeFormatter: {
          day: "MMM dd", // Show date once per day
          hour: "HH:mm",
        },
      },
    },
    yaxis: {
      max: 100,
      min: 0,
    },
  };
  chartlight = new ApexCharts(
    document.getElementById("lightChart"),
    optionslight
  );
  chartlight.render();
};
// Update chart with new data
function updateGraphLichtsensor(Jsonresponse) {
  var newValue = {
    x: new Date().getTime(), // Use current timestamp
    y: Number(Math.round(Jsonresponse.waarde + "e" + 2) + "e-" + 2),
  };

  lightSensorData.push(newValue);

  // Limit the data to a certain length if necessary
  if (lightSensorData.length > 50) {
    lightSensorData.shift();
  }

  chartlight.updateSeries([
    {
      data: lightSensorData,
    },
  ]);
}

// **************************scoreboard*************************
// 2*grafiek
const renderscoreboarddailychart = function (dates, values) {
  // if (dailyChart) {
  //   dailyChart.destroy();
  // }
  const options = {
    chart: {
      type: "bar",
    },
    series: [
      {
        name: "throw",
        data: values,
      },
    ],
    xaxis: {
      categories: dates,
    },
  };
  if (dailyChart) {
    // If the chart already exists, update it
    dailyChart.updateOptions(options);
    dailyChart.updateSeries([
      {
        name: "throw",
        data: values,
      },
    ]);
  } else {
    // If the chart does not exist, create a new one
    dailyChart = new ApexCharts(document.getElementById("Dailygraph"), options);
    dailyChart.render();
  }
};
const renderscoreboardweeklychart = function (dates, values) {
  // if (weeklyChart) {
  //   weeklyChart.destroy();
  // }
  const options = {
    chart: {
      type: "bar",
    },
    series: [
      {
        name: "throw",
        data: values,
      },
    ],
    xaxis: {
      categories: dates,
    },
  };

  if (weeklyChart) {
    // If the chart already exists, update it
    weeklyChart.updateOptions(options);
    weeklyChart.updateSeries([
      {
        name: "throw",
        data: values,
      },
    ]);
  } else {
    // If the chart does not exist, create a new one
    weeklyChart = new ApexCharts(
      document.getElementById("Weeklygraph"),
      options
    );
    weeklyChart.render();
  }
};
// ***********************************************************************************************************************
// *****************************************************UI****************************************************************
// ***********************************************************************************************************************
const updateUI = () => {
  const loginbutton = document.querySelector(".js-login");
  const loginbutton2 = document.querySelector(".js-login2");

  if (loggedin) {
    console.log("User logged in:", loggedinuser);
    document.querySelector(".js-header--username").innerHTML = loggedinuser;
    loginbutton.innerHTML = "loggedin";
    loginbutton.classList.remove("c-button--nonactive");
    loginbutton2.innerHTML = "loggedin";
    loginbutton2.classList.remove("c-button--nonactive");

    url = backend + "/gamesboules/" + loggedinuserid + "/";
    // console.log("dit is de url die naar de showgameboules verstuurd zal worden: " + url)
    handleData(url, show_gamesboules, null, "GET");
    // Show relevant user info (replace with actual data)

    document.querySelector(".js-update-user").classList.remove("o-hidden");
    document.querySelector(".js-delete-user").classList.remove("o-hidden");
    document.querySelector(".js-create-user").classList.add("o-hidden");
  } else {
    console.log("User logged out");
    document.querySelector(".js-header--username").innerHTML = "no user";
    loginbutton.innerHTML = "log in";
    loginbutton.classList.add("c-button--nonactive");
    loginbutton2.innerHTML = "log in";
    loginbutton2.classList.add("c-button--nonactive");

    // Hide user info and actions
    document.querySelector(".js-user-boules").innerHTML = "/";
    document.querySelector(".js-user-games").innerHTML = "/";
    document.querySelector(".js-update-user").classList.add("o-hidden");
    document.querySelector(".js-delete-user").classList.add("o-hidden");
    document.querySelector(".js-create-user").classList.remove("o-hidden");
  }
};
const listenToUI = function () {
  paginas = document.querySelector(".c-header__nav-list");
  let navelscoreboard = document.querySelector(".js-scoreboard");
  let navellights = document.querySelector(".js-lights");
  let navelgames = document.querySelector(".js-games");
  let navelsensors = document.querySelector(".js-sensors");
  let next = document.querySelector(".js-next");
  let navellivegame = document.querySelector(".js-livegame");

  next.addEventListener("click", function () {
    showPage("page4");
  });
  paginas.addEventListener("click", function (event) {
    const classListnavitem = event.target.classList;
    console.log("creating eventlistener");

    navelscoreboard.classList.remove("c-link--active");
    navellights.classList.remove("c-link--active");
    navelgames.classList.remove("c-link--active");
    navelsensors.classList.remove("c-link--active");
    navellivegame.classList.remove("c-link--active");

    switch (true) {
      case classListnavitem.contains("js-scoreboard"):
        navelscoreboard.classList.toggle("c-link--active");
        console.log("toggled");
        showPage("page1");

        break;
      case classListnavitem.contains("js-lights"):
        navellights.classList.toggle("c-link--active");
        showPage("page2");

        break;
      case classListnavitem.contains("js-games"):
        navelgames.classList.toggle("c-link--active");
        showPage("page3");

        break;
      case classListnavitem.contains("js-sensors"):
        navelsensors.classList.toggle("c-link--active");
        showPage("page6");

        break;
      case classListnavitem.contains("js-livegame"):
        navellivegame.classList.toggle("c-link--active");
        showPage("page5");
      default:
        break;
    }
  });
  document
    .querySelector(".js-button-createuser")
    .addEventListener("click", function (event) {
      event.preventDefault();
      console.log("in the create user form");
      const data = {
        name: document.getElementById("nameformcreate").value,
        surname: document.getElementById("surnameformcreate").value,
        age: document.getElementById("ageformcreate").value,
        length: document.getElementById("lengthformcreate").value,
        username: document.getElementById("usernameformcreate").value,
        country: document.getElementById("countryformcreate").value,
      };
      console.log(data);
      loggedinuser = data.username;
      // url = backend + "/users/"
      // handleData(url,show_create_user,null,"POST")
      if (updatinguser === false) {
        fetch(backend + "/users/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        })
          .then((response) => response.json())
          .then((result) => {
            show_create_user(data);
            console.log("Success:", result);
            // Handle success response as needed
          })
          .catch((error) => {
            console.error("Error:", error);
            // Handle error response as needed
          });
      } else {
        fetch(backend + "/users/" + updatinguserid + "/", {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        })
          .then((response) => response.json())
          .then((result) => {
            show_create_user(data);
            console.log("Success:", result);
            // Handle success response as needed
          })
          .catch((error) => {
            console.error("Error:", error);
            // Handle error response as needed
          });
      }
      updatinguser = false;
      document
        .querySelector(".overlay-form-create-user")
        .classList.add("o-hidden");
    });

  // *************************scoreboard***********************************************

  container = document.querySelector(".o-body");
  container.addEventListener("click", function (event) {
    event.preventDefault();
    // Get the class list of the clicked element
    const classList = event.target.classList;

    // Check the class of the clicked element using a switch case statement
    let elyourstats = document.querySelector(".js-YOURSTATS");
    let elworldwide = document.querySelector(".js-WORLDWIDESTATS");
    let gamemode301 = document.querySelector(".js-301");
    let gamemode501 = document.querySelector(".js-501");
    let gamemode9lives = document.querySelector(".js-9lives");
    let lamp1 = document.querySelector(".jslamp1");
    let lamp2 = document.querySelector(".jslamp2");
    let lamp3 = document.querySelector(".jslamp3");
    let singleplayerdetails = document.querySelector(
      ".js-single-playerdetails"
    );
    let teamplayerdetails = document.querySelector(".js-teams-playerdetails");
    let gamesgamemode301 = document.querySelector(".js-games-gamemode-301");
    let gamesgamemode501 = document.querySelector(".js-games-gamemode-501");
    let gamesgamemode9lives = document.querySelector(
      ".js-games-gamemode-9lives"
    );
    let gamesdoubleout = document.querySelector(".js-games-doubleout");
    let gamessingleout = document.querySelector(".js-games-singleout");
    let adduserrowteam = document.querySelector(".js-adduserrowteam");
    let adduserrowsingle = document.querySelector(".js-adduserrowsingle");

    let loginbutton = document.querySelector(".js-login");
    let loginbutton2 = document.querySelector(".js-login2");
    let deleteuser = document.querySelector(".js-delete-user");
    let createuser = document.querySelector(".js-create-user");
    let updateuser = document.querySelector(".js-update-user");

    switch (true) {
      case classList.contains("js-YOURSTATS"):
        console.log("yourstats");
        elyourstats.classList.toggle("c-button--nonactive");
        elworldwide.classList.toggle("c-button--nonactive");
        isyourstats = true;
        break;
      case classList.contains("js-WORLDWIDESTATS"):
        console.log("wordwidestats");
        elyourstats.classList.toggle("c-button--nonactive");
        elworldwide.classList.toggle("c-button--nonactive");
        isyourstats = false;
        break;
      case classList.contains("js-301"):
        console.log("gamemode 301 button clicked!");
        gamemode301.classList.add("c-button--active");
        gamemode301.classList.toggle("c-button--nonactive");
        gamemode501.classList.remove("c-button--active");
        gamemode501.classList.add("c-button--nonactive");
        gamemode9lives.classList.remove("c-button--active");
        gamemode9lives.classList.add("c-button--nonactive");
        get_scoreboard(isyourstats, 1);
        break;
      case classList.contains("js-501"):
        console.log("gamemode 501 button clicked!");
        gamemode501.classList.add("c-button--active");
        gamemode501.classList.toggle("c-button--nonactive");
        gamemode301.classList.remove("c-button--active");
        gamemode301.classList.add("c-button--nonactive");
        gamemode9lives.classList.remove("c-button--active");
        gamemode9lives.classList.add("c-button--nonactive");
        get_scoreboard(isyourstats, 2);
        break;
      case classList.contains("js-9lives"):
        console.log("gamemode 9 lives button clicked!");
        gamemode9lives.classList.add("c-button--active");
        gamemode9lives.classList.toggle("c-button--nonactive");
        gamemode301.classList.remove("c-button--active");
        gamemode301.classList.add("c-button--nonactive");
        gamemode501.classList.remove("c-button--active");
        gamemode501.classList.add("c-button--nonactive");
        get_scoreboard(isyourstats, 3);
        break;
      case classList.contains("jslamp1"):
        console.log("lamp1 button clicked!");
        lamp1.classList.toggle("c-button--nonactive");
        break;
      case classList.contains("jslamp2"):
        console.log("lamp2 button clicked!");
        lamp2.classList.toggle("c-button--nonactive");
        break;
      case classList.contains("jslamp3"):
        console.log("lamp3 button clicked!");
        lamp3.classList.toggle("c-button--nonactive");
        break;
      case classList.contains("js-single-playerdetails"):
        singleplayerdetails.classList.toggle("c-button--nonactive");
        teamplayerdetails.classList.add("c-button--nonactive");
        adduserrowteam.classList.add("o-hidden");
        adduserrowsingle.classList.remove("o-hidden");
        jsonstartgameusermode = "single";
        break;
      case classList.contains("js-teams-playerdetails"):
        singleplayerdetails.classList.add("c-button--nonactive");
        teamplayerdetails.classList.toggle("c-button--nonactive");
        teamplayerdetails.classList.add("c-button--active");
        adduserrowteam.classList.remove("o-hidden");
        adduserrowsingle.classList.add("o-hidden");
        jsonstartgameusermode = "team";
        break;
      case classList.contains("js-games-gamemode-301"):
        gamesgamemode301.classList.add("c-button--active");
        gamesgamemode301.classList.remove("c-button--nonactive");
        gamesgamemode501.classList.add("c-button--nonactive");
        gamesgamemode9lives.classList.add("c-button--nonactive");
        jsonstartgamegamemode = "301";
        break;
      case classList.contains("js-games-gamemode-501"):
        gamesgamemode501.classList.add("c-button--active");
        gamesgamemode501.classList.remove("c-button--nonactive");
        gamesgamemode9lives.classList.add("c-button--nonactive");
        gamesgamemode301.classList.add("c-button--nonactive");
        jsonstartgamegamemode = "501";

        break;
      case classList.contains("js-games-gamemode-9lives"):
        gamesgamemode9lives.classList.add("c-button--active");
        gamesgamemode9lives.classList.remove("c-button--nonactive");
        gamesgamemode501.classList.add("c-button--nonactive");
        gamesgamemode301.classList.add("c-button--nonactive");
        jsonstartgamegamemode = "9lives";

        break;
      case classList.contains("js-games-doubleout"):
        gamesdoubleout.classList.add("c-button--active");
        gamesdoubleout.classList.remove("c-button--nonactive");
        gamessingleout.classList.add("c-button--nonactive");
        jsonstartgameoutmode = "doubleout";
        break;
      case classList.contains("js-games-singleout"):
        gamessingleout.classList.add("c-button--active");
        gamessingleout.classList.remove("c-button--nonactive");
        gamesdoubleout.classList.add("c-button--nonactive");
        jsonstartgameoutmode = "singleout";
        break;
      case classList.contains("js-games-startgame"):
        if (jsonstartgameusermode === "single") {
          const jsonData = {
            userGameMode: jsonstartgameusermode,
            gameMode: jsonstartgamegamemode,
            finishMode: jsonstartgameoutmode,
            username: jsonstartgameusernames[0],
          };
          console.log(JSON.stringify(jsonData, null, 2));
          showPage("page5");
          start_game(jsonData);
        } else if (jsonstartgameusermode === "team") {
          const jsonData = {
            userGameMode: jsonstartgameusermode,
            gameMode: jsonstartgamegamemode,
            finishMode: jsonstartgameoutmode,
            usernames: {
              team1: jsonstartgameusernamesteam1,
              team2: jsonstartgameusernamesteam2,
            },
          };
          console.log(JSON.stringify(jsonData, null, 2));
          showPage("page5");
          start_game(jsonData);
        }
        document.querySelector(".js-livegame").classList.remove("o-hidden");
        break;
      case classList.contains("js-previous"):
        showPage("page3");
        break;
      case classList.contains("js-stop"):
        // send stopgame to backend via route
        url = backend + "/stop/";
        handleData(url, null, null, "POST");
        showPage("page2");
        document.querySelector(".js-livegame").classList.add("o-hidden");
        window.location.reload();
        break;
      case classList.contains("js-login"):
      case classList.contains("js-login2"):
        console.log("js-login or js-login2 clicked");
        if (!loggedin) {
          console.log("Logging in");
          loggedin = true;
          loggingin = true;
          localStorage.setItem("loggedin", "true");
          fetchUsers(); // Function to fetch users
          // Update UI after login
          loggedinuser = localStorage.getItem("loggedinuser") || "no user";
          updateUI();
        } else {
          console.log("Logging out");
          loggedin = false;
          localStorage.setItem("loggedin", "false");
          localStorage.removeItem("loggedinuser");
          updateUI();
        }
        break;

      case classList.contains("js-delete-user"):
        if (loggedin) {
          console.log("Deleting user");
          const username = loggedinuser;
          console.log("Username:", username);
          const url = `${backend}/users/${username}/`;
          handleData(url, show_delete_user, null, "DELETE"); // Function to handle DELETE request
        }
        break;

      case classList.contains("js-create-user"):
        if (!loggedin) {
          console.log("Creating user");
          document
            .querySelector(".overlay-form-create-user")
            .classList.remove("o-hidden");
        }
        break;

      case classList.contains("js-update-user"):
        if (loggedin) {
          console.log("Updating user");
          document
            .querySelector(".overlay-form-create-user")
            .classList.remove("o-hidden");
          const url = `${backend}/users/${loggedinuser}/`;
          updatinguser = true;
          handleData(url, show_updateuser_form, null, "GET"); // Function to handle GET request
        }
        break;

      case classList.contains("js-hideoverlayformcreateuser"):
        document
          .querySelector(".overlay-form-create-user")
          .classList.add("o-hidden");
        break;

      default:
        break;

        document
          .querySelector(".overlay-form-create-user")
          .classList.add("o-hidden");
        break;

      // deleteuser
      // createuser
      // updateuser
    }

    // let popup = document.querySelector('.js-popup');
    let overlay = document.querySelector(".js-overlay");
    let userList = document.querySelector(".js-userlist");
    let currentTeam = null;
    let plusbutton = document.querySelector(".js-adduser-btn");
    let plusbutton2 = document.querySelector(".js-adduser-btn2");
    let plusbutton3 = document.querySelector(".js-adduser-btn3");

    function fetchUsers() {
      console.log("fetching usrs");
      const url = backend + `/users/`;
      handleData(url, show_Popup, show_error_fetchusers(), "GET");
      console.log("handledatadone");
    }

    function show_Popup(Jsonresponse) {
      console.log("users", Jsonresponse); // Corrected the console log
      // popup.classList.remove("o-hidden");
      overlay.classList.remove("o-hidden");
      userList = ""; // Reset the user list

      users = Jsonresponse;
      let userListHTML = ""; // Create an HTML string to append the list items

      users.forEach((user) => {
        userListHTML += `<li data-username="${user.username} "data-id="${user.IDuser}">${user.username}</li>`;
      });
      console.log("userlist : " + userListHTML);
      document.querySelector(".js-userlist").innerHTML = userListHTML;

      document.querySelectorAll(".js-userlist li").forEach((item) => {
        item.addEventListener("click", function (event) {
          const username = event.target.getAttribute("data-username");
          const userid = event.target.getAttribute("data-id");
          console.log("dit is het userid van het gelkikete item: " + userid);
          if (loggingin === true) {
            loggedin = true;
            document
              .querySelector(".js-update-user")
              .classList.remove("o-hidden");
            document
              .querySelector(".js-delete-user")
              .classList.remove("o-hidden");
            document.querySelector(".js-create-user").classList.add("o-hidden");
            loggedinuser = username;
            localStorage.setItem("loggedinuser", username);
            localStorage.setItem("loggedinuserid", userid);

            document.querySelector(".js-header--username").innerHTML =
              loggedinuser;
            url = backend + "/gamesboules/" + userid + "/";
            // console.log("dit is de url die naar de showgameboules verstuurd zal worden: " + url)
            handleData(url, show_gamesboules, null, "GET");
            hidePopup();
            loggingin = false;
          } else {
            document.querySelector(
              `.js-adduser-team${currentTeam}`
            ).innerHTML += `<div class="c-Playerdetails--adduser--team--users--player">${username}</div>`;
            hidePopup();
            if (currentTeam === 1) {
              jsonstartgameusernamesteam1.push(username);
            }
            if (currentTeam === 2) {
              jsonstartgameusernamesteam2.push(username);
            }
            if (currentTeam === 3) {
              jsonstartgameusernames[0] = username;
            }
          }
        });
      });
    }

    function hidePopup() {
      // popup.classList.add("o-hidden");
      overlay.classList.add("o-hidden");
    }

    plusbutton.addEventListener("click", function () {
      console.log("ha you been clicked niga");
      const team = 1;
      currentTeam = team;
      fetchUsers();
    });
    plusbutton2.addEventListener("click", function () {
      console.log("ha you been clicked niga2");
      const team = 2;
      currentTeam = team;
      fetchUsers();
    });
    plusbutton3.addEventListener("click", function () {
      console.log("ha you been clicked niga3");
      const team = 3;
      currentTeam = team;
      fetchUsers();
      plusbutton3.classList.add("o-hidden");
    });

    overlay.addEventListener("click", function () {
      hidePopup();
    });
  });
};
// ***********************************************************************************************************************
// ****************************************************SOCKETIO***********************************************************
// ***********************************************************************************************************************

const listenToSocket = function () {
  socketio.on("connect", function () {
    console.log("verbonden met socket webserver");
  });

  socketio.on("B2F_alle_worpen", function (Jsonresponse) {
    console.log(Jsonresponse);
  });

  socketio.on("B2F_namen_users", function (Jsonresponse) {
    console.log(Jsonresponse);

    // show_users(Jsonresponse);
  });
  socketio.on("B2F_GameFinished", function (Jsonresponse) {
    console.log(Jsonresponse);
    console.log("winnaar: " + Jsonresponse.username);
    showPage("page2");
    document.querySelector(".js-livegame").classList.add("o-hidden");
    window.location.reload();
  });
  // **********************************Sensors***************************************
  socketio.on("B2F_temperatuur", function (Jsonresponse) {
    console.log("temperatuur : " + Jsonresponse);
    updateGraphtemperatuursensor(Jsonresponse);
  });
  socketio.on("B2F_lichtsensor", function (Jsonresponse) {
    console.log(Jsonresponse);
    updateGraphLichtsensor(Jsonresponse);

    const progressBar = document.getElementById("progress-bar");
    const progressText = document.getElementById("progress-text");

    // Clamp the value between 0 and 100
    const percentage = Math.max(0, Math.min(100, Jsonresponse.waarde));

    // Update the progress bar width and text
    progressBar.style.width =
      Number(Math.round(percentage + "e" + 2) + "e-" + 2) + "%";
    progressText.textContent =
      Number(Math.round(percentage + "e" + 2) + "e-" + 2) + "%";
  });

  // todo: positie stappenmotor, distance covered
  socketio.on("B2F_positionstepmotor", function (Jsonresponse) {
    console.log("in de positiestapmotor functie");
    console.log(Jsonresponse);
    positiestappenmotor = document.querySelector(".js-position");
    positiestappenmotor.innerHTML = Jsonresponse.waarde;
    url = backend + "/distance/";
    handleData(url, show_stepmotordistance);
  });

  // *********************************lampen***************************************
  // todo:lichtsensor (ev in sensors lichsensor B2f)
  // listentolamps(nrml 2 lampen)

  // *************************************livegame***************************************
  // todo als team veranderd, stuurt backend door welke punten ze nu hebben
  socketio.on("B2F_last3throws", function (Jsonresponse) {
    console.log(
      "samenvatting last 3 throws: " + JSON.stringify(Jsonresponse.beurt)
    );

    // Extracting data from the response
    const player = Jsonresponse.beurt.player;
    const username = Jsonresponse.beurt.username;
    const throw1 = Jsonresponse.beurt.throw1;
    const throw2 = Jsonresponse.beurt.throw2;
    const throw3 = Jsonresponse.beurt.throw3;

    // Query all player name elements
    const playerNameElements = document.querySelectorAll(
      ".c-GameLive--player--info--name"
    );
    const playerElement = Array.from(playerNameElements).find(
      (el) => el.textContent.trim() === username.trim()
    );

    if (playerElement) {
      // Find the parent .c-GameLive--player element
      const playerContainer = playerElement.closest(".c-GameLive--player");

      // Update the player's remaining score
      const scoreElement = playerContainer.querySelector(
        ".js-gamelive--extra--score"
      );
      const remainingScore =
        parseInt(scoreElement.textContent) - (throw1 + throw2 + throw3);
      scoreElement.textContent = remainingScore;

      // Update the player's last 3 throws
      playerContainer.querySelector(".js-gamelive--extra--throw1").textContent =
        throw1;
      playerContainer.querySelector(".js-gamelive--extra--throw2").textContent =
        throw2;
      playerContainer.querySelector(".js-gamelive--extra--throw3").textContent =
        throw3;
    } else {
      console.error(`Player element for username "${username}" not found.`);
    }
  });
};

// ***********************************************************************************************************************
// ****************************************************INIT***************************************************************
// ***********************************************************************************************************************

const init = function () {
  console.info("DOM geladen");

  getusers();

  listenToUI();
  listenToSocket();
  updateUI();

  // **************sensors
  // gettemperature();
  initializetempsensor();
  initializelichtsensor();

  // getusers();
  socketio.emit("F2B_read_all_worpen");
};

document.addEventListener("DOMContentLoaded", init);

// const show_users = function (Jsonresponse) {
//   console.log(lanIP);
//   users = Jsonresponse.users;
//   console.log(users);
//   for (const user of users) {
//     console.log(user);
//     document.querySelector(".js-IDuser").innerHTML = user.IDuser;
//     document.querySelector(".js-age").innerHTML = user.age;
//     document.querySelector(".js-country").innerHTML = user.country;
//     document.querySelector(".js-length").innerHTML = user.length;
//     document.querySelector(".js-name").innerHTML = user.name;
//     document.querySelector(".js-surname").innerHTML = user.surname;
//     document.querySelector(".js-username").innerHTML = user.username;
//   }
// };

// ******************************************************pages*************
// Function to show the specified page and hide others
function showPage(pageId) {
  // Get all div elements with IDs starting with "page"
  const divs = document.querySelectorAll(".c-section--row");

  // Loop through each div and toggle its visibility based on the pageId
  divs.forEach(function (div) {
    if (div.classList.contains(pageId)) {
      // Show the div if it has the specified pageId in its class list
      div.classList.remove("o-hidden");
    } else {
      // Hide the div if it does not have the specified pageId in its class list
      div.classList.add("o-hidden");
    }
  });
}

// function getActiveButton(buttonGroupSelector) {
//     const buttons = document.querySelectorAll(buttonGroupSelector);
//     for (const button of buttons) {
//         if (!button.classList.contains('c-button--nonactive')) {
//             return button.textContent.trim(); // Assuming button text is the value we want
//         }
//     }
//     return null;
// }

// // Function to get usernames based on the user game mode
function getUsernames() {
  console.log("in de getusernames functie");
  // Get usernames for team mode
  const team1Elements = document.querySelectorAll(
    ".js-adduserrowteam .team1-selector"
  );
  const team2Elements = document.querySelectorAll(
    ".js-adduserrowteam .team2-selector"
  );

  const team1Names = Array.from(team1Elements).map((el) =>
    el.textContent.trim()
  );
  const team2Names = Array.from(team2Elements).map((el) =>
    el.textContent.trim()
  );
  console.log("team1" + team1Names);
  return { team1: team1Names, team2: team2Names };
}
