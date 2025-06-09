import React from 'react';
import { Search } from 'lucide-react';

export const VacancyFilters: React.FC = () => {
  return (
    <div className="bg-white text-black rounded-2xl p-6 shadow-md space-y-6">
      {/* поиск */}
      <div className="flex flex-wrap items-center gap-4">
        <input
          type="text"
          placeholder="Должность, навыки, компания"
          className="flex-grow rounded-md border border-gray-300 bg-white px-4 py-2 text-sm placeholder:text-gray-500 outline-none focus:ring-2 focus:ring-orange-500"
        />
        <button className="flex items-center gap-1 rounded-md bg-orange-600 hover:bg-orange-700 px-4 py-2 text-sm text-white">
          <Search size={16} />
          Поиск
        </button>
      </div>

      {/* фильтры */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">

        {/* Ключевые слова */}
        <div className="flex flex-col">
          <label className="text-sm mb-1">Ключевые слова</label>
          <input
            type="text"
            placeholder="Должность, навыки, компания"
            className="rounded-md border border-gray-300 bg-white px-3 py-2 text-sm placeholder:text-gray-500 outline-none"
          />
        </div>

        {/* Регион */}
        <div className="flex flex-col">
          <label className="text-sm mb-1">Регион</label>
          <select className="rounded-md border border-gray-300 bg-white px-3 py-2 text-sm">
            <option>Все регионы</option>
            <option>Москва</option>
            <option>Санкт-Петербург</option>
          </select>
        </div>

        {/* Зарплата */}
        <div className="flex flex-col">
          <label className="text-sm mb-1">Диапазон зарплаты</label>
          <input type="range" min={30000} max={150000} className="w-full" />
          <div className="flex justify-between text-xs mt-1 text-gray-500">
            <span>30 000 ₽</span>
            <span>150 000 ₽</span>
          </div>
        </div>

        {/* Опыт */}
        <div className="flex flex-col">
          <label className="text-sm mb-1">Опыт работы</label>
          <div className="space-y-1 text-sm">
            <label className="flex items-center">
              <input type="checkbox" className="mr-2" /> Без опыта
            </label>
            <label className="flex items-center">
              <input type="checkbox" className="mr-2" /> 1–3 года
            </label>
            <label className="flex items-center">
              <input type="checkbox" className="mr-2" /> 3–6 лет
            </label>
            <label className="flex items-center">
              <input type="checkbox" className="mr-2" /> Более 6 лет
            </label>
          </div>
        </div>

        {/* Источники */}
        <div className="flex flex-col">
          <label className="text-sm mb-1">Источники</label>
          <div className="space-y-1 text-sm">
            <label className="flex items-center">
              <input type="checkbox" className="mr-2" /> HH.ru
            </label>
            <label className="flex items-center">
              <input type="checkbox" className="mr-2" /> Работа.ру
            </label>
            <label className="flex items-center">
              <input type="checkbox" className="mr-2" /> SuperJob
            </label>
          </div>
        </div>

        {/* Кнопки */}
        <div className="flex flex-col gap-2">
          <button className="px-4 py-2 text-sm bg-gray-200 text-black rounded-md hover:bg-gray-300">
            Сбросить
          </button>
          <button className="px-4 py-2 text-sm bg-orange-600 text-white rounded-md hover:bg-orange-700">
            Применить фильтры
          </button>
        </div>

      </div>
    </div>
  );
};
