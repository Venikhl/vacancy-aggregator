import React from "react";
import { Search } from "lucide-react";
import { useForm } from "react-hook-form";

import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
} from "@/components/ui/form";
import {
  Select,
  SelectTrigger,
  SelectContent,
  SelectItem,
  SelectValue,
} from "@/components/ui/select";

import type { Filters } from "@/types/filters";

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

  const { control, watch } = form;

  React.useEffect(() => {
    const subscription = watch((value) => {
      const cleaned: Filters = {
        ...value,
        experience: value.experience?.filter((v): v is string => typeof v === "string"),
        sources: value.sources?.filter((v): v is string => typeof v === "string"),
      };
      onChange(cleaned);
    });

    return () => subscription.unsubscribe();
  }, [watch, onChange]);

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onApply)}
        className="bg-white text-black rounded-2xl p-6 shadow-md space-y-6"
      >
        {/* Поиск */}
        <div className="flex flex-wrap items-center gap-4">
          <FormField
            control={control}
            name="keyword"
            render={({ field }) => (
              <FormItem className="flex-grow">
                <FormControl>
                  <Input
                    {...field}
                    placeholder="Должность, навыки, компания"
                    startIcon={Search}
                  />
                </FormControl>
              </FormItem>
            )}
          />
          <Button type="submit" variant="default" size="default">
            <Search size={16} />
            Поиск
          </Button>
        </div>

        {/* Фильтры */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 items-start">

          {/* Регион */}
          <FormField
            control={control}
            name="region"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Регион</FormLabel>
                <FormControl>
                  <Select
                    value={field.value || "unset"}
                    onValueChange={(value) =>
                      field.onChange(value === "unset" ? undefined : value)
                    }
                  >
                    <SelectTrigger className="w-full">
                      <SelectValue placeholder="Выберите регион" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="unset">Не выбрано</SelectItem>
                      <SelectItem value="Москва">Москва</SelectItem>
                      <SelectItem value="Санкт-Петербург">Санкт-Петербург</SelectItem>
                      <SelectItem value="Екатеринбург">Екатеринбург</SelectItem>
                    </SelectContent>
                  </Select>
                </FormControl>
              </FormItem>
            )}
          />


          {/* Зарплата */}
          <FormField
            control={control}
            name="salary.max"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Максимальная зарплата</FormLabel>
                <FormControl>
                  <input
                    type="range"
                    min={30000}
                    max={150000}
                    step={5000}
                    {...field}
                    value={field.value ?? 150000}
                  />
                </FormControl>
                <div className="flex justify-between text-xs mt-1 text-gray-500">
                  <span>30 000 ₽</span>
                  <span>{field.value?.toLocaleString() ?? "—"} ₽</span>
                </div>
              </FormItem>
            )}
          />

          {/* Опыт */}
          <FormField
            control={control}
            name="experience"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Опыт работы</FormLabel>
                <div className="space-y-1 text-sm">
                  {["Без опыта", "1–3 года", "3–6 лет", "Более 6 лет"].map((exp) => (
                    <label key={exp} className="flex items-center gap-2">
                      <Checkbox
                        checked={(field.value ?? []).includes(exp)}
                        onCheckedChange={(checked) => {
                          const arr = field.value ?? [];
                          const newValue = checked
                            ? [...arr, exp]
                            : arr.filter((v) => v !== exp);
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

          {/* Источники */}
          <FormField
            control={control}
            name="sources"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Источники</FormLabel>
                <div className="space-y-1 text-sm">
                  {["HH.ru", "Работа.ру", "SuperJob"].map((source) => (
                    <label key={source} className="flex items-center gap-2">
                      <Checkbox
                        checked={(field.value ?? []).includes(source)}
                        onCheckedChange={(checked) => {
                          const arr = field.value ?? [];
                          const newValue = checked
                            ? [...arr, source]
                            : arr.filter((v) => v !== source);
                          field.onChange(newValue);
                        }}
                      />
                      {source}
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
