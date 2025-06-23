import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  DialogClose,
} from '@/components/ui/dialog';
import { getVacancyById } from '@/api';

type VacancyCardProps = {
  id: number | string;
  title: string;
  company?: string;
  location?: string;
  salary?: string;
};

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
}

export const VacancyCard: React.FC<VacancyCardProps> = ({
  id,
  title,
  company,
  location,
  salary,
}) => {
  const [open, setOpen] = useState(false);
  const [details, setDetails] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleOpen = async () => {
    setOpen(true);
    setLoading(true);
    try {
      const res = await getVacancyById(id);
      setDetails(res.data);
    } catch (e) {
      setDetails(null);
    }
    setLoading(false);
  };

  return (
    <>
      <div
        className="p-5 flex flex-col gap-2 rounded-xl shadow-sm hover:shadow-md transition border"
        style={{
          backgroundColor: 'var(--color-card)',
          color: 'var(--color-card-foreground)',
          borderColor: 'var(--color-border)',
        }}
      >
        <h2 className="text-lg font-semibold">{title}</h2>
        {company && <p className="text-sm">{company}</p>}
        {location && <p className="text-sm">{location}</p>}
        {salary && (
          <p className="text-base font-medium text-[var(--color-accent-foreground)]">
            {salary}
          </p>
        )}

        <div className="flex justify-end gap-2 mt-4">
          <Button variant="outline" size="sm">
            Сохранить
          </Button>
          <Button variant="default" size="sm" onClick={handleOpen}>
            Подробнее
          </Button>
        </div>
      </div>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent
          className="max-w-2xl max-h-[80vh] overflow-y-auto border"
          style={{
            backgroundColor: 'var(--color-card)',
            color: 'var(--color-card-foreground)',
            borderColor: 'var(--color-border)',
          }}
        >
          <DialogHeader>
            <DialogTitle className="text-xl">{details?.title || title}</DialogTitle>
            {details?.company && (
              <DialogDescription className="text-sm text-[var(--color-muted-foreground)]">
                {details.company}
              </DialogDescription>
            )}
          </DialogHeader>

          {loading ? (
            <div className="text-sm">Загрузка...</div>
          ) : details ? (
            <div className="space-y-4 text-sm">
              {details.salary?.value && (
                <div>
                  <span className="font-medium">Зарплата: </span>
                  {details.salary.value.toLocaleString()} {details.salary.currency}
                  {details.salary.type ? ` (${details.salary.type.toLowerCase()})` : ''}
                </div>
              )}
              {details.location?.region && (
                <div>
                  <span className="font-medium">Регион: </span>
                  {details.location.region}
                </div>
              )}
              {details.experience_category?.name && (
                <div>
                  <span className="font-medium">Опыт: </span>
                  {details.experience_category.name}
                </div>
              )}
              {details.specialization?.specialization && (
                <div>
                  <span className="font-medium">Специализация: </span>
                  {details.specialization.specialization}
                </div>
              )}
              {details.published_at?.time_stamp && (
                <div>
                  <span className="font-medium">Опубликовано: </span>
                  {formatDate(details.published_at.time_stamp)}
                </div>
              )}
              {details.description && (
                <div
                  className="prose prose-sm max-w-none"
                  style={{ color: 'var(--color-card-foreground)' }}
                  dangerouslySetInnerHTML={{ __html: details.description }}
                />
              )}
              {details.url && (
                <div>
                  <a
                    href={details.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="underline"
                    style={{ color: 'var(--color-accent-foreground)' }}
                  >
                    Открыть вакансию на сайте
                  </a>
                </div>
              )}
            </div>
          ) : (
            <div className="text-sm text-[var(--color-destructive)]">Ошибка загрузки данных</div>
          )}

          <DialogFooter className="pt-4">
            <DialogClose asChild>
              <Button variant="outline">Закрыть</Button>
            </DialogClose>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
};
