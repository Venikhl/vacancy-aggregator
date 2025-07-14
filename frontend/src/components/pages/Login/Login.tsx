import { loginFormSchema } from '@/schemas/login';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormMessage,
} from '@/components/ui/form';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useForm } from 'react-hook-form';
import { Checkbox } from '@/components/ui/checkbox';
import { Link, useNavigate } from 'react-router-dom';
import { LockKeyhole, User } from 'lucide-react';
import axiosInstance from '@/api';
import TokenService from '@/api/tokens.ts';

const Login = () => {
    const navigate = useNavigate();

    const form = useForm<z.infer<typeof loginFormSchema>>({
        resolver: zodResolver(loginFormSchema),
        defaultValues: {
            email: '',
            password: '',
            remember: false,
        },
    });

    function onSubmit(values: z.infer<typeof loginFormSchema>) {
        axiosInstance
            .post('/login', values)
            .then((response) => {
                TokenService.setTokens(response.data);
                navigate('/');
            })
            .catch((error) => {
                console.log(error);
            });
    }

    return (
        <Form {...form}>
            <form
                onSubmit={form.handleSubmit(onSubmit)}
                className="h-full w-full flex flex-col justify-between"
            >
                <div className="w-full flex flex-col gap-y-9">
                    <h1 className="text-4xl font-semibold text-primary mb-[11px]">
                        Вход
                    </h1>
                    <FormField
                        control={form.control}
                        name="email"
                        render={({ field }) => (
                            <FormItem>
                                <FormControl>
                                    <Input
                                        startIcon={User}
                                        placeholder="Почта"
                                        {...field}
                                    />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="password"
                        render={({ field }) => (
                            <FormItem>
                                <FormControl>
                                    <Input
                                        startIcon={LockKeyhole}
                                        placeholder="Пароль"
                                        {...field}
                                    />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                </div>
                <div className="w-full flex flex-col gap-y-[13px]">
                    <div className="flex items-center justify-between w-full text-side">
                        <div className="flex items-center gap-x-2">
                            <FormField
                                control={form.control}
                                name="remember"
                                render={({ field: { onChange, value } }) => (
                                    <FormItem>
                                        <FormControl>
                                            <Checkbox
                                                onCheckedChange={() =>
                                                    onChange(!value)
                                                }
                                                checked={value}
                                            />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                            <span className="text-on-background">
                                Запомнить меня
                            </span>
                        </div>
                        <Link to="#" className="text-on-background">
                            Забыли пароль?
                        </Link>
                    </div>
                    <Button type="submit" className="w-full">
                        Войти
                    </Button>
                </div>
            </form>
        </Form>
    );
};

export default Login;
