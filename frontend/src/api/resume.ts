import type { ResumeFilters } from '@/types/filters';
import axiosInstance from '.';

export const getResumes = async (
    offset: number,
    count: number,
    filters: ResumeFilters,
) => {
    return axiosInstance.post('/resumes', {
        filter: filters,
        view: {
            offset,
            count,
        },
    });
};

export const getResumeById = async (id: number | string) => {
    return axiosInstance.get(`/resume/${id}`);
};
