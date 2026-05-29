/**
 * sessionize.ts — Build-time fetch of Martin's Sessionize speaker catalog.
 *
 * Shared by Speaking.astro (homepage) and work.astro (/work) so both surfaces
 * render the same live session list from one fetch path.
 *
 * The fetch is build-time only (Astro static output). It fails soft: on any
 * network error, non-OK status, or empty payload it returns [] and the calling
 * component hides the catalog. A warning is logged so CI build logs show why.
 */

export type SessionizeSession = {
  id: number;
  title: string;
  description: string;
  sessionUrl: string;
  languageCode: string;
  language: string;
};

type SessionizePayload = {
  sessions?: SessionizeSession[];
};

const SESSIONIZE_API = 'https://sessionize.com/api/speaker/json/0q2vfif629';

export async function getSessions(): Promise<SessionizeSession[]> {
  try {
    const res = await fetch(SESSIONIZE_API, { signal: AbortSignal.timeout(10000) });
    if (!res.ok) {
      console.warn(`[sessionize] Sessionize returned HTTP ${res.status}; session catalog hidden in this build.`);
      return [];
    }
    const data = (await res.json()) as SessionizePayload;
    const sessions = data.sessions ?? [];
    if (sessions.length === 0) {
      console.warn('[sessionize] Sessionize returned 0 sessions; session catalog hidden in this build.');
    }
    return sessions;
  } catch (err) {
    const name = err instanceof Error ? err.name : 'error';
    console.warn(`[sessionize] Sessionize fetch failed (${name}); session catalog hidden in this build.`);
    return [];
  }
}

export function summarise(text: string, max = 220): string {
  const clean = text.replace(/\r\n|\r|\n/g, ' ').replace(/\s+/g, ' ').trim();
  if (clean.length <= max) return clean;
  const cut = clean.slice(0, max);
  const lastSpace = cut.lastIndexOf(' ');
  return (lastSpace > 0 ? cut.slice(0, lastSpace) : cut) + '...';
}
