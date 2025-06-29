import React from 'react';
import { ResumeCard } from '@/components/cards/ResumeCard';
import { ResumeFilters } from '@/components/filters/ResumeFilters';

const Resume: React.FC = () => {
    const resumes = [
        {
            position: 'Frontend Developer',
            name: 'Иван Иванов',
            location: 'Москва',
            experience: '3 года',
            skills: ['JavaScript', 'React', 'TypeScript', 'HTML/CSS'],
            salary: '150 000 ₽',
            timeAgo: 'Обновлено 3 дня назад',
        },
        {
            position: 'Backend Developer',
            name: 'Петр Петров',
            location: 'Санкт-Петербург',
            experience: '5 лет',
            skills: ['Python', 'Django', 'PostgreSQL', 'Docker'],
            salary: '180 000 ₽',
            timeAgo: 'Обновлено неделю назад',
        },
    ];

    return (
        <div className="min-h-screen bg-[#f1f0ee] px-4 py-6">
            <div className="max-w-6xl mx-auto space-y-6">
                {/* Фильтры */}
                <div>
                    <ResumeFilters />
                </div>

                {/* Список резюме */}
                <div className="space-y-6">
                    <p className="text-sm text-gray-600">
                        Найдено резюме: {resumes.length}
                    </p>
                    {resumes.map((resume, idx) => (
                        <ResumeCard key={idx} {...resume} />
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Resume;
