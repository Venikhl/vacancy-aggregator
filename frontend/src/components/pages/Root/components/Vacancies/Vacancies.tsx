import { useEffect } from 'react';
import { Button } from '@/components/ui/button.tsx';
import { Vacancy } from '@/components/shared/Vacancy';
import { useVacancies } from '@/components/pages/Root/components/Vacancies/useVacancies.ts';
import { useNavigate } from 'react-router-dom';

const Vacancies = () => {
    const { vacancies, loading, fetchVacancies } = useVacancies();
    const navigate = useNavigate();

    useEffect(() => {
        fetchVacancies(
            {
                title: '',
                salary_min: 0,
                salary_max: 15000000,
                experience_categories: [],
                location: null,
            },
            20,
        );
    }, [fetchVacancies]);

    return (
        <div className="relative z-20 mt-28">
            <div className="bg-foreground rounded-tr-3xl px-8 py-4 flex justify-between items-start shadow-none w-[600px] relative z-30 -ml-4">
                <div>
                    <h2 className="text-2xl font-bold mb-1">
                        Последние <br />
                        найденные вакансии
                    </h2>
                </div>
                <div className="flex flex-col items-end max-w-[200px]">
                    <p className="text-sm text-secondary mb-2 text-right">
                        Посмотрите что мы нашли!
                    </p>
                    <Button
                        className="bg-primary hover:bg-primary/80 text-on-primary rounded-full px-6 py-2"
                        onClick={() => navigate('/vacancies')} // переход на страницу вакансий
                    >
                        Посмотреть все
                    </Button>
                </div>
            </div>

            {/* Cards */}
            <div className="bg-foreground px-10 pt-5 pb-20">
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                    {loading
                        ? Array.from({ length: 12 }).map((_, index) => (
                              <div
                                  key={index}
                                  className="animate-pulse h-40 bg-muted rounded-xl"
                              />
                          ))
                        : vacancies.map((v) => (
                              <Vacancy
                                  key={v.id}
                                  url={v.url ?? ''}
                                  company={
                                      v.company?.name || v.source?.name || '—'
                                  }
                                  title={v.title || 'Без названия'}
                                  description={
                                      v.description
                                          ? v.description
                                                .replace(/<[^>]+>/g, '')
                                                .slice(0, 120) + '...'
                                          : 'Описание отсутствует'
                                  }
                                  tags={[
                                      v.experience_category?.name,
                                      v.location?.region,
                                  ].filter((tag): tag is string =>
                                      Boolean(tag),
                                  )}
                              />
                          ))}
                </div>
            </div>
        </div>
    );
};

export default Vacancies;
