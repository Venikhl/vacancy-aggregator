import { Outlet } from 'react-router-dom';
import { TopPanel } from './components/TopPanel';

const MainLayout = () => {
    return (
        <main>
            <TopPanel />
            <Outlet />
        </main>
    );
};

export default MainLayout;
