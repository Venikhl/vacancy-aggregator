import React, { useEffect, useState } from 'react';
import { ResumeCard } from '@/components/cards/ResumeCard';
import { ResumeFilters } from '@/components/filters/ResumeFilters';
import { useResumes } from './hooks/useResume';
import { Button } from '@/components/ui/button';
import type { ResumeFilters as Filters } from '@/types/filters';

const defaultFilters: Filters = {
    title: null,
    location: null,
    salary_min: null,
    salary_max: null,
    experience_categories: [],
    skills: [],
};

export const Resume: React.FC = () => {
    const [filters, setFilters] = useState<Filters>(defaultFilters);
    const [currentPage, setCurrentPage] = useState(1);

    const { resumes, loading, totalCount, fetchResumes } = useResumes();

    const RESUMES_PER_PAGE = 15;
    const totalPages = Math.ceil(totalCount / RESUMES_PER_PAGE);

    useEffect(() => {
        const offset = (currentPage - 1) * RESUMES_PER_PAGE;
        fetchResumes(filters, offset, RESUMES_PER_PAGE);
    }, [filters, currentPage, fetchResumes]);

    const handlePageChange = (page: number) => {
        setCurrentPage(page);
    };

    const handleReset = () => {
        setFilters(defaultFilters);
        setCurrentPage(1);
    };

    const handleApplyFilters = () => {
        setCurrentPage(1);
    };

    return (
        <div className="min-h-screen px-4 py-6">
            <div className="max-w-6xl mx-auto space-y-6">
                <ResumeFilters
                    filters={filters}
                    onChange={setFilters}
                    onApply={handleApplyFilters}
                    onReset={handleReset}
                />

                <div className="space-y-6">
                    {loading ? (
                        <p className="text-sm text-muted-foreground animate-pulse">
                            Загрузка резюме...
                        </p>
                    ) : (
                        <>
                            <p className="text-sm text-muted-foreground">
                                Найдено резюме: {totalCount}
                            </p>

                            {resumes.length === 0 ? (
                                <p className="text-muted-foreground italic">
                                    Нет подходящих резюме.
                                </p>
                            ) : (
                                <>
                                    {resumes.map((resume) => {
                                        const {
                                            id,
                                            title,
                                            first_name,
                                            last_name,
                                            middle_name,
                                            salary,
                                            description,
                                        } = resume;

                                        const fullName =
                                            [last_name, first_name, middle_name]
                                                .filter(Boolean)
                                                .join(' ')
                                                .trim() || 'Имя не указано';

                                        return (
                                            <ResumeCard
                                                id={id}
                                                title={title || 'Без названия'}
                                                fullName={
                                                    fullName || 'Имя не указано'
                                                }
                                                salary={
                                                    salary
                                                        ? {
                                                              value:
                                                                  salary.value ??
                                                                  0,
                                                              currency:
                                                                  salary.currency ??
                                                                  'руб.',
                                                              type:
                                                                  salary.type ??
                                                                  '',
                                                          }
                                                        : null
                                                }
                                                description={description ?? ''}
                                            />
                                        );
                                    })}

                                    {totalPages > 1 && (
                                        <div className="flex justify-center gap-2 pt-4 flex-wrap">
                                            <Button
                                                variant="outline"
                                                size="sm"
                                                disabled={currentPage === 1}
                                                onClick={() =>
                                                    handlePageChange(
                                                        currentPage - 1,
                                                    )
                                                }
                                            >
                                                Назад
                                            </Button>

                                            {getPaginationRange(
                                                currentPage,
                                                totalPages,
                                            ).map((page, idx) =>
                                                typeof page === 'number' ? (
                                                    <Button
                                                        key={page}
                                                        variant={
                                                            currentPage === page
                                                                ? 'default'
                                                                : 'outline'
                                                        }
                                                        size="sm"
                                                        onClick={() =>
                                                            handlePageChange(
                                                                page,
                                                            )
                                                        }
                                                    >
                                                        {page}
                                                    </Button>
                                                ) : (
                                                    <span
                                                        key={`dots-${idx}`}
                                                        className="px-2 text-muted-foreground select-none"
                                                    >
                                                        ...
                                                    </span>
                                                ),
                                            )}

                                            <Button
                                                variant="outline"
                                                size="sm"
                                                disabled={
                                                    currentPage === totalPages
                                                }
                                                onClick={() =>
                                                    handlePageChange(
                                                        currentPage + 1,
                                                    )
                                                }
                                            >
                                                Вперёд
                                            </Button>
                                        </div>
                                    )}
                                </>
                            )}
                        </>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Resume;

function getPaginationRange(
    current: number,
    total: number,
): (number | string)[] {
    const delta = 2;
    const range: (number | string)[] = [];
    const rangeWithDots: (number | string)[] = [];

    for (let i = 1; i <= total; i++) {
        if (
            i === 1 ||
            i === total ||
            (i >= current - delta && i <= current + delta)
        ) {
            range.push(i);
        }
    }

    let prev: number | null = null;
    for (const num of range) {
        if (prev !== null && typeof num === 'number') {
            if (num - prev > 1) {
                rangeWithDots.push('...');
            }
        }
        rangeWithDots.push(num);
        if (typeof num === 'number') prev = num;
    }

    return rangeWithDots;
}
