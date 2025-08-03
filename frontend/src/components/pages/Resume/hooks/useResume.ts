import { useState, useCallback } from 'react';
import { getResumes } from '@/api/resume';
import type { ResumeFilters } from '@/types/filters';

export interface Resume {
    id: number;
    title: string | null;
    description: string | null;
    first_name: string | null;
    last_name: string | null;
    middle_name?: string | null;
    location: { region: string } | null;
    experience_category: { name: string } | null;
    skills: string[];
    salary: { value: number; currency: string; type?: string | null } | null;
    published_at: string;
}

export function useResumes() {
    const [resumes, setResumes] = useState<Resume[]>([]);
    const [loading, setLoading] = useState(true);
    const [totalCount, setTotalCount] = useState(0);

    const fetchResumes = useCallback(
        async (filters: ResumeFilters, offset = 0, count = 15) => {
            setLoading(true);
            try {
                const response = await getResumes(offset, count, filters);
                const data = response.data;

                if (Array.isArray(data.resumes)) {
                    setResumes(data.resumes);
                    setTotalCount(data.count || 0);
                } else {
                    setResumes([]);
                    setTotalCount(0);
                }
            } catch (error) {
                console.error('Ошибка при загрузке резюме:', error);
                setResumes([]);
                setTotalCount(0);
            } finally {
                setLoading(false);
            }
        },
        [],
    );

    return {
        resumes,
        loading,
        totalCount,
        fetchResumes,
    };
}
