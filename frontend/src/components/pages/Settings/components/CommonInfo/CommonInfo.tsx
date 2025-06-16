import { FormControl, FormField, FormItem } from '@/components/ui/form.tsx';
import { SettingsItem } from '@/components/pages/Settings/components/SettingsItem';
import { Input } from '@/components/ui/input.tsx';
import type { UseFormReturn } from 'react-hook-form';
import type { settingsSchema } from '@/schemas/settings';
import type z from 'zod';
import { DateTimePicker } from '@/components/ui/datetime-picker';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale/ru';

type SettingsFormData = z.infer<typeof settingsSchema>;

interface CommonInfoProps {
    form: UseFormReturn<SettingsFormData>;
    values: SettingsFormData;
    onSubmit: () => void;
}

const CommonInfo = ({ form, values, onSubmit }: CommonInfoProps) => {
    return (
        <section>
            <h2>Общая Информация</h2>

            <FormField
                control={form.control}
                name="fullName"
                render={({ field }) => (
                    <FormItem>
                        <FormControl>
                            <SettingsItem
                                name="Имя"
                                value={values.fullName}
                                onSave={onSubmit}
                            >
                                <Input placeholder="Введите имя" {...field} />
                            </SettingsItem>
                        </FormControl>
                    </FormItem>
                )}
            />

            <FormField
                control={form.control}
                name="birthDate"
                render={({ field }) => (
                    <FormItem>
                        <FormControl>
                            <SettingsItem
                                name="Дата Рождения"
                                value={format(values.birthDate, 'd MMMM y', {
                                    locale: ru,
                                })}
                                onSave={onSubmit}
                            >
                                <DateTimePicker
                                    value={field.value}
                                    onChange={field.onChange}
                                    hideTime
                                />
                            </SettingsItem>
                        </FormControl>
                    </FormItem>
                )}
            />
        </section>
    );
};

export default CommonInfo;
