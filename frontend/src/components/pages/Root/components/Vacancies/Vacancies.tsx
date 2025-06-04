import { Button } from '@/components/ui/button.tsx';
import { Vacancy } from '@/components/shared/Vacancy';

const Vacancies = () => {
    return (
        <div className="relative z-20 mt-28">
            <div className="bg-foreground rounded-tr-3xl px-8 py-4 flex justify-between items-start shadow-none w-[600px] relative z-30 -ml-4">
                {/* Appendix */}
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
                    <Button className="bg-primary hover:bg-primary-hover text-on-primary rounded-full px-6 py-2">
                        Посмотреть все
                    </Button>
                </div>
            </div>

            {/* Cards */}
            <div className="bg-foreground px-10 pt-5 pb-20">
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                    {Array.from({ length: 12 }).map((_, index) => (
                        <Vacancy
                            key={index}
                            company="МТС"
                            title="Frontend разработчик"
                            description="Ищем талантливого разработчика с опытом React и Tailwind CSS."
                            tags={['web', 'remote', 'от 120000₽']}
                            phone="8 (800) 555 35 35"
                        />
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Vacancies;
