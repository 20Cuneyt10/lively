const canvas = document.getElementById("visualizer");
const startButton = document.getElementById("startButton");
const context = canvas.getContext("2d");

let audioContext;
let analyser;
let source;
let dataArray;

function resizeCanvas() {
  const pixelRatio = Math.min(window.devicePixelRatio || 1, 2);
  const width = Math.floor(window.innerWidth * pixelRatio);
  const height = Math.floor(window.innerHeight * pixelRatio);

  if (canvas.width !== width || canvas.height !== height) {
    canvas.width = width;
    canvas.height = height;
  }
}

function clearCanvas() {
  context.fillStyle = "#050505";
  context.fillRect(0, 0, canvas.width, canvas.height);
}

function drawWaveform() {
  if (!analyser || !dataArray) {
    return;
  }

  resizeCanvas();
  clearCanvas();

  analyser.getByteTimeDomainData(dataArray);

  const width = canvas.width;
  const height = canvas.height;
  const centerY = height / 2;
  const step = width / (dataArray.length - 1);

  context.lineWidth = Math.max(2, Math.floor(height * 0.004));
  context.strokeStyle = "#57ff9a";
  context.shadowColor = "rgba(87, 255, 154, 0.8)";
  context.shadowBlur = 18;
  context.beginPath();

  for (let i = 0; i < dataArray.length; i += 1) {
    const normalized = dataArray[i] / 128.0;
    const y = normalized * (height * 0.28);
    const x = i * step;

    if (i === 0) {
      context.moveTo(x, centerY + y);
    } else {
      context.lineTo(x, centerY + y);
    }
  }

  context.stroke();
  context.shadowBlur = 0;

  context.strokeStyle = "rgba(87, 255, 154, 0.16)";
  context.beginPath();
  context.moveTo(0, centerY);
  context.lineTo(width, centerY);
  context.stroke();

  window.requestAnimationFrame(drawWaveform);
}

async function startVisualizer() {
  startButton.disabled = true;

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    audioContext = new window.AudioContext();
    analyser = audioContext.createAnalyser();
    analyser.fftSize = 2048;
    dataArray = new Uint8Array(analyser.fftSize);

    source = audioContext.createMediaStreamSource(stream);
    source.connect(analyser);

    startButton.remove();
    drawWaveform();
  } catch (error) {
    startButton.disabled = false;
    startButton.textContent = "Mic access denied";
    console.error(error);
  }
}

window.addEventListener("resize", resizeCanvas);
startButton.addEventListener("click", startVisualizer);
resizeCanvas();
clearCanvas();