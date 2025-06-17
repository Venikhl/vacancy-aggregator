import React, { useEffect, useState } from "react";
import { getVacancies } from "@/api";
import { VacancyCard } from "@/components/cards/VacancyCard";
import { VacancyFilters } from "@/components/filters/VacancyFilters";
import type { Filters } from "@/types/filters";

interface Salary {
  value: number;
  currency: string;
}

interface Vacancy {
  id: string;
  title: string;
  salary: Salary | null;
}

export const Vacancies: React.FC = () => {
  const [vacancies, setVacancies] = useState<Vacancy[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<Filters>({
    keyword: "",
    region: "",
    salary: { min: 30000, max: 150000 },
    experience: [],
    sources: [],
  });

  const fetchVacancies = async () => {
    setLoading(true);
    try {
      const cleanedFilters: Record<string, any> = {};
      if (filters.keyword.trim()) cleanedFilters.keyword = filters.keyword.trim();
      if (filters.region) cleanedFilters.region = filters.region;
      if (filters.salary.min || filters.salary.max) cleanedFilters.salary = filters.salary;
      if (filters.experience.length > 0) cleanedFilters.experience = filters.experience;
      if (filters.sources.length > 0) cleanedFilters.sources = filters.sources;

      console.log("👉 Отправка запроса с фильтрами:", cleanedFilters);

      const response = await getVacancies(0, 20, cleanedFilters);
      setVacancies(response.data.vacancies || []);
    } catch (error) {
      console.error("Ошибка при загрузке вакансий:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFilters({
      keyword: "",
      region: "",
      salary: { min: 30000, max: 150000 },
      experience: [],
      sources: [],
    });
  };

  useEffect(() => {
    fetchVacancies();
  }, []);

  return (
    <div className="min-h-screen px-4 py-6 text-on-background">
      <div className="max-w-6xl mx-auto space-y-6">
        <VacancyFilters
          filters={filters}
          onChange={setFilters}
          onApply={fetchVacancies}
          onReset={handleReset}
        />

        <div className="space-y-6">
          {loading ? (
            <p className="text-sm text-muted-foreground">Загрузка...</p>
          ) : (
            <>
              <p className="text-sm text-muted-foreground">
                Найдено результатов: {vacancies.length}
              </p>
              {vacancies.map((v) => (
                <VacancyCard
                  key={v.id}
                  title={v.title}
                  company="—"
                  location="—"
                  salary={
                    v.salary
                      ? `${v.salary.value} ${v.salary.currency}`
                      : "Зарплата не указана"
                  }
                  timeAgo="—"
                />
              ))}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Vacancies;
