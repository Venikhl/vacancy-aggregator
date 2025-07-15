import { z } from 'zod';

export const registerFormSchema = z
    .object({
        first_name: z
            .string()
            .min(2, 'Имя должно содержать минимум 2 символа')
            .max(50, 'Имя должно содержать не более 50 символов'),

        last_name: z
            .string()
            .min(2, 'Фамилия должна содержать минимум 2 символа')
            .max(50, 'Фамилия должна содержать не более 50 символов'),

        email: z.string().email('Неверный формат e-mail').min(2).max(50),

        password: z
            .string()
            .min(8, 'Пароль должен содержать минимум 8 символов')
            .max(50),

        confirmPassword: z
            .string()
            .min(8, 'Пароль должен содержать минимум 8 символов')
            .max(50),

        birth_date: z
            .string()
            .regex(
                /^\d{4}-\d{2}-\d{2}$/,
                'Дата рождения должна быть в формате ГГГГ-ММ-ДД',
            ),

        gender: z.enum(['male', 'female'], {
            errorMap: () => ({
                message:
                    'Пол должен быть либо "Мужской", либо "Женский". Вертолёт это не пол.',
            }),
        }),
    })
    .superRefine(({ password, confirmPassword }, ctx) => {
        if (password !== confirmPassword) {
            ctx.addIssue({
                code: z.ZodIssueCode.custom,
                message: 'Пароли не совпадают',
                path: ['confirmPassword'],
            });
        }
    });
