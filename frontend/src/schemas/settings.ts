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

    email: z
        .string()
        .describe('Почта')
        .email({ message: 'Введите корректный адрес электронной почты' }),

    nickname: z
        .string()
        .describe('Никнейм')
        .min(2, { message: 'Никнейм должен содержать минимум 2 символа' })
        .max(50, { message: 'Никнейм не должен превышать 50 символов' }),

    password: z
        .string()
        .describe('Пароль')
        .min(8, { message: 'Пароль должен содержать минимум 8 символов' })
        .max(50, { message: 'Пароль не должен превышать 50 символов' }),
});
