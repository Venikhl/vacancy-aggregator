import { useState, useCallback } from 'react';
import { getVacancies } from '@/api/vacancies.ts';
import type { Filters } from '@/types/filters';

interface Vacancy {
    id: string;
    title: string;
    description: string;
    salary: {
        value: number;
        currency: string;
        type: string;
    } | null;
}

export function useVacancies() {
    const [vacancies, setVacancies] = useState<Vacancy[]>([]);
    const [loading, setLoading] = useState(true);
    const [totalCount, setTotalCount] = useState(0);

    const fetchVacancies = useCallback(
        async (filters: Filters, offset = 0, count = 20) => {
            setLoading(true);
            try {
                const response = await getVacancies(offset, count, filters);
                setVacancies(response.data.vacancies || []);
                setTotalCount(response.data.count || 0);
            } catch (error) {
                console.error('Ошибка при загрузке вакансий:', error);
            } finally {
                setLoading(false);
            }
        },
        [],
    );

    return {
        vacancies,
        loading,
        totalCount,
        fetchVacancies,
    };
}
