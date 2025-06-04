import { createBrowserRouter } from 'react-router-dom';
import { MainLayout } from '@/components/layout/MainLayout';
import { SidebarLayout } from '@/components/layout/SidebarLayout';

import { Resume } from '@/components/pages/Resume';
import { About } from '@/components/pages/About';
import { Root } from '@/components/pages/Root';
import { Vacancies } from '@/components/pages/Vacancies';
import { Settings } from '@/components/pages/Settings';
import { Favorites } from '@/components/pages/Favorites';

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
            {
                path: 'resume',
                element: <Resume />,
            },
            {
                path: 'settings',
                element: <Settings />,
            },
            {
                path: 'favorites',
                element: <Favorites />,
            },
        ],
    },
]);
