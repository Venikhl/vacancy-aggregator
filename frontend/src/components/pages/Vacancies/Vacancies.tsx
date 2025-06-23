import React, { useEffect, useState } from "react";
import { VacancyCard } from "@/components/cards/VacancyCard";
import { VacancyFilters } from "@/components/filters/VacancyFilters";
import { useVacancies } from "./hooks/useVacancies";
import { Button } from "@/components/ui/button";
import type { Filters } from "@/types/filters";

const defaultFilters: Filters = {
  title: "",
  salary_min: 0,
  salary_max: 1500000,
  experience_categories: [],
  location: null,
};

export const Vacancies: React.FC = () => {
  const [filters, setFilters] = useState<Filters>(defaultFilters);
  const [currentPage, setCurrentPage] = useState(1);

  const { vacancies, loading, totalCount, fetchVacancies } = useVacancies();

  const VACANCIES_PER_PAGE = 15;
  const totalPages = Math.ceil(totalCount / VACANCIES_PER_PAGE);

  useEffect(() => {
    const offset = (currentPage - 1) * VACANCIES_PER_PAGE;
    fetchVacancies(filters, offset, VACANCIES_PER_PAGE);
  }, [filters, currentPage]);

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  const handleReset = () => {
    setFilters(defaultFilters);
    setCurrentPage(1);
  };

  const handleApplyFilters = () => {
    setCurrentPage(1);
    fetchVacancies(filters, 0, VACANCIES_PER_PAGE);
  };

  return (
    <div className="min-h-screen px-4 py-6 text-on-background">
      <div className="max-w-6xl mx-auto space-y-6">
        <VacancyFilters
          filters={filters}
          onChange={setFilters}
          onApply={handleApplyFilters}
          onReset={handleReset}
        />

        <div className="space-y-6">
          {loading ? (
            <p className="text-sm text-muted-foreground animate-pulse">
              Загрузка вакансий...
            </p>
          ) : (
            <>
              <p className="text-sm text-muted-foreground">
                Найдено результатов: {totalCount}
              </p>

              {vacancies.length === 0 ? (
                <p className="text-muted-foreground italic">Нет подходящих вакансий.</p>
              ) : (
                <>
                  {vacancies.map((v) => (
                    <VacancyCard
                      key={v.id}
                      id={v.id}
                      title={v.title}
                      salary={
                        v.salary?.value
                          ? `${v.salary.value.toLocaleString()} ${v.salary.currency}`
                          : undefined
                      }
                    />
                  ))}

                  {totalPages > 1 && (
                    <div className="flex justify-center gap-2 pt-4 flex-wrap">
                      <Button
                        variant="outline"
                        size="sm"
                        disabled={currentPage === 1}
                        onClick={() => handlePageChange(currentPage - 1)}
                      >
                        Назад
                      </Button>

                      {getPaginationRange(currentPage, totalPages).map((page, index) =>
                        typeof page === "number" ? (
                          <Button
                            key={page}
                            variant={currentPage === page ? "default" : "outline"}
                            size="sm"
                            onClick={() => handlePageChange(page)}
                          >
                            {page}
                          </Button>
                        ) : (
                          <span
                            key={`dots-${index}`}
                            className="px-2 text-muted-foreground select-none"
                          >
                            ...
                          </span>
                        )
                      )}

                      <Button
                        variant="outline"
                        size="sm"
                        disabled={currentPage === totalPages}
                        onClick={() => handlePageChange(currentPage + 1)}
                      >
                        Вперёд
                      </Button>
                    </div>
                  )}
                </>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Vacancies;

function getPaginationRange(current: number, total: number): (number | string)[] {
  const delta = 2;
  const range: (number | string)[] = [];
  const rangeWithDots: (number | string)[] = [];

  for (let i = 1; i <= total; i++) {
    if (i === 1 || i === total || (i >= current - delta && i <= current + delta)) {
      range.push(i);
    }
  }

  let prev: number | null = null;
  for (let num of range) {
    if (prev !== null && typeof num === "number") {
      if (num - prev > 1) {
        rangeWithDots.push("...");
      }
    }
    rangeWithDots.push(num);
    if (typeof num === "number") prev = num;
  }

  return rangeWithDots;
}
