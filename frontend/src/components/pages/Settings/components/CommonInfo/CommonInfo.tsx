import { FormControl, FormField, FormItem } from '@/components/ui/form.tsx';
import { SettingsItem } from '@/components/pages/Settings/components/SettingsItem';
import { Input } from '@/components/ui/input.tsx';
import type { UseFormReturn } from 'react-hook-form';
import { settingsSchema } from '@/schemas/settings';
import type z from 'zod';
import { DateTimePicker } from '@/components/ui/datetime-picker';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale/ru';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select';

type SettingsFormData = z.infer<typeof settingsSchema>;

interface CommonInfoProps {
    form: UseFormReturn<SettingsFormData>;
    handleSave: () => void;
    values: SettingsFormData;
}

const CommonInfo = ({ form, handleSave, values }: CommonInfoProps) => {
    return (
        <section>
            <FormField
                control={form.control}
                name="firstName"
                render={({ field }) => (
                    <FormItem>
                        <FormControl>
                            <SettingsItem
                                name="Имя"
                                value={values.firstName}
                                onSave={handleSave}
                            >
                                <Input placeholder="Введите имя" {...field} />
                            </SettingsItem>
                        </FormControl>
                    </FormItem>
                )}
            />

            <FormField
                control={form.control}
                name="lastName"
                render={({ field }) => (
                    <FormItem>
                        <FormControl>
                            <SettingsItem
                                name="Фамилия"
                                value={values.lastName}
                                onSave={handleSave}
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
                                onSave={handleSave}
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

            <FormField
                control={form.control}
                name="gender"
                render={({ field }) => (
                    <FormItem>
                        <FormControl>
                            <SettingsItem
                                name="Пол"
                                value={
                                    values.gender === 'male'
                                        ? 'Мужской'
                                        : 'Женский'
                                }
                                onSave={handleSave}
                            >
                                <Select
                                    onValueChange={field.onChange}
                                    defaultValue={field.value}
                                >
                                    <SelectTrigger className="w-full text-primary">
                                        <SelectValue
                                            className=""
                                            placeholder="Гендер"
                                        />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value={'male'}>
                                            Мужской
                                        </SelectItem>
                                        <SelectItem value={'female'}>
                                            Женский
                                        </SelectItem>
                                    </SelectContent>
                                </Select>
                            </SettingsItem>
                        </FormControl>
                    </FormItem>
                )}
            />
        </section>
    );
};

export default CommonInfo;
