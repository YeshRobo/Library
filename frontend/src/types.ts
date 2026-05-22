export type ValidationFinding = {
  level: string;
  path: string;
  message: string;
};

export type ValidationStatus = {
  ok: boolean;
  findings: ValidationFinding[];
};

export type LibrarySummary = {
  targetCount: number;
  sourceCount: number;
  bookCount: number;
  validation: {
    ok: boolean;
    findingCount: number;
  };
};

export type TargetListItem = {
  slug: string;
  title: string;
  purpose: string;
  brief: string;
  status: string;
  stage: string;
  sourceEntries: string[];
  evidenceEntries: string[];
  paths: Record<string, string>;
};

export type Surface = {
  kind: string;
  label: string;
  path: string;
  exists: boolean;
  content: string;
};

export type TargetDetail = TargetListItem & {
  seed: Record<string, unknown>;
  map: Record<string, unknown>;
  memberFiles: unknown[];
  surfaces: Surface[];
};
