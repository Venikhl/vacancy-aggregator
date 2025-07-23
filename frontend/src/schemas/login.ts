import { z } from 'zod';

const whitelist = [
    'gmail.com',
    'yahoo.com',
    'hotmail.com',
    'aol.com',
    'outlook.com',
    'icloud.com',
    'mail.com',
    'protonmail.com',
    'yandex.com',
    'zoho.com',
    'yandex.ru',
    'mail.ru',
    'rambler.ru',
    'inbox.ru',
];

export const loginFormSchema = z.object({
    email: z
        .string()
        .email()
        .min(2, 'Почта должна содержать минимум 2 символа')
        .max(50, 'Почта должна содержать не более 50 символов')
        .refine(
            (email) => {
                const domain = email.split('@')[1].toLowerCase();
                return whitelist.includes(domain);
            },
            {
                message: 'Домен электронной почты не разрешен',
            },
        ),

    password: z
        .string()
        .min(8, 'Пароль должен содержать минимум 8 символов')
        .max(50, 'Пароль должен содержать не более 50 символов'),

    remember: z.boolean(),
});
