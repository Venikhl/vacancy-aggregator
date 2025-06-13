import React from 'react';
import { VacancyCard } from "@/components/cards/VacancyCard";
import { VacancyFilters } from "@/components/filters/VacancyFilters";

const Vacancies: React.FC = () => {
  const vacancies = [
    {
      title: "Frontend Developer",
      company: "МТС",
      location: "Москва",
      salary: "150 000 ₽",
      timeAgo: "Parsed 3 hours ago",
    },
    {
      title: "Backend Developer",
      company: "МТС",
      location: "Санкт-Петербург",
      salary: "180 000 ₽",
      timeAgo: "Parsed 1 day ago",
    },
  ];

  return (
    <div className="min-h-screen bg-[#f1f0ee] px-4 py-6">
      <div className="max-w-6xl mx-auto space-y-6">
        
        {/* Фильтры */}
        <div >
          <VacancyFilters />
        </div>

        {/* Список вакансий */}
        <div className="space-y-6">
          <p className="text-sm text-gray-600">
            Найдено результатов: {vacancies.length}
          </p>
          {vacancies.map((v, idx) => (
            <VacancyCard key={idx} {...v} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Vacancies;
