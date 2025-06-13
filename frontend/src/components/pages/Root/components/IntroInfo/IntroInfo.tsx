import { Button } from '@/components/ui/button.tsx';

const IntroInfo = () => {
    return (
        <div className="flex items-center justify-between px-20 py-10 relative z-10">
            <div className="max-w-xl">
                <h1 className="text-5xl font-bold mb-4">
                    Объединяем возможности
                </h1>
                <p className="text-secondary mb-6">
                    Donec gravida, urna vitae tincidunt gravida, dui lectus
                    finibus erat, nec vehicula urna sem quis dui.
                </p>
                <Button className="bg-primary hover:bg-primary/90 text-on-primary rounded-full px-6 py-2">
                    Регистрация
                </Button>

                <div className="mt-10 grid grid-cols-2 gap-6 text-primary">
                    <div>
                        <p className="text-2xl font-bold">15 482</p>
                        <p className="text-sm text-secondary">Вакансий</p>
                    </div>
                    <div>
                        <p className="text-2xl font-bold">8 729</p>
                        <p className="text-sm text-secondary">Резюме</p>
                    </div>
                    <div>
                        <p className="text-2xl font-bold">3 254</p>
                        <p className="text-sm text-secondary">Компаний</p>
                    </div>
                    <div>
                        <p className="text-2xl font-bold">3</p>
                        <p className="text-sm text-secondary">Источников</p>
                    </div>
                </div>
            </div>

            <img
                src="/planet.png"
                alt="Планета"
                className="absolute right-[-100px] top-[-80px] w-[900px] h-[900px] object-contain z-0 opacity-90 transform scale-x-[-1] pointer-events-none select-none"
            />
        </div>
    );
};

export default IntroInfo;
