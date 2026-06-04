export async function status() {
  const r = await fetch('/valves/status');
  return r.json();
}

export function action(id, path, body) {
  return fetch(`/valve/${encodeURIComponent(id)}/${path}`, { method: 'POST', body });
}
