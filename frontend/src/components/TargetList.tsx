import { BookMarked, CircleDot } from 'lucide-react';

import type { TargetListItem } from '../types';

type TargetListProps = {
  targets: TargetListItem[];
  activeSlug: string;
  loading: boolean;
  onSelect: (slug: string) => void;
};

export function TargetList({ targets, activeSlug, loading, onSelect }: TargetListProps) {
  if (loading) {
    return <div className="empty-state">Loading...</div>;
  }

  if (targets.length === 0) {
    return <div className="empty-state">No targets</div>;
  }

  return (
    <div className="target-list">
      {targets.map((target) => (
        <button
          className={`target-row ${activeSlug === target.slug ? 'active' : ''}`}
          type="button"
          key={target.slug}
          onClick={() => onSelect(target.slug)}
        >
          <span className="target-row-icon" aria-hidden="true">
            <BookMarked size={18} />
          </span>
          <span className="target-row-main">
            <span className="target-row-title">{target.title}</span>
            <span className="target-row-brief">{target.purpose}</span>
            <span className="target-row-meta">
              <CircleDot size={11} /> {target.stage} · {target.sourceEntries.length} source
              {target.sourceEntries.length === 1 ? '' : 's'}
            </span>
          </span>
        </button>
      ))}
    </div>
  );
}
