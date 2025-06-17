import { useState } from "react";
import { getVacancies } from "@/api";
import type { Filters } from "@/types/filters";

interface Vacancy {
  id: string;
  title: string;
  salary: {
    value: number;
    currency: string;
  } | null;
}

export function useVacancies() {
  const [vacancies, setVacancies] = useState<Vacancy[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchVacancies = async (
    filters: Filters = {},
    offset = 0,
    count = 20
  ) => {
    setLoading(true);
    try {
      const response = await getVacancies(offset, count, filters);
      setVacancies(response.data.vacancies || []);
    } catch (error) {
      console.error("Ошибка при загрузке вакансий:", error);
    } finally {
      setLoading(false);
    }
  };

  return {
    vacancies,
    loading,
    fetchVacancies,
  };
}
