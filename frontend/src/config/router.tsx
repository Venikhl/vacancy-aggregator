import { createBrowserRouter } from 'react-router-dom';
import MainLayout from '@/components/layout/MainLayout/MainLayout.tsx';
import SidebarLayout from '@/components/layout/SidebarLayout';

import Resume from '@/components/pages/Resume/Resume';
import About from '@/components/pages/About/About';
import { Root } from '@/components/pages/Root';
import { Vacancies } from '@/components/pages/Vacancies';

export const router = createBrowserRouter([
    {
        path: '/',
        element: <MainLayout />,
        children: [
            {
                index: true,
                element: <Root />,
            },
            {
                path: 'about',
                element: <About />,
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
                path: 'vacancies',
                element: <Vacancies />,
            },
            // добавляй сюда другие страницы
        ],
    },
]);
