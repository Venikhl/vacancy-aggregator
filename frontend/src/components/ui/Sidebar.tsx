import React from 'react';
import { Link, NavLink } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { File, Cog, Heart, Search } from 'lucide-react';

const Sidebar: React.FC = () => {
    const navLinks = [
        { href: '/resume', title: 'Резюме', icon: File },
        { href: '/vacancies', title: 'Поиск работы', icon: Search },
        { href: '/favorites', title: 'Избранное', icon: Heart },
        { href: '/settings', title: 'Настройки', icon: Cog },
    ];

    return (
        <aside
            className="
                fixed top-0 left-0 z-[1000]
                h-screen w-[250px]
                flex flex-col
                bg-background text-on
                pt-8 pb-8 pl-4
                overflow-x-hidden
                box-border
            "
        >
            <div className="flex flex-col items-center mb-8 px-4">
                <img
                    src="/planet.png"
                    alt="avatar"
                    className="w-20 h-20 rounded-full object-cover mb-4"
                />
                <div className="font-bold text-[1.1rem] text-on-foreground">
                    Вера Неттор
                </div>
                <div className="text-[0.9rem] text-secondary">
                    VeraNettor2002@gmail.com
                </div>
            </div>

            <nav className="flex flex-col gap-4">
                {navLinks.map(({ href, title, icon: Icon }) => (
                    <NavLink
                        key={href}
                        to={href}
                        className={({ isActive }) =>
                            cn(
                                'flex items-center gap-3 w-full box-border',
                                'py-[0.8rem] px-4 rounded-l-[20px]',
                                'text-on-foreground transition-colors duration-200 no-underline',

                                isActive
                                    ? 'bg-foreground text-on-background font-bold'
                                    : 'hover:bg-foreground hover:text-primary-active',
                            )
                        }
                    >
                        <Icon /> {title}
                    </NavLink>
                ))}
            </nav>

            <Button
                variant="transparent"
                className="
                    mt-auto mr-auto
                    bg-none border-none
                    text-[0.9rem]
                    px-4 py-2
                    text-left
                    cursor-pointer
                    transition-colors duration-200
                "
                asChild
            >
                <Link to="/">← На главную</Link>
            </Button>
        </aside>
    );
};

export default Sidebar;
