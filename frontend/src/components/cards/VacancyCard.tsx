import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
} from '@/components/ui/dialog';
import { getVacancyById } from '@/api/vacancies.ts';

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
type VacancyDetails = {
    id: number | string;
    title: string;
    company?: {
        name: string;
    };
    location?: {
        region?: string;
    };
    salary?: {
        value?: number;
        currency?: string;
        type?: string;
    };
    experience_category?: {
        name?: string;
    };
    specialization?: {
        specialization?: string;
    };
    published_at?: {
        time_stamp?: string;
    };
    description?: string;
    url?: string;
};

export const VacancyCard: React.FC<VacancyCardProps> = ({
    id,
    title,
    company,
    location,
    salary,
}) => {
    const [open, setOpen] = useState(false);
    const [details, setDetails] = useState<VacancyDetails | null>(null);
    const [loading, setLoading] = useState(false);

    const handleOpen = async () => {
        setOpen(true);
        setLoading(true);
        try {
            const res = await getVacancyById(id);
            console.log(res);
            setDetails(res.data as VacancyDetails);
        } catch (e: unknown) {
            if (e instanceof Error) {
                console.log(e.message);
            } else {
                console.log(String(e));
            }
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
                        <DialogTitle className="text-xl">
                            {details?.title || title}
                        </DialogTitle>
                        {details?.company && (
                            <DialogDescription className="text-sm text-[var(--color-muted-foreground)]">
                                {details.company.name}
                            </DialogDescription>
                        )}
                    </DialogHeader>

                    {loading ? (
                        <div className="text-sm text-muted-foreground">
                            Загрузка...
                        </div>
                    ) : details ? (
                        <div className="space-y-6 text-sm leading-relaxed">
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                {details.salary?.value && (
                                    <div>
                                        <div className="text-xs text-muted-foreground uppercase mb-1">
                                            Зарплата
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <span>
                                                {details.salary.value.toLocaleString()}{' '}
                                                {details.salary.currency}
                                            </span>
                                            {details.salary.type && (
                                                <span className="text-xs bg-muted text-muted-foreground px-2 py-0.5 rounded">
                                                    {details.salary.type.toLowerCase()}
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                )}
                                {details.location?.region && (
                                    <div>
                                        <div className="text-xs text-muted-foreground uppercase mb-1">
                                            Регион
                                        </div>
                                        <div>{details.location.region}</div>
                                    </div>
                                )}
                                {details.experience_category?.name && (
                                    <div>
                                        <div className="text-xs text-muted-foreground uppercase mb-1">
                                            Опыт
                                        </div>
                                        <div>
                                            {details.experience_category.name}
                                        </div>
                                    </div>
                                )}
                                {details.specialization?.specialization && (
                                    <div>
                                        <div className="text-xs text-muted-foreground uppercase mb-1">
                                            Специализация
                                        </div>
                                        <div>
                                            {
                                                details.specialization
                                                    .specialization
                                            }
                                        </div>
                                    </div>
                                )}
                                {details.published_at?.time_stamp && (
                                    <div>
                                        <div className="text-xs text-muted-foreground uppercase mb-1">
                                            Опубликовано
                                        </div>
                                        <div>
                                            {formatDate(
                                                details.published_at.time_stamp,
                                            )}
                                        </div>
                                    </div>
                                )}
                            </div>

                            {details.description && (
                                <div className="border rounded-md p-4 bg-muted/50 text-[var(--color-card-foreground)]">
                                    <div
                                        className="text-sm leading-relaxed whitespace-pre-wrap"
                                        dangerouslySetInnerHTML={{
                                            __html: details.description,
                                        }}
                                    />
                                </div>
                            )}

                            {details.url && (
                                <div className="pt-2 text-end">
                                    <a
                                        href={details.url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        <Button
                                            variant="default"
                                            className="w-full"
                                        >
                                            Перейти на сайт вакансии
                                        </Button>
                                    </a>
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="text-sm text-destructive">
                            Ошибка загрузки данных
                        </div>
                    )}
                </DialogContent>
            </Dialog>
        </>
    );
};
