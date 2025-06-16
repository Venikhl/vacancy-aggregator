import { z } from 'zod';

export const settingsSchema = z.object({
    fullName: z
        .string()
        .describe('Имя')
        .min(2, { message: 'Имя должно содержать минимум 2 символа' })
        .max(50, { message: 'Имя не должно превышать 50 символов' }),

    birthDate: z.date().describe('Дата Рождения'),

    gender: z
        .enum(['Мужской', 'Женский', 'Другое'], {
            errorMap: () => ({ message: 'Выберите корректный гендер' }),
        })
        .describe('Гендер'),

    nickname: z
        .string()
        .describe('Никнейм')
        .min(2, { message: 'Никнейм должен содержать минимум 2 символа' })
        .max(50, { message: 'Никнейм не должен превышать 50 символов' }),
});

export const settingsEmailSchema = z.object({
    email: z
        .string({
            required_error: 'Email обязателен',
            invalid_type_error: 'Email должен быть строкой',
        })
        .min(5, { message: 'Email слишком короткий' })
        .max(50, { message: 'Email слишком длинный' })
        .email({ message: 'Введите корректный email' })
        .refine((val) => val.trim() === val, {
            message: 'Email не должен содержать пробелов в начале или в конце',
        }),
});

export const settingsPasswordSchema = z
    .object({
        password: z
            .string({
                required_error: 'Пароль обязателен',
                invalid_type_error: 'Пароль должен быть строкой',
            })
            .min(8, { message: 'Пароль должен содержать не менее 8 символов' })
            .max(100, { message: 'Пароль слишком длинный' })
            .regex(/[A-Z]/, {
                message: 'Пароль должен содержать хотя бы одну заглавную букву',
            })
            .regex(/[a-z]/, {
                message: 'Пароль должен содержать хотя бы одну строчную букву',
            })
            .regex(/[0-9]/, {
                message: 'Пароль должен содержать хотя бы одну цифру',
            })
            .regex(/[^A-Za-z0-9]/, {
                message: 'Пароль должен содержать хотя бы один спецсимвол',
            }),

        passwordAgain: z.string({
            required_error: 'Повтор пароля обязателен',
            invalid_type_error: 'Пароль должен быть строкой',
        }),
    })
    .refine((data) => data.password === data.passwordAgain, {
        path: ['passwordAgain'],
        message: 'Пароли не совпадают',
    });
