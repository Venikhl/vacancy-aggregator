import React from 'react';
import { Button } from '@/components/ui/button';

type VacancyCardProps = {
  title: string;
  company: string;
  location: string;
  salary?: string;
  timeAgo?: string;
};

export const VacancyCard: React.FC<VacancyCardProps> = ({
  title,
  company,
  location,
  salary,
  timeAgo,
}) => {
  return (
    <div
      className="p-5 flex flex-col gap-2 rounded-[var(--radius-xl)] shadow-sm hover:shadow-md transition"
      style={{
        backgroundColor: 'var(--color-card)',
        color: 'var(--color-card-foreground)',
        border: '1px solid var(--color-border)',
      }}
    >
      <div
        className="flex items-center justify-between text-sm"
        style={{ color: 'var(--muted-foreground)' }}
      >
        <span>{timeAgo || 'Parsed recently'}</span>
      </div>

      <div className="flex items-center gap-2">
        <span
          className="text-xs font-semibold px-3 py-1 rounded-full"
          style={{
            backgroundColor: 'var(--color-primary)',
            color: 'var(--color-on-primary)',
          }}
        >
          🔶 {company}
        </span>
      </div>

      <h2 className="text-xl font-semibold">{title}</h2>

      <p style={{ color: 'var(--color-secondary)' }}>{location}</p>

      {salary && (
        <p style={{ color: 'oklch(0.45 0.2 150)' }} className="font-medium">
          {salary}
        </p>
      )}

      <div className="flex justify-end gap-2 mt-3">
        <Button variant="outline" size="sm">
          Сохранить
        </Button>
        <Button variant="default" size="sm">
          Откликнуться
        </Button>
      </div>
    </div>
  );
};
