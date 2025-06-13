import { z } from 'zod';

export const loginFormSchema = z.object({
    username: z
        .string()
        .min(2, 'Имя пользователя должно содержать минимум 2 символа')
        .max(50, 'Имя пользователя должно содержать не более 50 символов'),

    password: z
        .string()
        .min(8, 'Пароль должен содержать минимум 8 символов')
        .max(50, 'Пароль должен содержать не более 50 символов'),

    remember: z.boolean(),
});
