import test from 'node:test';
import assert from 'node:assert/strict';
import { createHostBridge } from '../assets/portable/host-bridge.mjs';
import { createGeminiTokenHandler } from '../assets/portable/token-handler.mjs';
import { createGeminiLiveClient } from '../assets/portable/gemini-live-client.mjs';

const makeBridge = (overrides = {}) => createHostBridge({
  getState: async () => ({ page: '首頁' }),
  actions: [{
    name: 'open_panel',
    description: '開啟面板',
    parameters: { type: 'object', properties: { id: { type: 'string' } }, required: ['id'] },
    validate: (args) => typeof args?.id === 'string' || '需要 id',
    run: async ({ id }) => ({ ok: true, id }),
  }],
  ...overrides,
});

test('只暴露宿主註冊的工具與狀態', async () => {
  const host = makeBridge();
  assert.deepEqual(host.declarations.map((item) => item.name), ['read_app_state', 'open_panel']);
  assert.deepEqual(await host.execute('read_app_state'), { ok: true, state: { page: '首頁' } });
  assert.deepEqual(await host.execute('open_panel', { id: '圖層' }), { ok: true, id: '圖層' });
  assert.equal((await host.execute('delete_everything')).ok, false);
  assert.equal((await host.execute('open_panel', {})).ok, false);
});

test('高風險工具必須由宿主確認', async () => {
  let ran = false;
  const host = makeBridge({
    actions: [{
      name: 'delete_item', description: '刪除', risk: 'confirm',
      parameters: { type: 'object', properties: {} },
      validate: () => true,
      run: async () => { ran = true; return { ok: true }; },
    }],
    confirm: async () => false,
  });
  assert.equal((await host.execute('delete_item')).ok, false);
  assert.equal(ran, false);
});

test('後端拒絕未授權、無金鑰及非 POST 請求', async () => {
  const handler = createGeminiTokenHandler({
    model: 'models/test-live', getApiKey: () => '', authorize: () => false,
  });
  assert.equal((await handler(new Request('https://app.example/token', { method: 'GET' }))).status, 405);
  assert.equal((await handler(new Request('https://app.example/token', { method: 'POST' }))).status, 403);
  const noKey = createGeminiTokenHandler({
    model: 'models/test-live', getApiKey: () => '', authorize: () => true,
  });
  assert.equal((await noKey(new Request('https://app.example/token', { method: 'POST' }))).status, 503);
});

test('後端僅回傳短效權杖，長期金鑰不出現在回應', async () => {
  let requestBody;
  const handler = createGeminiTokenHandler({
    model: 'models/test-live', getApiKey: () => 'PRIVATE_API_KEY',
    authorize: () => true, now: () => Date.parse('2026-09-24T00:00:00Z'),
    fetchImpl: async (_url, options) => {
      requestBody = JSON.parse(options.body);
      assert.equal(options.headers['x-goog-api-key'], 'PRIVATE_API_KEY');
      return Response.json({ name: 'short-token' });
    },
  });
  const response = await handler(new Request('https://app.example/token', { method: 'POST' }));
  const body = await response.json();
  assert.equal(response.status, 200);
  assert.equal(body.token, 'short-token');
  assert.equal(body.model, 'models/test-live');
  assert.equal(JSON.stringify(body).includes('PRIVATE_API_KEY'), false);
  assert.equal(requestBody.uses, 1);
});

test('瀏覽器會話可連線、回傳工具結果、分享授權畫面並停止麥克風', async () => {
  const saved = ['navigator', 'window', 'AudioContext', 'AudioWorkletNode'].map((key) => [key, Object.getOwnPropertyDescriptor(globalThis, key)]);
  let trackStopped = false;
  const connectable = () => ({ connect() {}, disconnect() {} });
  class FakeAudio {
    currentTime = 0;
    destination = {};
    audioWorklet = { addModule: async () => {} };
    resume = async () => {};
    close = async () => {};
    createMediaStreamSource = connectable;
    createGain() { return { ...connectable(), gain: { value: 1 } }; }
  }
  class FakeNode {
    port = { onmessage: null };
    connect() {}
    disconnect() {}
  }
  class FakeSocket {
    static OPEN = 1;
    static CLOSING = 2;
    constructor() {
      this.readyState = 1;
      this.bufferedAmount = 0;
      this.sent = [];
      FakeSocket.instance = this;
      queueMicrotask(() => this.onopen?.());
    }
    send(value) {
      this.sent.push(JSON.parse(value));
      if (this.sent.at(-1)?.setup) queueMicrotask(() => this.onmessage?.({ data: JSON.stringify({ setupComplete: {} }) }));
    }
    close() { this.readyState = 3; }
  }
  try {
    Object.defineProperty(globalThis, 'navigator', { configurable: true, value: { mediaDevices: { getUserMedia: async () => ({ getTracks: () => [{ stop: () => { trackStopped = true; } }] }) } } });
    Object.defineProperty(globalThis, 'window', { configurable: true, value: { AudioContext: FakeAudio } });
    Object.defineProperty(globalThis, 'AudioContext', { configurable: true, value: FakeAudio });
    Object.defineProperty(globalThis, 'AudioWorkletNode', { configurable: true, value: FakeNode });
    const host = makeBridge({ getFrame: async () => ({ fresh: true, mimeType: 'image/jpeg', data: 'ZmFrZQ==' }) });
    const client = createGeminiLiveClient({
      host, Socket: FakeSocket,
      fetchImpl: async () => Response.json({ token: 'short-token', model: 'models/test-live' }),
    });
    await client.start();
    assert.equal(client.connected, true);
    assert.equal(FakeSocket.instance.sent[0].setup.model, 'models/test-live');
    FakeSocket.instance.onmessage({ data: JSON.stringify({ toolCall: { functionCalls: [{ name: 'open_panel', id: 'a1', args: { id: '圖層' } }] } }) });
    await new Promise((resolve) => setTimeout(resolve, 0));
    assert.equal(FakeSocket.instance.sent.at(-1).toolResponse.functionResponses[0].response.result.ok, true);
    assert.equal(await client.shareFrame(), false);
    client.setVisualSharing(true);
    assert.equal(await client.shareFrame(), true);
    assert.equal(FakeSocket.instance.sent.at(-1).realtimeInput.video.mimeType, 'image/jpeg');
    client.stop();
    assert.equal(trackStopped, true);
    assert.equal(client.connected, false);
  } finally {
    for (const [key, descriptor] of saved) {
      if (descriptor) Object.defineProperty(globalThis, key, descriptor);
      else delete globalThis[key];
    }
  }
});

