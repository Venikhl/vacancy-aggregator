import React from 'react';
import { useForm } from 'react-hook-form';
import { Search } from 'lucide-react';

import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
    Form,
    FormField,
    FormItem,
    FormLabel,
    FormControl,
} from '@/components/ui/form';
import {
    Select,
    SelectTrigger,
    SelectContent,
    SelectItem,
    SelectValue,
} from '@/components/ui/select';

import type { ResumeFilters as ResumeFiltersType } from '@/types/filters';

type Props = {
    filters: ResumeFiltersType;
    onChange: (filters: ResumeFiltersType) => void;
    onApply: () => void;
    onReset: () => void;
};

export const ResumeFilters: React.FC<Props> = ({
    filters,
    onChange,
    // onApply,
    onReset,
}) => {
    const form = useForm<ResumeFiltersType>({
        defaultValues: filters,
    });

    const { control, getValues, reset } = form;

    React.useEffect(() => {
        reset(filters);
    }, [filters, reset]);

    const handleApply = () => {
        const value = getValues();
        const cleaned: ResumeFiltersType = {
            title: value.title?.trim() || null,
            location:
                typeof value.location === 'string'
                    ? { region: value.location }
                    : value.location?.region
                      ? { region: value.location.region }
                      : null,
            salary_min: value.salary_min ?? null,
            salary_max: value.salary_max ?? null,
            experience_categories: (value.experience_categories ?? [])
                .filter(
                    (
                        v,
                    ): v is {
                        name: string;
                        years_of_experience: number | null;
                    } => !!v?.name,
                )
                .map((v) => ({ name: v.name, years_of_experience: null })),
            skills: (value.skills ?? []).filter((s) => !!s.trim()),
        };
        // console.log('[Фильтр] Отправка фильтра:', cleaned);
        // console.log(JSON.stringify(cleaned.location));
        // console.log(JSON.stringify(cleaned));

        onChange(cleaned);
        // onApply();
    };

    const handleSearch = () => {
        const value = getValues();
        onChange({
            ...filters,
            title: value.title?.trim() || null,
        });
        // onApply();
    };

    return (
        <Form {...form}>
            <form
                onSubmit={(e) => {
                    e.preventDefault();
                    handleApply();
                }}
                className="bg-white text-black rounded-2xl p-6 shadow-md space-y-6"
            >
                {/* Поиск */}
                <div className="flex flex-wrap items-center gap-4">
                    <FormField
                        control={control}
                        name="title"
                        render={({ field }) => (
                            <FormItem className="flex-grow">
                                <FormControl>
                                    <Input
                                        {...field}
                                        placeholder="Должность, имя, навык"
                                        startIcon={Search}
                                        value={field.value ?? ''}
                                    />
                                </FormControl>
                            </FormItem>
                        )}
                    />
                    <Button type="button" onClick={handleSearch}>
                        <Search size={16} />
                        Поиск
                    </Button>
                </div>

                {/* Сетка фильтров */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 items-start">
                    {/* Регион */}
                    <FormField
                        control={control}
                        name="location"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Регион</FormLabel>
                                <FormControl>
                                    <Select
                                        value={field.value?.region ?? 'unset'}
                                        onValueChange={(value) =>
                                            field.onChange(
                                                value === 'unset'
                                                    ? null
                                                    : { region: value },
                                            )
                                        }
                                    >
                                        <SelectTrigger>
                                            <SelectValue placeholder="Выберите регион" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="unset">
                                                Не выбрано
                                            </SelectItem>
                                            {[
                                                'Москва',
                                                'Санкт-Петербург',
                                                'Екатеринбург',
                                                'Новосибирск',
                                                'Казань',
                                                'Нижний Новгород',
                                                'Челябинск',
                                                'Самара',
                                                'Омск',
                                                'Ростов-на-Дону',
                                                'Уфа',
                                                'Красноярск',
                                                'Воронеж',
                                                'Пермь',
                                                'Волгоград',
                                                'Саратов',
                                                'Тюмень',
                                                'Тольятти',
                                                'Ижевск',
                                                'Барнаул',
                                                'Иркутск',
                                                'Кемерово',
                                                'Хабаровск',
                                                'Ярославль',
                                                'Махачкала',
                                                'Томск',
                                                'Оренбург',
                                                'Курск',
                                                'Ульяновск',
                                                'Владивосток',
                                                'Чебоксары',
                                                'Севастополь',
                                                'Тула',
                                                'Калининград',
                                                'Липецк',
                                                'Киров',
                                                'Ставрополь',
                                                'Брянск',
                                                'Белгород',
                                                'Архангельск',
                                                'Рязань',
                                                'Пенза',
                                                'Набережные Челны',
                                                'Астрахань',
                                                'Сочи',
                                                'Якутск',
                                                'Нижневартовск',
                                                'Сургут',
                                                'Грозный',
                                            ].map((region) => (
                                                <SelectItem
                                                    key={region}
                                                    value={region}
                                                >
                                                    {region}
                                                </SelectItem>
                                            ))}
                                        </SelectContent>
                                    </Select>
                                </FormControl>
                            </FormItem>
                        )}
                    />

                    {/* Зарплата */}
                    <FormItem>
                        <FormLabel>Желаемая зарплата</FormLabel>
                        <div className="flex gap-2">
                            <FormField
                                control={control}
                                name="salary_min"
                                render={({ field }) => (
                                    <FormItem className="w-full">
                                        <FormControl>
                                            <Input
                                                type="text"
                                                inputMode="numeric"
                                                placeholder="От"
                                                value={field.value ?? ''}
                                                onChange={(e) => {
                                                    const raw = e.target.value;
                                                    const num = parseInt(raw);
                                                    field.onChange(
                                                        raw === ''
                                                            ? null
                                                            : isNaN(num)
                                                              ? null
                                                              : num,
                                                    );
                                                }}
                                            />
                                        </FormControl>
                                    </FormItem>
                                )}
                            />
                            <FormField
                                control={control}
                                name="salary_max"
                                render={({ field }) => (
                                    <FormItem className="w-full">
                                        <FormControl>
                                            <Input
                                                type="text"
                                                inputMode="numeric"
                                                placeholder="До"
                                                value={field.value ?? ''}
                                                onChange={(e) => {
                                                    const raw = e.target.value;
                                                    const num = parseInt(raw);
                                                    field.onChange(
                                                        raw === ''
                                                            ? null
                                                            : isNaN(num)
                                                              ? null
                                                              : num,
                                                    );
                                                }}
                                            />
                                        </FormControl>
                                    </FormItem>
                                )}
                            />
                        </div>
                    </FormItem>

                    {/* Опыт */}
                    <FormField
                        control={control}
                        name="experience_categories"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Опыт работы</FormLabel>
                                <div className="space-y-1 text-sm">
                                    {[
                                        'Без опыта',
                                        '1–3 года',
                                        '3–6 лет',
                                        'Более 6 лет',
                                    ].map((label) => (
                                        <label
                                            key={label}
                                            className="flex items-center gap-2"
                                        >
                                            <input
                                                type="checkbox"
                                                checked={(
                                                    field.value ?? []
                                                ).some((v) => v.name === label)}
                                                onChange={() => {
                                                    const current =
                                                        field.value ?? [];
                                                    const exists = current.some(
                                                        (v) => v.name === label,
                                                    );
                                                    const updated = exists
                                                        ? current.filter(
                                                              (v) =>
                                                                  v.name !==
                                                                  label,
                                                          )
                                                        : [
                                                              ...current,
                                                              {
                                                                  name: label,
                                                                  years_of_experience:
                                                                      null,
                                                              },
                                                          ];
                                                    field.onChange(updated);
                                                }}
                                            />
                                            {label}
                                        </label>
                                    ))}
                                </div>
                            </FormItem>
                        )}
                    />

                    {/* Навыки */}
                    <FormField
                        control={control}
                        name="skills"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Ключевые навыки</FormLabel>
                                <FormControl>
                                    <Input
                                        placeholder="JavaScript, Python"
                                        value={(field.value ?? []).join(', ')}
                                        onChange={(e) =>
                                            field.onChange(
                                                e.target.value
                                                    .split(',')
                                                    .map((s) => s.trim())
                                                    .filter((s) => s !== ''),
                                            )
                                        }
                                    />
                                </FormControl>
                            </FormItem>
                        )}
                    />
                </div>

                {/* Кнопки */}
                <div className="flex justify-end gap-4 mt-4">
                    <Button type="button" variant="outline" onClick={onReset}>
                        Сбросить
                    </Button>
                    <Button type="submit" variant="default">
                        Применить фильтры
                    </Button>
                </div>
            </form>
        </Form>
    );
};
