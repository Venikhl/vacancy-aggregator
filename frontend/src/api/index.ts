// api.ts (или где ты определяешь API-запросы)
import axios from "axios";

export const getVacancies = async (
  offset: number,
  count: number,
  filters: any
) => {
  return axios.post("/api/v1/vacancies", {
    filter: filters,
    view: { offset, count } // <-- ВОТ ЗДЕСЬ
  });
};
