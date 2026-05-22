import { BookOpen, FileText, Map, ScrollText } from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';

import type { Surface, TargetDetail as TargetDetailType } from '../types';

type TargetDetailProps = {
  target: TargetDetailType | null;
  loading: boolean;
};

export function TargetDetail({ target, loading }: TargetDetailProps) {
  const [activeSurfacePath, setActiveSurfacePath] = useState('');

  useEffect(() => {
    setActiveSurfacePath(target?.surfaces[0]?.path ?? '');
  }, [target?.slug, target?.surfaces]);

  const activeSurface = useMemo(() => {
    return target?.surfaces.find((surface) => surface.path === activeSurfacePath) ?? target?.surfaces[0] ?? null;
  }, [activeSurfacePath, target?.surfaces]);

  if (loading) {
    return <section className="detail-pane loading-pane">Loading...</section>;
  }

  if (!target) {
    return <section className="detail-pane empty-state">No target selected</section>;
  }

  return (
    <section className="detail-pane">
      <div className="detail-header">
        <div>
          <div className="eyebrow">{target.stage}</div>
          <h2>{target.title}</h2>
        </div>
        <span className="status-pill">{target.status}</span>
      </div>

      <p className="target-brief">{target.purpose}</p>

      <div className="surface-tabs" role="tablist" aria-label="Target surfaces">
        {target.surfaces.map((surface) => (
          <button
            className={`surface-tab ${activeSurface?.path === surface.path ? 'active' : ''}`}
            type="button"
            role="tab"
            aria-selected={activeSurface?.path === surface.path}
            key={`${surface.kind}-${surface.path}`}
            onClick={() => setActiveSurfacePath(surface.path)}
            title={surface.path}
          >
            <SurfaceIcon kind={surface.kind} />
            <span>{surface.label}</span>
          </button>
        ))}
      </div>

      {activeSurface ? <SurfaceReader surface={activeSurface} /> : null}
    </section>
  );
}

function SurfaceReader({ surface }: { surface: Surface }) {
  return (
    <article className="surface-reader">
      <header className="surface-header">
        <div>
          <div className="surface-kind">{surface.kind}</div>
          <h3>{surface.path}</h3>
        </div>
        <span className={`file-state ${surface.exists ? 'exists' : 'missing'}`}>
          {surface.exists ? 'available' : 'missing'}
        </span>
      </header>
      <pre>{surface.content || 'No content'}</pre>
    </article>
  );
}

function SurfaceIcon({ kind }: { kind: string }) {
  if (kind === 'book') {
    return <BookOpen size={16} />;
  }
  if (kind === 'map') {
    return <Map size={16} />;
  }
  if (kind === 'brief') {
    return <ScrollText size={16} />;
  }
  return <FileText size={16} />;
}
