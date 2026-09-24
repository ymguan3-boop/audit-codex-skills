/** Register only capabilities the host app intentionally exposes to Gemini. */
export function createHostBridge({ actions, getState, getFrame, confirm } = {}) {
  if (!Array.isArray(actions) || typeof getState !== 'function')
    throw new TypeError('actions 與 getState 為必要項目');
  const registry = new Map();
  for (const action of actions) {
    if (!/^[a-z][a-z0-9_]{0,63}$/.test(action?.name || '') || action.name === 'read_app_state' || registry.has(action.name))
      throw new TypeError('工具名稱無效或重複');
    if (typeof action.run !== 'function' || typeof action.validate !== 'function')
      throw new TypeError(`${action.name} 必須提供 run 與 validate`);
    if (!action.parameters || typeof action.description !== 'string')
      throw new TypeError(`${action.name} 缺少 schema 或說明`);
    registry.set(action.name, action);
  }

  const declarations = [
    {
      name: 'read_app_state',
      description: '讀取宿主程式目前已授權、已遮蔽敏感資料的狀態。不能代替畫面截圖。',
      parameters: { type: 'object', properties: {} },
    },
    ...actions.map(({ name, description, parameters }) => ({ name, description, parameters })),
  ];

  return {
    declarations,
    getFrame: typeof getFrame === 'function' ? getFrame : null,
    async execute(name, args = {}, { signal } = {}) {
      if (signal?.aborted) throw signal.reason || new DOMException('已取消', 'AbortError');
      if (name === 'read_app_state') return { ok: true, state: await getState({ signal }) };
      const action = registry.get(name);
      if (!action) return { ok: false, error: '未授權或不存在的工具' };
      const valid = await action.validate(args);
      if (valid !== true) return { ok: false, error: typeof valid === 'string' ? valid : '參數不合法' };
      if (action.risk === 'confirm') {
        if (typeof confirm !== 'function' || !(await confirm({ action: name, args, signal })))
          return { ok: false, error: '使用者未核准此操作' };
      }
      if (signal?.aborted) throw signal.reason || new DOMException('已取消', 'AbortError');
      try {
        const result = await action.run(args, { signal });
        if (signal?.aborted) throw signal.reason || new DOMException('已取消', 'AbortError');
        return result;
      } catch (error) {
        return { ok: false, error: error?.message || '操作失敗' };
      }
    },
  };
}

