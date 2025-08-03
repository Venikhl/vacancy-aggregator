import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
} from '@/components/ui/dialog';
import { getResumeById } from '@/api/resume';

type ResumeCardProps = {
    id: number;
    title: string;
    description: string;
    salary?: {
        type: string | null;
        currency: string;
        value: number;
    } | null;
    fullName?: string | null;
};

type ResumeDetails = {
    id: number;
    title: string;
    description?: string;
    salary?: {
        type: string | null;
        currency: string | null;
        value: number | null;
    } | null;
    location?: {
        region?: string;
    } | null;
    experience_category?: {
        name?: string;
    } | null;
    education?: string | null;
    published_at?: {
        time_stamp?: string;
    };
    phone_number?: string | null;
    email?: string | null;
};

function formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
    });
}

export const ResumeCard: React.FC<ResumeCardProps> = ({
    id,
    title,
    description,
    salary,
    fullName,
}) => {
    const [open, setOpen] = useState(false);
    const [details, setDetails] = useState<ResumeDetails | null>(null);
    const [loading, setLoading] = useState(false);

    const handleOpen = async () => {
        setOpen(true);
        setLoading(true);
        try {
            const res = await getResumeById(id);
            setDetails(res.data);
        } catch (e) {
            console.error('Ошибка получения резюме:', e);
            setDetails(null);
        }
        setLoading(false);
    };

    let salaryString: string | null = null;
    if (salary && typeof salary.value === 'number' && salary.currency) {
        salaryString = `${salary.value.toLocaleString()} ${salary.currency} ${salary.type || ''}`;
    }

    return (
        <>
            <div className="bg-white border border-gray-200 rounded-xl p-5 flex flex-col gap-3 shadow-sm hover:shadow-md transition">
                {/* <h2 className="text-xl font-semibold text-gray-900">
                    {title || 'Без названия'}
                </h2> */}
                {fullName && (
                    <div className="flex items-center gap-2">
                        <span className="bg-primary text-white text-xs font-semibold px-3 py-1 rounded-full">
                            👤 {fullName}
                        </span>
                    </div>
                )}
                <p className="text-green-600 font-medium">
                    Желаемая зарплата: {salaryString}
                </p>
                {description && (
                    <p className="text-gray-800 text-sm whitespace-pre-line line-clamp-5">
                        {description}
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
                        {details?.location?.region && (
                            <DialogDescription className="text-sm text-[var(--color-muted-foreground)]">
                                {details.location.region}
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
                                {details.education && (
                                    <div className="sm:col-span-2">
                                        <div className="text-xs text-muted-foreground uppercase mb-1">
                                            Образование
                                        </div>
                                        <div>{details.education}</div>
                                    </div>
                                )}
                                {details.published_at?.time_stamp && (
                                    <div>
                                        <div className="text-xs text-muted-foreground uppercase mb-1">
                                            Обновлено
                                        </div>
                                        <div>
                                            {formatDate(
                                                details.published_at.time_stamp,
                                            )}
                                        </div>
                                    </div>
                                )}
                                {(details.phone_number || details.email) && (
                                    <div className="sm:col-span-2">
                                        <div className="text-xs text-muted-foreground uppercase mb-1">
                                            Контакты
                                        </div>
                                        <div className="flex flex-col gap-1">
                                            {details.phone_number && (
                                                <div>
                                                    📞 {details.phone_number}
                                                </div>
                                            )}
                                            {details.email && (
                                                <div>📧 {details.email}</div>
                                            )}
                                        </div>
                                    </div>
                                )}
                            </div>

                            {details.description && (
                                <div className="border rounded-md p-4 bg-muted/50 text-[var(--color-card-foreground)]">
                                    {details.description}
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="text-sm text-destructive">
                            Не удалось загрузить данные резюме
                        </div>
                    )}
                </DialogContent>
            </Dialog>
        </>
    );
};
