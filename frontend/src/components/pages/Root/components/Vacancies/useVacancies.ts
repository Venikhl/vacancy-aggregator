import { useState, useCallback } from 'react';
import { getVacancies, getVacancyById } from '@/api/vacancies';
import type { Filters } from '@/types/filters';

interface Vacancy {
    id: number | string;
    title: string;
    url?: string;
    company?: { name?: string };
    source?: { name?: string };
    description?: string;
    experience_category?: { name?: string };
    location?: { region?: string };
    [key: string]: unknown;
}

export function useVacancies() {
    const [vacancies, setVacancies] = useState<Vacancy[]>([]);
    const [loading, setLoading] = useState(true);
    const [totalCount, setTotalCount] = useState(0);

    const fetchVacancies = useCallback(async (filters: Filters, count = 20) => {
        setLoading(true);
        try {
            const initialRes = await getVacancies(0, 1, filters);
            const total = initialRes.data.count || 0;
            setTotalCount(total);

            if (total === 0) {
                setVacancies([]);
                return;
            }

            const maxOffset = Math.max(0, total - count);
            const randomOffset = Math.floor(Math.random() * (maxOffset + 1));

            const res = await getVacancies(randomOffset, count, filters);
            const ids = res.data.vacancies.map((v: Vacancy) => v.id);

            const detailedVacancies = await Promise.all(
                ids.map((id: number | string) =>
                    getVacancyById(id).then((res) => res.data as Vacancy),
                ),
            );

            setVacancies(detailedVacancies);
        } catch (error) {
            console.error('Ошибка при загрузке случайных вакансий:', error);
        } finally {
            setLoading(false);
        }
    }, []);

    return {
        vacancies,
        loading,
        totalCount,
        fetchVacancies,
    };
}
