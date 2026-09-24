// Adapted from the app's PCM AudioWorklet: resample to 16 kHz off the UI thread.
class PortablePcmCapture extends AudioWorkletProcessor {
  constructor() {
    super();
    this.samples = new Int16Array(1024);
    this.index = 0;
    this.phase = 0;
  }
  process(inputs) {
    const input = inputs[0]?.[0];
    if (!input) return true;
    for (const sample of input) {
      this.phase += 16000;
      if (this.phase < sampleRate) continue;
      this.phase -= sampleRate;
      const value = Math.max(-1, Math.min(1, sample));
      this.samples[this.index++] = value < 0 ? value * 32768 : value * 32767;
      if (this.index === this.samples.length) {
        this.port.postMessage(this.samples.buffer, [this.samples.buffer]);
        this.samples = new Int16Array(1024);
        this.index = 0;
      }
    }
    return true;
  }
}
registerProcessor('portable-gemini-pcm', PortablePcmCapture);

