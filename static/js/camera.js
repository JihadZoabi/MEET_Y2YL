        var videoElement = document.querySelector('video');
        var videoSelect = document.querySelector('select#videoSource');


        videoSelect.onchange = getStream;

        getStream().then(getDevices).then(gotDevices);

        function getDevices() {
          // AFAICT in Safari this only gets default devices until gUM is called :/
          return navigator.mediaDevices.enumerateDevices();
        }

        function gotDevices(deviceInfos) {
          window.deviceInfos = deviceInfos; // make available to console
          console.log('Available input and output devices:', deviceInfos);
          for (const deviceInfo of deviceInfos) {
            const option = document.createElement('option');
            option.value = deviceInfo.deviceId;
            if (deviceInfo.kind === 'videoinput') {
              option.text = deviceInfo.label || `Camera ${videoSelect.length + 1}`;
              videoSelect.appendChild(option);
            }
          }
        }

        function getStream() {
          if (window.stream) {
            window.stream.getTracks().forEach(track => {
              track.stop();
            });
          }
          const videoSource = videoSelect.value;
          const constraints = {
            video: {deviceId: videoSource ? {exact: videoSource} : undefined}
          };
          return navigator.mediaDevices.getUserMedia(constraints).
            then(gotStream).catch(handleError);
        }

        function gotStream(stream) {
          window.stream = stream; // make stream available to console
          videoSelect.selectedIndex = [...videoSelect.options].
            findIndex(option => option.text === stream.getVideoTracks()[0].label);
          videoElement.srcObject = stream;
        }

        function handleError(error) {
          console.error('Error: ', error);
        }

        const captureVideoButton = document.querySelector(
  "#screenshot .capture-button"
);
const screenshotButton = document.querySelector("#screenshot-button");
const img = document.querySelector("#screenshot img");
const video = document.querySelector("#screenshot video");

const canvas = document.createElement("canvas");

captureVideoButton.onclick = function () {
// -1 (nothing) - 0 (cam) - 1 (obs)
    var dict = {0:1, 1:0};
    var option_tag = document.getElementById("videoSource");
    if (option_tag.selectedIndex + 1 < 0)
        option_tag.selectedIndex += 2;
    else
        option_tag.selectedIndex += 1;
    videoSelect.onchange = getStream;
    getStream();
};

screenshotButton.onclick = video.onclick = function () {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0);
  // Other browsers will fall back to image/png
  img.src = canvas.toDataURL("image/webp");
  document.getElementById("imgLink").value = img.src;
  console.log(canvas.toDataURL("image/jpeg"));
};

function handleSuccess(stream) {
  screenshotButton.disabled = false;
  video.srcObject = stream;
}
