import React from 'react';

type ResumeCardProps = {
  position: string;
  name: string;
  location: string;
  experience: string;
  skills: string[];
  salary?: string;
  timeAgo?: string;
};

export const ResumeCard: React.FC<ResumeCardProps> = ({ 
  position, 
  name, 
  location, 
  experience, 
  skills, 
  salary, 
  timeAgo 
}) => {
  return (
    <div className="bg-white border border-gray-200 rounded-xl p-5 flex flex-col gap-3 shadow-sm hover:shadow-md transition">
      <div className="flex items-center justify-between text-sm text-gray-400">
        <span>{timeAgo || 'Обновлено недавно'}</span>
      </div>
      <h2 className="text-xl font-semibold text-gray-900">{position}</h2>
      <div className="flex items-center gap-2">
        <span className="bg-[#1e1e1e] text-white text-xs font-semibold px-3 py-1 rounded-full">👤 {name}</span>
      </div>
      <p className="text-gray-600">{location}</p>
      <p className="text-gray-700">Опыт: {experience}</p>
      {salary && <p className="text-green-600 font-medium">Желаемая зарплата: {salary}</p>}
      <div className="flex flex-wrap gap-2 mt-1">
        {skills.map((skill, idx) => (
          <span key={idx} className="bg-gray-100 text-gray-800 text-xs px-3 py-1 rounded-full">
            {skill}
          </span>
        ))}
      </div>
      <div className="flex justify-end gap-2 mt-3">
        <button className="border border-[#1e1e1e] text-[#1e1e1e] px-4 py-1 rounded-md hover:bg-gray-100">
          Сохранить
        </button>
        <button className="bg-[#1e1e1e] text-white px-4 py-1 rounded-md hover:bg-gray-800">
          Пригласить
        </button>
      </div>
    </div>
  );
};