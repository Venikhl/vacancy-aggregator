import { Outlet } from 'react-router-dom';
import Sidebar from '@/components/ui/Sidebar';

const SIDEBAR_WIDTH = 250;

const SidebarLayout = () => {
  return (
    <>
      <Sidebar />
      <main
        style={{
          marginLeft: SIDEBAR_WIDTH,
          padding: '2rem',
          backgroundColor: '#1A1A1A',
          color: 'white',
          minHeight: '100vh',
          boxSizing: 'border-box',
        }}
      >
        <Outlet />
      </main>
    </>
  );
};

export default SidebarLayout;
