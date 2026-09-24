/** Web Request/Response handler; mount it behind the host app's own auth. */
export function createGeminiTokenHandler({ getApiKey, authorize, model, fetchImpl = fetch, now = Date.now }) {
  if (typeof getApiKey !== 'function' || typeof authorize !== 'function' || !model)
    throw new TypeError('getApiKey、authorize 與 model 為必要項目');
  const json = (body, status) => Response.json(body, { status, headers: { 'Cache-Control': 'no-store' } });
  return async function handle(request) {
    if (request.method !== 'POST') return json({ error: 'POST required' }, 405);
    if (!(await authorize(request))) return json({ error: '未授權' }, 403);
    const apiKey = await getApiKey();
    if (!apiKey) return json({ error: '尚未設定 Gemini API key' }, 503);
    const issuedAt = now();
    const body = {
      uses: 1,
      newSessionExpireTime: new Date(issuedAt + 60_000).toISOString(),
      expireTime: new Date(issuedAt + 30 * 60_000).toISOString(),
    };
    try {
      const upstream = await fetchImpl('https://generativelanguage.googleapis.com/v1beta/auth_tokens', {
        method: 'POST',
        headers: { 'x-goog-api-key': apiKey, 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        signal: AbortSignal.timeout(20_000),
      });
      const payload = await upstream.json().catch(() => ({}));
      if (!upstream.ok || !payload.name)
        return json({ error: `Gemini 權杖申請失敗（HTTP ${upstream.status}）` }, 502);
      return json({ token: payload.name, model, expireTime: payload.expireTime || body.expireTime }, 200);
    } catch {
      return json({ error: 'Gemini 權杖服務暫時無法使用' }, 502);
    }
  };
}

