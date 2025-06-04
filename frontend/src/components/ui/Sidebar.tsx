import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { FaFileAlt, FaCog, FaSearch, FaHeart } from 'react-icons/fa';
import '../../styles/sidebar.css';

const Sidebar: React.FC = () => {
  const navigate = useNavigate();

  return (
    <aside className="sidebar">
      <div className="sidebar__profile">
        <img src="/planet.png" alt="avatar" className="sidebar__avatar" />
        <div className="sidebar__name">Вера Неттор</div>
        <div className="sidebar__email">VeraNettor2002@gmail.com</div>
      </div>

      <nav className="sidebar__nav">
        <NavLink to="/resume" className={({ isActive }) => isActive ? 'sidebar__link sidebar__link--active' : 'sidebar__link'}>
          <FaFileAlt /> Резюме
        </NavLink>
        <NavLink to="/vacancy" className={({ isActive }) => isActive ? 'sidebar__link sidebar__link--active' : 'sidebar__link'}>
          <FaSearch /> Поиск работы
        </NavLink>
        <NavLink to="/favorites" className={({ isActive }) => isActive ? 'sidebar__link sidebar__link--active' : 'sidebar__link'}>
          <FaHeart /> Избранное
        </NavLink>
        <NavLink to="/settings" className={({ isActive }) => isActive ? 'sidebar__link sidebar__link--active' : 'sidebar__link'}>
          <FaCog /> Настройки
        </NavLink>
      </nav>

      <button
        type="button"
        className="sidebar__home-button"
        onClick={() => navigate('/')}
      >
        ← На главную
      </button>
    </aside>
  );
};

export default Sidebar;
