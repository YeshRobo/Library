import { BookOpen, CheckCircle2, Database, FileText, Library, RefreshCw, Search } from 'lucide-react';
import type { ReactNode } from 'react';
import { useMemo, useState } from 'react';

import { TargetDetail } from './components/TargetDetail';
import { TargetList } from './components/TargetList';
import { ValidationBanner } from './components/ValidationBanner';
import { useLibraryConsole } from './useLibraryConsole';

export function App() {
  const [query, setQuery] = useState('');
  const {
    summary,
    validation,
    targets,
    activeSlug,
    activeTarget,
    loading,
    detailLoading,
    error,
    selectTarget,
    refresh,
  } = useLibraryConsole();

  const filteredTargets = useMemo(() => {
    const normalized = query.trim().toLowerCase();
    if (!normalized) {
      return targets;
    }
    return targets.filter((target) => {
      return [target.title, target.purpose, target.slug, target.stage]
        .join(' ')
        .toLowerCase()
        .includes(normalized);
    });
  }, [query, targets]);

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand-block">
          <div className="brand-icon" aria-hidden="true">
            <Library size={20} />
          </div>
          <div>
            <div className="eyebrow">Library Console</div>
            <h1>Knowledge Library</h1>
          </div>
        </div>
        <button className="icon-button" type="button" onClick={() => void refresh()} title="Refresh console data">
          <RefreshCw size={18} />
          <span>Refresh</span>
        </button>
      </header>

      {error ? <div className="error-banner">{error}</div> : null}
      <ValidationBanner validation={validation} />

      <section className="metrics" aria-label="Library summary">
        <Metric icon={<Database size={18} />} label="Targets" value={summary?.targetCount ?? 0} />
        <Metric icon={<FileText size={18} />} label="Sources" value={summary?.sourceCount ?? 0} />
        <Metric icon={<BookOpen size={18} />} label="Books" value={summary?.bookCount ?? 0} />
        <Metric
          icon={<CheckCircle2 size={18} />}
          label="Findings"
          value={summary?.validation.findingCount ?? 0}
          tone={summary?.validation.ok ? 'good' : 'warn'}
        />
      </section>

      <section className="workspace-grid">
        <aside className="target-pane">
          <label className="search-box">
            <Search size={17} />
            <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search targets" />
          </label>
          <TargetList
            targets={filteredTargets}
            activeSlug={activeSlug}
            loading={loading}
            onSelect={selectTarget}
          />
        </aside>
        <TargetDetail target={activeTarget} loading={detailLoading} />
      </section>
    </main>
  );
}

type MetricProps = {
  icon: ReactNode;
  label: string;
  value: number;
  tone?: 'good' | 'warn';
};

function Metric({ icon, label, value, tone }: MetricProps) {
  return (
    <div className={`metric ${tone ?? ''}`}>
      <div className="metric-icon" aria-hidden="true">
        {icon}
      </div>
      <div>
        <div className="metric-value">{value}</div>
        <div className="metric-label">{label}</div>
      </div>
    </div>
  );
}
