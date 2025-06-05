import BackGround from '@/assets/auth.png';
import { Link, Outlet, useLocation } from 'react-router-dom';
import { cn } from '@/lib/utils.ts';

const AuthLayout = () => {
    const location = useLocation();

    const title = location.pathname.startsWith('/register')
        ? 'Регистрируйся'
        : 'Войди в систему';
    const link = location.pathname.startsWith('/register')
        ? '/login'
        : '/register';
    const linkTitle = location.pathname.startsWith('/register')
        ? 'Войти'
        : 'Зарегистрироваться';

    return (
        <main className="flex items-center w-[100vw] h-[100vh]">
            <div className="relative h-full hidden w-0 md:block md:w-1/2">
                <img
                    src={BackGround}
                    alt="Auth background"
                    className="min-w-full w-full min-h-full h-full object-cover"
                />
                <div
                    className={cn(
                        'absolute inset-0',
                        'flex flex-col justify-center',
                    )}
                >
                    <h1 className="w-full font-semibold text-[54px] text-on-primary text-center">
                        Найти работу просто!
                    </h1>
                    <span className="px-[100px] mt-4 text-[18px] text-on-primary text-center">
                        {title} и найди себе работу мечты в нашей коллекции!
                    </span>
                </div>
            </div>
            <div className="relative bg-foreground h-full w-full md:w-1/2">
                <Link
                    to={link}
                    className="absolute top-5 right-5 text-on-foreground underline"
                >
                    {linkTitle}
                </Link>
                <div
                    className={cn(
                        'bg-background w-full max-w-[565px] h-[635px] rounded-[25px]',
                        'absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2',
                        'flex flex-col justify-center items-center py-[81px] px-[48px]',
                    )}
                >
                    <Outlet />
                </div>
            </div>
        </main>
    );
};

export default AuthLayout;
