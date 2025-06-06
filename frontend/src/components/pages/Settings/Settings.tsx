import { SettingsItem } from '@/components/pages/Settings/components/SettingsItem';
import { type Path, useForm } from 'react-hook-form';
import { settingsSchema } from '@/schemas/settings.ts';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { Form } from '@/components/ui/form.tsx';

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
        console.log(values);
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)}>
                {Object.entries(settingsSchema.shape).map(
                    ([key, fieldSchema]) => (
                        <SettingsItem
                            key={key}
                            name={key as Path<SettingsFormData>}
                            fieldSchema={fieldSchema}
                            value={
                                values[
                                    key as Path<SettingsFormData>
                                ]?.toString?.() ?? ''
                            }
                            control={form.control}
                            onSave={form.handleSubmit(onSubmit)}
                        />
                    ),
                )}
            </form>
        </Form>
    );
};

export default Settings;
