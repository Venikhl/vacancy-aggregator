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
            gender: 'Женский',
        },
    });

    const [values, setValues] = useState<SettingsFormData>(form.getValues());

    useEffect(() => {
        if (user) {
            form.setValue('firstName', user.first_name);
            form.setValue('lastName', user.last_name);
            setValues(form.getValues());
        }
    }, [user, form]);

    useEffect(() => {
        if (!user) {
            navigate('/login');
        }
    }, [navigate, user]);

    function onSubmit(values: SettingsFormData) {
        axiosInstance
            .post('/update_me', {
                first_name: values.firstName,
                last_name: values.lastName,
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
