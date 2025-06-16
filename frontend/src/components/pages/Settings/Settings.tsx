import { useForm } from 'react-hook-form';
import { settingsSchema } from '@/schemas/settings.ts';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { Form } from '@/components/ui/form.tsx';
import { CommonInfo } from './components/CommonInfo';

const Settings = () => {
    type SettingsFormData = z.infer<typeof settingsSchema>;

    const form = useForm<SettingsFormData>({
        resolver: zodResolver(settingsSchema),
        defaultValues: {
            fullName: 'Вера Неттор',
            birthDate: new Date(2000, 12, 31),
            gender: 'Женский',
            email: 'VeraNettor2002@gmail.com',
            nickname: 'VeraNettor',
            password: '',
        },
    });

    const values = form.getValues();

    function onSubmit(values: SettingsFormData) {
        console.log('submitting');
        console.log(values);
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)}>
                <CommonInfo
                    form={form}
                    onSubmit={form.handleSubmit(onSubmit)}
                    values={values}
                />
            </form>
        </Form>
    );
};

export default Settings;
