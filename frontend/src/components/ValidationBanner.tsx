import { AlertTriangle, CheckCircle2 } from 'lucide-react';

import type { ValidationStatus } from '../types';

type ValidationBannerProps = {
  validation: ValidationStatus | null;
};

export function ValidationBanner({ validation }: ValidationBannerProps) {
  if (!validation) {
    return null;
  }

  if (validation.ok) {
    return (
      <div className="validation-banner ok">
        <CheckCircle2 size={18} />
        <span>Validation passing</span>
      </div>
    );
  }

  return (
    <div className="validation-banner warn">
      <div className="validation-summary">
        <AlertTriangle size={18} />
        <span>{validation.findings.length} validation finding{validation.findings.length === 1 ? '' : 's'}</span>
      </div>
      <ul>
        {validation.findings.slice(0, 4).map((finding) => (
          <li key={`${finding.path}-${finding.message}`}>
            <strong>{finding.path}</strong>: {finding.message}
          </li>
        ))}
      </ul>
    </div>
  );
}
