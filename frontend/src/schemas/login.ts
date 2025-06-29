import { z } from 'zod';

export const loginFormSchema = z.object({
    email: z
        .string()
        .email()
        .min(2, 'Почта должна содержать минимум 2 символа')
        .max(50, 'Почта должна содержать не более 50 символов'),

    password: z
        .string()
        .min(8, 'Пароль должен содержать минимум 8 символов')
        .max(50, 'Пароль должен содержать не более 50 символов'),

    remember: z.boolean(),
});
