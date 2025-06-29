import { createRoot } from 'react-dom/client';
import { RouterProvider } from 'react-router-dom';
import { router } from '@/config/router';
import './styles/index.css';

createRoot(document.getElementById('root')!).render(
    // <StrictMode>
    //
    // </StrictMode>,
    <RouterProvider router={router} />,
);
