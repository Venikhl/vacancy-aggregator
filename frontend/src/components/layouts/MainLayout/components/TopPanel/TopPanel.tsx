import { Button } from '@/components/ui/button.tsx';
import { Link } from 'react-router-dom';

const TopPanel = () => {
    const navLinks = [
        {
            title: 'Главная',
            href: '/',
        },
        {
            title: 'Вакансии',
            href: '/vacancies',
        },
        {
            title: 'О нас',
            href: '/about',
        },
    ];

    return (
        <div className="flex justify-between items-center px-8 py-4 z-10 relative">
            <div className="flex items-center gap-2">
                <img src="/logo.svg" className="w-8 h-8" alt="Лого" />
                <span className="text-xl font-semibold text-on-background">
                    РаботаПоиск
                </span>
            </div>

            <div className="flex gap-4">
                {navLinks.map(({ title, href }, index) => (
                    <Button
                        key={index}
                        asChild
                        className="bg-transparent border border-primary text-on-background rounded-full px-4 py-1 hover:bg-primary hover:text-on-primary transition"
                    >
                        <Link to={href}>{title}</Link>
                    </Button>
                ))}
            </div>

            <Button className="bg-primary hover:bg-primary/80 text-on-primary rounded-full px-6 py-1">
                Войти
            </Button>
        </div>
    );
};

export default TopPanel;
