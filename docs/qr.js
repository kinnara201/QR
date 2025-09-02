// jsQRライブラリをCDNで読み込んでいる前提です

let video = null;
let resultDiv = null;
let scanning = true;
let stream = null;
let scanInterval = null;

window.addEventListener('DOMContentLoaded', async () => {
  video = document.getElementById('qr-video');
  resultDiv = document.getElementById('qr-result');
  if (!resultDiv) {
    // 結果表示用divがなければ作成
    resultDiv = document.createElement('div');
    resultDiv.setAttribute('id', 'qr-result');
    resultDiv.style.textAlign = 'center';
    resultDiv.style.fontSize = '1.2em';
    resultDiv.style.marginTop = '16px';
    document.body.insertBefore(resultDiv, document.querySelector('.footer'));
  }

  // ページ表示時に自動でカメラ起動＆QR読み取り
  video.style.display = 'block';
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
    video.srcObject = stream;
    scanInterval = setInterval(scanQRCode, 300);
  } catch (e) {
    resultDiv.textContent = 'カメラの権限が必要です。';
    scanning = false;
  }
});

// 一致判定用リスト（ここに一致させたい文字列を追加）
const MATCH_LIST = ["テスタ", "テスト", "12345"];

function scanQRCode() {
  if (!video || !video.videoWidth) return;
  let canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  let ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  let imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  if (window.jsQR) {
    let code = jsQR(imageData.data, canvas.width, canvas.height);
    if (code) {
      const matched = MATCH_LIST.filter(item => code.data.includes(item));
      const statusMessage = document.getElementById('status-message');
      if (matched.length > 0) {
        resultDiv.textContent = `一致: ${matched.join(", ")}（QRコード: ${code.data}）`;
        if (statusMessage) statusMessage.textContent = 'お通りください';
      } else {
        resultDiv.textContent = `一致するデータはありません（QRコード: ${code.data}）`;
        if (statusMessage) statusMessage.textContent = 'このQRコードは使用できません';
      }
      scanning = false;
      video.style.display = 'none';
      if (scanInterval) clearInterval(scanInterval);
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
      }
    }
  }
}
