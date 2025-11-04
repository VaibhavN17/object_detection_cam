const video = document.getElementById("camera");
const canvas = document.getElementById("canvas");
const resultImg = document.getElementById("result");

// request camera access
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  })
  .catch(err => {
    alert("Camera access denied: " + err);
  });

async function sendFrame() {
  const ctx = canvas.getContext("2d");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  const blob = await new Promise(resolve => canvas.toBlob(resolve, "image/jpeg"));
  const formData = new FormData();
  formData.append("frame", blob);

  const response = await fetch("/detect", {
    method: "POST",
    body: formData
  });

  if (response.ok) {
    const imgBlob = await response.blob();
    resultImg.src = URL.createObjectURL(imgBlob);
  }
}

// send frame every 500 ms
setInterval(sendFrame, 500);
