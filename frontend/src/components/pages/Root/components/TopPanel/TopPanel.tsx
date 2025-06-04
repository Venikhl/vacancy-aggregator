import { Button } from '@/components/ui/button';

const TopPanel = () => {
    return (
        <div className="flex justify-between items-center px-8 py-4 z-10 relative">
            <div className="flex items-center gap-2">
                <img src="/logo.svg" className="w-8 h-8" alt="Лого" />
                <span className="text-xl font-semibold">РаботаПоиск</span>
            </div>

            <div className="flex gap-4">
                {['Главная', 'Вакансии', 'О нас'].map((item) => (
                    <button
                        key={item}
                        className="border border-orange-500 text-orange-500 rounded-full px-4 py-1 hover:bg-orange-500 hover:text-black transition"
                    >
                        {item}
                    </button>
                ))}
            </div>

            <Button className="bg-orange-600 hover:bg-orange-700 text-white rounded-full px-6 py-1">
                Войти
            </Button>
        </div>
    );
};

export default TopPanel;
