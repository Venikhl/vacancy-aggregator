import React, { useEffect, useState } from "react";
import { VacancyCard } from "@/components/cards/VacancyCard";
import { VacancyFilters } from "@/components/filters/VacancyFilters";
import type { Filters } from "@/types/filters";
import { useVacancies } from "./hooks/useVacancies";

const defaultFilters: Filters = {
  keyword: "",
  region: "",
  salary: { min: 30000, max: 150000 },
  experience: [],
  sources: [],
};

export const Vacancies: React.FC = () => {
  const [filters, setFilters] = useState<Filters>(defaultFilters);
  const { vacancies, loading, fetchVacancies } = useVacancies();

  const loadVacancies = React.useCallback(() => {
    fetchVacancies({
      ...filters,
      experience: filters.experience?.filter((v): v is string => typeof v === "string"),
      sources: filters.sources?.filter((v): v is string => typeof v === "string"),
    });
  }, [filters, fetchVacancies]);

  const handleReset = () => {
    setFilters({ ...defaultFilters });
  };

  useEffect(() => {
    loadVacancies();
  }, [loadVacancies]);

  return (
    <div className="min-h-screen px-4 py-6 text-on-background">
      <div className="max-w-6xl mx-auto space-y-6">
        <VacancyFilters
          filters={filters}
          onChange={setFilters}
          onApply={loadVacancies}
          onReset={handleReset}
        />

        <div className="space-y-6">
          {loading ? (
            <p className="text-sm text-muted-foreground animate-pulse">Загрузка вакансий...</p>
          ) : (
            <>
              <p className="text-sm text-muted-foreground">
                Найдено результатов: {vacancies.length}
              </p>

              {vacancies.length === 0 ? (
                <p className="text-muted-foreground italic">Нет подходящих вакансий.</p>
              ) : (
                vacancies.map((v) => (
                  <VacancyCard
                    key={v.id}
                    title={v.title}
                    company="—"
                    location="—"
                    salary={
                      v.salary?.value
                        ? `${v.salary.value.toLocaleString()} ${v.salary.currency}`
                        : `${filters.salary?.max?.toLocaleString() ?? "—"} ₽`
                    }
                    timeAgo="—"
                  />
                ))
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Vacancies;
