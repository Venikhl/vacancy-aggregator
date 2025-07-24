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
import { Mail, User, Lock, CalendarIcon } from 'lucide-react';
import { registerFormSchema } from '@/schemas/register.ts';
import axiosInstance from '@/api';
import TokenService from '@/api/tokens.ts';
import { useNavigate } from 'react-router-dom';
import { useUserInfo } from '@/hooks/useUserInfo.ts';
import { useEffect } from 'react';
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from '@/components/ui/popover.tsx';
import { cn } from '@/lib/utils';
import { format } from 'date-fns';
import { Calendar } from '@/components/ui/calendar.tsx';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select';

const Register = () => {
    const navigate = useNavigate();

    const form = useForm<z.infer<typeof registerFormSchema>>({
        resolver: zodResolver(registerFormSchema),
        defaultValues: {
            first_name: '',
            last_name: '',
            email: '',
            password: '',
            confirmPassword: '',
            birth_date: '',
            gender: undefined,
        },
    });

    function onSubmit(values: z.infer<typeof registerFormSchema>) {
        axiosInstance
            .post('/register', values)
            .then((response) => {
                TokenService.setTokens(response.data);
                navigate('/');
            })
            .catch((error) => {
                console.log(error);
            });
    }

    const { user } = useUserInfo();

    useEffect(() => {
        if (user) {
            navigate('/');
        }
    }, [navigate, user]);

    useEffect(() => {
        console.log(form.getValues());
    }, [form]);

    return (
        <Form {...form}>
            <form
                onSubmit={form.handleSubmit(onSubmit)}
                className="h-full w-full flex flex-col justify-between"
            >
                <div className="w-full flex flex-col gap-y-9">
                    <h1 className="text-4xl font-semibold text-primary mb-[11px]">
                        Регистрация
                    </h1>
                    <div className="flex items-center gap-x-[60px]">
                        <FormField
                            control={form.control}
                            name="first_name"
                            render={({ field }) => (
                                <FormItem>
                                    <FormControl>
                                        <Input
                                            startIcon={User}
                                            placeholder="Имя"
                                            {...field}
                                        />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                        <FormField
                            control={form.control}
                            name="last_name"
                            render={({ field }) => (
                                <FormItem>
                                    <FormControl>
                                        <Input
                                            startIcon={User}
                                            placeholder="Фамилия"
                                            {...field}
                                        />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                    </div>
                    <FormField
                        control={form.control}
                        name="email"
                        render={({ field }) => (
                            <FormItem>
                                <FormControl>
                                    <Input
                                        startIcon={Mail}
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
                        name="birth_date"
                        render={({ field }) => (
                            <FormItem className="flex flex-col">
                                <Popover>
                                    <PopoverTrigger asChild>
                                        <FormControl>
                                            <Button
                                                variant="outline"
                                                type="button"
                                                className={cn(
                                                    'w-full pl-3 text-left font-normal bg-foreground border rounded-md h-10 flex items-center justify-between px-3',
                                                    !field.value &&
                                                        'text-muted-foreground',
                                                )}
                                            >
                                                {field.value
                                                    ? format(
                                                          new Date(field.value),
                                                          'dd.MM.yyyy',
                                                      )
                                                    : 'Выберите дату рождения'}
                                                <CalendarIcon className="ml-2 h-4 w-4 opacity-50" />
                                            </Button>
                                        </FormControl>
                                    </PopoverTrigger>
                                    <PopoverContent
                                        className="w-auto p-0"
                                        align="start"
                                    >
                                        <Calendar
                                            mode="single"
                                            selected={
                                                field.value
                                                    ? new Date(field.value)
                                                    : undefined
                                            }
                                            onSelect={(date) =>
                                                field.onChange(
                                                    date
                                                        ? format(
                                                              date,
                                                              'yyyy-MM-dd',
                                                          )
                                                        : '',
                                                )
                                            }
                                            captionLayout="dropdown"
                                        />
                                    </PopoverContent>
                                </Popover>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="gender"
                        render={({ field }) => (
                            <FormItem>
                                <FormControl>
                                    <Select
                                        onValueChange={field.onChange}
                                        value={field.value}
                                    >
                                        <SelectTrigger
                                            className={cn(
                                                'w-full bg-foreground text-on-foreground',
                                            )}
                                        >
                                            <SelectValue placeholder="Выберите пол" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="male">
                                                Мужской
                                            </SelectItem>
                                            <SelectItem value="female">
                                                Женский
                                            </SelectItem>
                                        </SelectContent>
                                    </Select>
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
                                        type="password"
                                        startIcon={Lock}
                                        placeholder="Пароль"
                                        {...field}
                                    />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="confirmPassword"
                        render={({ field }) => (
                            <FormItem>
                                <FormControl>
                                    <Input
                                        type="password"
                                        startIcon={Lock}
                                        placeholder="Подтвердите пароль"
                                        {...field}
                                    />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                </div>
                <Button type="submit" className="w-full">
                    Зарегистрироваться
                </Button>
            </form>
        </Form>
    );
};

export default Register;
