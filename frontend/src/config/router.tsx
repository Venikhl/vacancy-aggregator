import { createBrowserRouter } from 'react-router-dom';
import { MainLayout } from '@/components/layouts/MainLayout';
import { SidebarLayout } from '@/components/layouts/SidebarLayout';

import { Resume } from '@/components/pages/Resume';
import { About } from '@/components/pages/About';
import { Root } from '@/components/pages/Root';
import { Vacancies } from '@/components/pages/Vacancies';
import { Settings } from '@/components/pages/Settings';
import { Favorites } from '@/components/pages/Favorites';
import { AuthLayout } from '@/components/layouts/AuthLayout';
import { Login } from '@/components/pages/Login';

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
    {
        path: '/',
        element: <AuthLayout />,
        children: [
            {
                path: 'login',
                element: <Login />,
            },
            {
                path: 'register',
                element: <About />,
            },
        ],
    },
]);
