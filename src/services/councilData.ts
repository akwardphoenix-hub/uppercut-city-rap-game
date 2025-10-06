// Re-export from councilService for backward compatibility
export { getProposals, type Proposal } from './councilService';

export async function saveVoteLocally(entry: unknown) {
  // In dev: mirror to localStorage to keep tests hermetic
  const key = 'council-votes';
  const cur = JSON.parse(localStorage.getItem(key) || '[]');
  cur.push(entry);
  localStorage.setItem(key, JSON.stringify(cur));
}
