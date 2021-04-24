var g_Interval = 1;
var g_PersonCount = parseInt("{{ pointrecord_num }}");
var g_Timer;
var running = false;

function beginRndNum(trigger) {
  if (running) {
  	setTimeout(randomNumber(),5000)
    running = false;
    clearTimeout(g_Timer);
    $(trigger).val("開始");
    $('#ResultNum').css('color', '#0babce');
    randomNumber();
  } else {
    running = true;
    $('#ResultNum').css('color', 'black');
    $(trigger).val("停止");
    beginTimer();
  }
}

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
}
function updateRndNum() {
  var num = Math.floor(Math.random() * g_PersonCount + 1);
  var name = randomNumber();
  $('#ResultNum').html(name);
}

function beginTimer() {
  g_Timer = setTimeout(beat, g_Interval);
}

function beat() {
  g_Timer = setTimeout(beat, g_Interval);
  updateRndNum();
}

function randomNumber() {
  var random = jsonContent.member[Math.floor(Math.random() * jsonContent.member.length)];
  //console.log(random.name);
  //console.log(random.id);
  return random.name;
}