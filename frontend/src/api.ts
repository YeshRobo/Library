import type { LibrarySummary, TargetDetail, TargetListItem, ValidationStatus } from './types';

const apiBase = import.meta.env.VITE_LIBRARY_API_URL ?? 'http://127.0.0.1:8000';

export async function fetchSummary(): Promise<LibrarySummary> {
  return request('/api/library/summary');
}

export async function fetchValidation(): Promise<ValidationStatus> {
  return request('/api/library/validation');
}

export async function fetchTargets(): Promise<TargetListItem[]> {
  return request('/api/library/knowledge');
}

export async function fetchTarget(slug: string): Promise<TargetDetail> {
  return request(`/api/library/knowledge/${encodeURIComponent(slug)}`);
}

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${apiBase}${path}`);
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}`);
  }
  return response.json() as Promise<T>;
}
