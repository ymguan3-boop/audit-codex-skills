/** Optional consented browser-tab frame source. Call start() from a user click. */
export function createTabFrameProvider({ maxPixels = 960 * 540, maxBase64Chars = 300_000 } = {}) {
  let stream = null;
  let video = null;

  function stop() {
    stream?.getTracks().forEach((track) => track.stop());
    if (video) video.srcObject = null;
    stream = video = null;
  }

  async function start() {
    if (!navigator.mediaDevices?.getDisplayMedia) throw new Error('此瀏覽器不支援分頁分享');
    stop();
    const acquired = await navigator.mediaDevices.getDisplayMedia({
      video: { displaySurface: 'browser' }, audio: false,
      preferCurrentTab: true, selfBrowserSurface: 'include',
    });
    const track = acquired.getVideoTracks()[0];
    // The browser may ignore hints. Fail closed if the user chose a screen/window.
    if (!track || track.getSettings().displaySurface !== 'browser') {
      acquired.getTracks().forEach((item) => item.stop());
      throw new Error('請在分享視窗中選擇瀏覽器分頁，不要分享整個螢幕');
    }
    stream = acquired;
    video = document.createElement('video');
    video.muted = true;
    video.playsInline = true;
    video.srcObject = stream;
    track.addEventListener('ended', stop, { once: true });
    try {
      await video.play();
    } catch (error) {
      stop();
      throw error;
    }
  }

  async function getFrame({ signal } = {}) {
    const track = stream?.getVideoTracks()[0];
    if (!track || track.readyState !== 'live' || document.hidden || !video) return null;
    if (typeof video.requestVideoFrameCallback !== 'function') return null;
    const currentVideo = video;
    const fresh = await new Promise((resolve) => {
      const timeout = setTimeout(() => resolve(false), 1500);
      const frameId = currentVideo.requestVideoFrameCallback(() => {
        clearTimeout(timeout);
        resolve(true);
      });
      signal?.addEventListener('abort', () => {
        clearTimeout(timeout);
        currentVideo.cancelVideoFrameCallback?.(frameId);
        resolve(false);
      }, { once: true });
    });
    if (!fresh || signal?.aborted || video !== currentVideo || track.readyState !== 'live') return null;
    const width = currentVideo.videoWidth;
    const height = currentVideo.videoHeight;
    if (!width || !height) return null;
    const scale = Math.min(1, Math.sqrt(maxPixels / (width * height)));
    const canvas = document.createElement('canvas');
    canvas.width = Math.max(1, Math.floor(width * scale));
    canvas.height = Math.max(1, Math.floor(height * scale));
    const context = canvas.getContext('2d');
    if (!context) return null;
    context.drawImage(currentVideo, 0, 0, canvas.width, canvas.height);
    const dataUrl = canvas.toDataURL('image/jpeg', 0.7);
    const data = dataUrl.slice(dataUrl.indexOf(',') + 1);
    if (data.length > maxBase64Chars) return null;
    return { fresh: true, mimeType: 'image/jpeg', data };
  }

  return { start, stop, getFrame, get active() { return !!stream; } };
}

