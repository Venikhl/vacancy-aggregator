import { Root } from '@/components/pages/Root';
import { createBrowserRouter } from 'react-router-dom';

export const router = createBrowserRouter([
    {
        path: '/',
        element: <Root />,
    },
    {
        path: '/auth',
        element: <Root />,
    },
]);
