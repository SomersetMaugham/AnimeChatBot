// Variables
const messages = document.querySelector('.message-list');
const btn = document.querySelector('.btn');
const input = document.querySelector('input');

const volume = 1; // [Optional arg, can be null or empty] [0.0 - 1.0]
const expression = 4; // [Optional arg, can be null or empty] [index|name of expression]
const resetExpression = true; // [Optional arg, can be null or empty] [true|false] [default: true] [if true, expression will be reset to default after animation is over]
const crossOrigin = "anonymous"; // [Optional arg, to use not same-origin audios] [DEFAULT: null]
let model;

window.PIXI = PIXI;
const live2d = PIXI.live2d;
const canvas_container = document.getElementById('canvas_container');

window.onload = function () {
  (async function () {
    const app = new PIXI.Application({
      view: document.getElementById('canvas'),
      autoStart: true,
      height: canvas_container.offsetHeight,
      width: canvas_container.offsetWidth,
      backgroundAlpha: 0.0,
    });

    // model = await live2d.Live2DModel.from('static/models/10an/10an_culture.model3.json',{autoInteract: false});
    model = await live2d.Live2DModel.from('static/models/haru/haru_greeter_t03.model3.json', { autoInteract: false });
    // model = await live2d.Live2DModel.from('static/models/shizuku/shizuku.model.json', { autoInteract: false });

    app.stage.addChild(model);
    let scale = 1.5;
    const scaleX = (canvas_container.offsetWidth) * scale / model.width;
    const scaleY = (canvas_container.offsetHeight) * scale / model.height;

    resize_factor = Math.min(scaleX, scaleY);
    // transforms
    model.x = -50;
    model.y = innerHeight - 100;
    model.rotation = Math.PI;
    model.skew.x = Math.PI;
    model.scale.set(resize_factor);
    model.anchor.set(1, 1);
    // model.motion('w-animal-tilthead01');
    model.motion('haharu_g_m05.motion3');
    //model.motion('haru_g_m05.motion3');
    
  })();

  function messageInteraction(audio_link, motion = NaN) {
    model.speak(audio_link, { volume: volume, expression: expression, resetExpression: resetExpression, crossOrign: crossOrigin });
    model.motion(motion);
  }

  // Button/Enter Key
  btn.addEventListener('click', sendMessage);
  input.addEventListener('keyup', function (e) {
    if (e.keyCode == 13) sendMessage();
  });

  function loadHistory() {
    fetch('/history')
      .then(response => response.json())
      .then(data => {
        // 데이터를 역순으로 정렬합니다.
        const reversedData = data.reverse();
        for (let i = 0; i < reversedData.length; i++) {
          if (reversedData[i].role === 'user') {
            writeLine(`<span>User</span><br> ${reversedData[i].content}`, 'primary');
          } else {
            writeLine(`<span>AKI</span><br> ${reversedData[i].content}`, 'secondary');
          }
        }
      })
      .catch(error => console.error('Error:', error));
  }

  loadHistory();

  // Messenger Functions
  function sendMessage() {
    var msg = input.value;
    writeLine(`<span>User</span><br> ${msg}`, 'primary');

    input.value = '';
    fetch('/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 'message': msg }),
    })
      .then(response => response.json())
      .then(data => addMessage(data, 'secondary'))
      .catch(error => console.error('Error:', error));
  }

  function addMessage(msg, typeMessage = 'primary') {
    writeLine(`<span>${msg.FROM}</span><br> ${msg.MESSAGE}`, typeMessage);
    messageInteraction(msg.WAV, motion = NaN);
  }

  function writeLine(text, typeMessage) {
    let message = document.createElement('li');
    message.classList.add('message-item', 'item-' + typeMessage);
    message.innerHTML = text;
    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
    // Use requestAnimationFrame to ensure the browser has rendered the new message
    // requestAnimationFrame(() => {
    //    messages.scrollTop = messages.scrollHeight;
    // });
  }
};
