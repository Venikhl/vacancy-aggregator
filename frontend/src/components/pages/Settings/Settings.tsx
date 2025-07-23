import { useForm } from 'react-hook-form';
import { settingsSchema } from '@/schemas/settings.ts';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { Form } from '@/components/ui/form.tsx';
import { CommonInfo } from './components/CommonInfo';
import { useEffect, useState } from 'react';
import { useUserInfo } from '@/hooks/useUserInfo.ts';
import axiosInstance from '@/api';
import { useNavigate } from 'react-router-dom';
import TokenService from '@/api/tokens.ts';
import { ImageUpload } from '@/components/pages/Settings/components/CommonInfo/components/ImageUpload';

const Settings = () => {
    const navigate = useNavigate();
    type SettingsFormData = z.infer<typeof settingsSchema>;

    const { user } = useUserInfo();

    const form = useForm<SettingsFormData>({
        resolver: zodResolver(settingsSchema),
        defaultValues: {
            firstName: '',
            lastName: '',
            birthDate: new Date(2000, 12, 31),
            gender: 'male',
        },
    });

    const [values, setValues] = useState<SettingsFormData>(form.getValues());

    useEffect(() => {
        if (user) {
            form.setValue('firstName', user.first_name);
            form.setValue('lastName', user.last_name);
            form.setValue('birthDate', new Date(user.birth_date));
            form.setValue('gender', user.gender as 'male' | 'female');
            setValues(form.getValues());
        }
    }, [user, form]);

    useEffect(() => {
        if (!TokenService.getLocalAccessToken()) {
            navigate('/login');
        }
    }, [navigate, user]);

    function onSubmit(values: SettingsFormData) {
        axiosInstance
            .post('/update_me', {
                first_name: values.firstName,
                last_name: values.lastName,
                birth_date: JSON.stringify(values.birthDate)
                    .split('T')[0]
                    .slice(1),
                gender: values.gender,
            })
            .then(() => {
                console.log('submitted');
            })
            .catch(() => {
                console.log('err at submitting');
            });
    }

    const handleSave = async () => {
        console.log('saving');
        await form.handleSubmit(onSubmit)();
        setValues(form.getValues());
    };

    return (
        <Form {...form}>
            <h2 className="font-semibold text-3xl pl-3 mb-4">
                Общая Информация
            </h2>

            <ImageUpload />

            <form onSubmit={form.handleSubmit(onSubmit)}>
                <CommonInfo
                    form={form}
                    values={values}
                    handleSave={handleSave}
                />
            </form>
        </Form>
    );
};

export default Settings;
