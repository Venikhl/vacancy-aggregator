import axios from 'axios';
import type { Filters } from '@/types/filters';

export const getVacancies = async (
  offset: number,
  count: number,
  filters: Filters
) => {
  return axios.post('/api/v1/vacancies', {
    filter: filters,
    view: {
      offset,
      count,
    },
  });
};
