import { Outlet } from 'react-router-dom';
import { TopPanel } from './components/Header';

const MainLayout = () => {
    return (
        <main>
            <TopPanel />
            <Outlet />
        </main>
    );
};

export default MainLayout;
