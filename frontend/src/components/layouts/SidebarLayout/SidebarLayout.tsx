import { Outlet } from 'react-router-dom';
import Sidebar from '@/components/ui/Sidebar';

const SidebarLayout = () => {
    return (
        <>
            <Sidebar />
            <main className="ml-[250px] p-8 bg-foreground text-on-primary min-h-[100vh] box-border">
                <Outlet />
            </main>
        </>
    );
};

export default SidebarLayout;
