import React from 'react';
import { Link, NavLink } from 'react-router-dom';
import { FaFileAlt, FaCog, FaSearch, FaHeart } from 'react-icons/fa';
import { Button } from '@/components/ui/button';
import '@/styles/sidebar.css';

const Sidebar: React.FC = () => {
    const navLinks = [
        {
            href: '/resume',
            title: 'Резюме',
            icon: FaFileAlt,
        },
        {
            href: '/vacancies',
            title: 'Поиск работы',
            icon: FaSearch,
        },
        {
            href: '/favorites',
            title: 'Избранное',
            icon: FaHeart,
        },
        {
            href: '/settings',
            title: 'Настройки',
            icon: FaCog,
        },
    ];

    return (
        <aside className="sidebar">
            <div className="sidebar__profile">
                <img
                    src="/planet.png"
                    alt="avatar"
                    className="sidebar__avatar"
                />
                <div className="sidebar__name">Вера Неттор</div>
                <div className="sidebar__email">VeraNettor2002@gmail.com</div>
            </div>

            <nav className="sidebar__nav">
                {navLinks.map(({ href, title, icon: Icon }, index) => (
                    <NavLink
                        key={index}
                        to={href}
                        className={({ isActive }) =>
                            isActive
                                ? 'sidebar__link sidebar__link--active'
                                : 'sidebar__link'
                        }
                    >
                        <Icon /> {title}
                    </NavLink>
                ))}
            </nav>

            <Button variant="ghost" className="sidebar__home-button" asChild>
                <Link to="/">← На главную</Link>
            </Button>
        </aside>
    );
};

export default Sidebar;
