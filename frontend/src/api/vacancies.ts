import type { Filters } from '@/types/filters';
import axiosInstance from '.';

export const getVacancies = async (
    offset: number,
    count: number,
    filters: Filters,
) => {
    return axiosInstance.post('/vacancies', {
        filter: filters,
        view: {
            offset,
            count,
        },
    });
};

export const getVacancyById = async (id: number | string) => {
    return axiosInstance.get(`/vacancy/${id}`);
};
