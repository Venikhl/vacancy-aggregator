import { createBrowserRouter } from 'react-router-dom';
import MainLayout from '@/components/layout/MainLayout';
import SidebarLayout from '@/components/layout/SidebarLayout';

import Home from '@/components/pages/Home/Home';
import Resume from '@/components/pages/Resume/Resume';
import Settings from '@/components/pages/Settings/Settings';
import Vacancy from '@/components/pages/Vacancy/Vacancy';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <MainLayout />,
    children: [
      {
        index: true,
        element: <Home />, // Главная без сайдбара
      },
    ],
  },
  {
    path: '/',
    element: <SidebarLayout />,
    children: [
      {
        path: 'resume',
        element: <Resume />,
      },
      {
        path: 'settings',
        element: <Settings />,
      },
      {
        path: 'vacancy',
        element: <Vacancy />,
      },
      // добавляй сюда другие страницы
    ],
  },
]);
