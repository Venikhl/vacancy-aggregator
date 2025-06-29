import React from 'react';
import { Search } from 'lucide-react';
import { useForm } from 'react-hook-form';

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

import type { Filters } from '@/types/filters';

type Props = {
    filters: Filters;
    onChange: (filters: Filters) => void;
    onApply: () => void;
    onReset: () => void;
};

export const VacancyFilters: React.FC<Props> = ({
    filters,
    onChange,
    onApply,
    onReset,
}) => {
    const form = useForm<Filters>({
        defaultValues: filters,
    });

    const { control, getValues, reset } = form;

    React.useEffect(() => {
        reset(filters);
    }, [filters, reset]);

    const handleApply = () => {
        const value = getValues();
        const cleaned: Filters = {
            title: value.title?.trim() ?? '',
            salary_min: value.salary_min ?? 0,
            salary_max: value.salary_max ?? 15000000,
            experience_categories: (value.experience_categories ?? [])
                .filter((v): v is { name: string } => !!v?.name)
                .map((v) => ({ name: v.name })),
            location:
                typeof value.location === 'string'
                    ? { region: value.location }
                    : value.location?.region
                      ? { region: value.location.region }
                      : null,
        };
        onChange(cleaned);
        onApply();
    };

    const handleSearch = () => {
        const value = getValues();
        const cleaned: Filters = {
            ...filters,
            title: value.title?.trim() ?? '',
        };
        onChange(cleaned);
        onApply();
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
                {/* Поиск по названию */}
                <div className="flex flex-wrap items-center gap-4">
                    <FormField
                        control={control}
                        name="title"
                        render={({ field }) => (
                            <FormItem className="flex-grow">
                                <FormControl>
                                    <Input
                                        {...field}
                                        placeholder="Поиск по названию вакансии"
                                        startIcon={Search}
                                    />
                                </FormControl>
                            </FormItem>
                        )}
                    />
                    <Button
                        type="button"
                        variant="default"
                        size="default"
                        onClick={handleSearch}
                    >
                        <Search size={16} />
                        Поиск
                    </Button>
                </div>

                {/* Фильтры */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 items-start">
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
                                        <SelectTrigger className="w-full">
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
                    <div className="col-span-1 flex flex-col gap-1">
                        <FormLabel>Зарплата</FormLabel>
                        <div className="flex gap-2">
                            {/* От */}
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
                                                value={
                                                    field.value === 0
                                                        ? ''
                                                        : field.value
                                                }
                                                onChange={(e) => {
                                                    const raw = e.target.value;
                                                    const num = parseInt(raw);
                                                    if (raw === '')
                                                        field.onChange(0);
                                                    else if (!isNaN(num))
                                                        field.onChange(num);
                                                }}
                                                className="appearance-none"
                                            />
                                        </FormControl>
                                    </FormItem>
                                )}
                            />

                            {/* До */}
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
                                                value={
                                                    field.value === 0
                                                        ? ''
                                                        : field.value
                                                }
                                                onChange={(e) => {
                                                    const raw = e.target.value;
                                                    const num = parseInt(raw);
                                                    if (raw === '')
                                                        field.onChange(0);
                                                    else if (!isNaN(num))
                                                        field.onChange(num);
                                                }}
                                                className="appearance-none"
                                            />
                                        </FormControl>
                                    </FormItem>
                                )}
                            />
                        </div>
                    </div>

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
                                        '1-3 года',
                                        '3-6 лет',
                                        'Более 6 лет',
                                    ].map((exp) => (
                                        <label
                                            key={exp}
                                            className="flex items-center gap-2"
                                        >
                                            <input
                                                type="checkbox"
                                                checked={(
                                                    field.value ?? []
                                                ).some((v) => v.name === exp)}
                                                onChange={() => {
                                                    const current =
                                                        field.value ?? [];
                                                    const exists = current.some(
                                                        (v) => v.name === exp,
                                                    );
                                                    const newValue = exists
                                                        ? current.filter(
                                                              (v) =>
                                                                  v.name !==
                                                                  exp,
                                                          )
                                                        : [
                                                              ...current,
                                                              { name: exp },
                                                          ];
                                                    field.onChange(newValue);
                                                }}
                                            />
                                            {exp}
                                        </label>
                                    ))}
                                </div>
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
