import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';

export default function Home() {
    const navLinks = [
        { label: 'Главная', path: '/' },
        { label: 'Вакансии', path: '/vacancy' },
        { label: 'О нас', path: '/about' }, // можешь создать эту страницу позже
    ];

    return (
        <div className="min-h-screen bg-black text-white flex flex-col relative overflow-hidden">
            {/* Top panel */}
            <div className="flex justify-between items-center px-8 py-4 z-10 relative">
                <div className="flex items-center gap-2">
                    <img src="/logo.svg" className="w-8 h-8" alt="Лого" />
                    <span className="text-xl font-semibold">РаботаПоиск</span>
                </div>

                <div className="flex gap-4">
                    {navLinks.map(({ label, path }) => (
                        <Link
                            key={label}
                            to={path}
                            className="border border-orange-500 text-orange-500 rounded-full px-4 py-1 hover:bg-orange-500 hover:text-black transition"
                        >
                            {label}
                        </Link>
                    ))}
                </div>

                <Button className="bg-orange-600 hover:bg-orange-700 text-white rounded-full px-6 py-1">
                    Войти
                </Button>
            </div>

            {/* Intro info */}
            <div className="flex-1 flex flex-col z-10 relative">
                <div className="flex items-center justify-between px-20 py-10 relative z-10">
                    <div className="max-w-xl">
                        <h1 className="text-5xl font-bold mb-4">Объединяем возможности</h1>
                        <p className="text-gray-400 mb-6">
                            Donec gravida, urna vitae tincidunt gravida, dui lectus finibus erat,
                            nec vehicula urna sem quis dui.
                        </p>
                        <Button className="bg-orange-600 hover:bg-orange-700 text-white rounded-full px-6 py-2">
                            Регистрация
                        </Button>

                        <div className="mt-10 grid grid-cols-2 gap-6 text-orange-500">
                            <div>
                                <p className="text-2xl font-bold">15 482</p>
                                <p className="text-sm text-white">Вакансий</p>
                            </div>
                            <div>
                                <p className="text-2xl font-bold">8 729</p>
                                <p className="text-sm text-white">Резюме</p>
                            </div>
                            <div>
                                <p className="text-2xl font-bold">3 254</p>
                                <p className="text-sm text-white">Компаний</p>
                            </div>
                            <div>
                                <p className="text-2xl font-bold">3</p>
                                <p className="text-sm text-white">Источников</p>
                            </div>
                        </div>
                    </div>

                    <img
                        src="/planet.png"
                        alt="Планета"
                        className="absolute right-[-100px] top-[-80px] w-[900px] h-[900px] object-contain z-0 opacity-90 transform scale-x-[-1] pointer-events-none select-none"
                    />
                </div>

                {/* Vacancies */}
                <div className="relative z-20 mt-28">
                    <div className="bg-[#1e1e1e] rounded-tr-3xl px-8 py-4 flex justify-between items-start shadow-none w-[600px] relative z-30 -ml-4">
                        {/* Appendix */}
                        <div>
                            <h2 className="text-2xl font-bold mb-1">Последние <br />найденные вакансии</h2>
                        </div>
                        <div className="flex flex-col items-end max-w-[200px]">
                            <p className="text-sm text-gray-400 mb-2 text-right">
                                Посмотрите что мы нашли!
                            </p>
                            <Button className="bg-orange-600 hover:bg-orange-700 text-white rounded-full px-6 py-2">
                                Посмотреть все
                            </Button>
                        </div>
                    </div>

                    {/* Cards */}
                    <div className="bg-[#1e1e1e] px-10 pt-5 pb-20">
                        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                            {Array.from({ length: 12 }).map((_, i) => (
                                <div
                                    key={i}
                                    className="bg-[#1e1e1e] border border-orange-500 rounded-xl p-4 flex flex-col gap-2 text-white shadow-md hover:shadow-orange-500/30 transition-shadow"
                                >
                                    <div className="flex items-center gap-2">
                                        <span className="bg-orange-600 text-white text-xs px-2 py-1 rounded-full font-semibold">МТС</span>
                                    </div>
                                    <h3 className="text-lg font-semibold">Frontend-разработчик</h3>
                                    <p className="text-sm text-gray-400">
                                        Ищем талантливого разработчика с опытом React и Tailwind CSS
                                    </p>
                                    <div className="flex flex-wrap gap-2 mt-2 text-xs">
                                        <span className="bg-black border border-gray-500 px-2 py-1 rounded-full">web</span>
                                        <span className="bg-black border border-gray-500 px-2 py-1 rounded-full">remote</span>
                                        <span className="bg-black border border-gray-500 px-2 py-1 rounded-full">от 120 000₽</span>
                                    </div>
                                    <div className="mt-2 text-xs text-gray-400">+7 777 777 77 77</div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
