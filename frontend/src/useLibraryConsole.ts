import { useCallback, useEffect, useState } from 'react';

import { fetchSummary, fetchTarget, fetchTargets, fetchValidation } from './api';
import type { LibrarySummary, TargetDetail, TargetListItem, ValidationStatus } from './types';

type ConsoleState = {
  summary: LibrarySummary | null;
  validation: ValidationStatus | null;
  targets: TargetListItem[];
  activeSlug: string;
  activeTarget: TargetDetail | null;
  loading: boolean;
  detailLoading: boolean;
  error: string;
  selectTarget: (slug: string) => void;
  refresh: () => Promise<void>;
};

export function useLibraryConsole(): ConsoleState {
  const [summary, setSummary] = useState<LibrarySummary | null>(null);
  const [validation, setValidation] = useState<ValidationStatus | null>(null);
  const [targets, setTargets] = useState<TargetListItem[]>([]);
  const [activeSlug, setActiveSlug] = useState('');
  const [activeTarget, setActiveTarget] = useState<TargetDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [error, setError] = useState('');

  const refresh = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const [nextSummary, nextValidation, nextTargets] = await Promise.all([
        fetchSummary(),
        fetchValidation(),
        fetchTargets(),
      ]);
      setSummary(nextSummary);
      setValidation(nextValidation);
      setTargets(nextTargets);
      setActiveSlug((current) => current || nextTargets[0]?.slug || '');
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : 'Unable to load console data');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  useEffect(() => {
    if (!activeSlug) {
      setActiveTarget(null);
      return;
    }

    let cancelled = false;
    setDetailLoading(true);
    setError('');
    fetchTarget(activeSlug)
      .then((detail) => {
        if (!cancelled) {
          setActiveTarget(detail);
        }
      })
      .catch((caught) => {
        if (!cancelled) {
          setError(caught instanceof Error ? caught.message : 'Unable to load target');
        }
      })
      .finally(() => {
        if (!cancelled) {
          setDetailLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [activeSlug]);

  return {
    summary,
    validation,
    targets,
    activeSlug,
    activeTarget,
    loading,
    detailLoading,
    error,
    selectTarget: setActiveSlug,
    refresh,
  };
}
