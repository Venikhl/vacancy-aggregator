import {
    Dialog,
    DialogClose,
    DialogContent,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from '@/components/ui/dialog';
import {
    FormControl,
    FormField,
    FormItem,
    FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import type {
    Control,
    ControllerRenderProps,
    FieldValues,
    Path,
} from 'react-hook-form';
import { Button } from '@/components/ui/button.tsx';
import { z } from 'zod';
import type { ChangeEvent } from 'react';
import { ChevronRight } from 'lucide-react';

interface SettingsItemProps<T extends FieldValues = FieldValues> {
    name: Path<T>;
    fieldSchema:
        | z.ZodString
        | z.ZodDate
        | z.ZodEnum<['Мужской', 'Женский', 'Другое']>;
    value: string;
    control: Control<T>;
    onSave: () => void;
}

const SettingsItem = <T extends FieldValues = FieldValues>({
    fieldSchema,
    name,
    value,
    control,
    onSave,
}: SettingsItemProps<T>) => {
    const getType = () => {
        if (fieldSchema instanceof z.ZodDate) return 'date';
        if (name.toLowerCase().includes('password')) return 'password';
        return 'text';
    };

    const getValue = () => {
        if (getType() === 'password')
            return Array.from({ length: value.length || 8 }).join('*');
        return value;
    };

    const onValueChange = (
        e: ChangeEvent<HTMLInputElement>,
        field: ControllerRenderProps<T, Path<T>>,
    ) => {
        if (fieldSchema instanceof z.ZodDate) {
            field.onChange(new Date(e.target.value));
        } else {
            field.onChange(e.target.value);
        }
    };

    return (
        <Dialog>
            <DialogTrigger asChild>
                <Button
                    variant="transparent"
                    className="w-full h-fit flex justify-between items-center py-4 border-b border-primary text-left hover:bg-background transition rounded-none"
                >
                    <div>
                        <div className="text-secondary text-sm">
                            {fieldSchema.description}
                        </div>
                        <div className="font-medium break-words max-w-[70vw]">
                            {getValue()}
                        </div>
                    </div>
                    <ChevronRight
                        size={26}
                        className="text-secondary shrink-0"
                    />
                </Button>
            </DialogTrigger>

            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle className="text-primary">
                        Изменить {fieldSchema.description?.toLowerCase()}
                    </DialogTitle>
                </DialogHeader>

                <FormField
                    control={control}
                    name={name}
                    render={({ field }) => (
                        <FormItem>
                            <FormControl>
                                <Input
                                    {...field}
                                    placeholder={fieldSchema.description}
                                    type={getType()}
                                    value={field.value ?? ''}
                                    onChange={(e) => onValueChange(e, field)}
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <DialogFooter>
                    <DialogClose>
                        <Button variant="outline">Отменить</Button>
                    </DialogClose>
                    <DialogClose asChild>
                        <Button onClick={onSave}>Сохранить</Button>
                    </DialogClose>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
};

export default SettingsItem;
