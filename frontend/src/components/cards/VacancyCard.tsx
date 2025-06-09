import React from 'react';

type VacancyCardProps = {
  title: string;
  company: string;
  location: string;
  salary?: string;
  timeAgo?: string;
};

export const VacancyCard: React.FC<VacancyCardProps> = ({ title, company, location, salary, timeAgo }) => {
  return (
    <div className="bg-white border border-gray-200 rounded-xl p-5 flex flex-col gap-2 shadow-sm hover:shadow-md transition">
      <div className="flex items-center justify-between text-sm text-gray-400">
        <span>{timeAgo || 'Parsed recently'}</span>
      </div>
      <div className="flex items-center gap-2">
        <span className="bg-orange-500 text-white text-xs font-semibold px-3 py-1 rounded-full">🔶 {company}</span>
      </div>
      <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
      <p className="text-gray-600">{location}</p>
      {salary && <p className="text-green-600 font-medium">{salary}</p>}
      <div className="flex justify-end gap-2 mt-3">
        <button className="border border-gray-300 text-gray-700 px-4 py-1 rounded-md hover:bg-gray-100">
          Сохранить
        </button>
        <button className="bg-orange-500 text-white px-4 py-1 rounded-md hover:bg-orange-600">
          Откликнуться
        </button>
      </div>
    </div>
  );
};
