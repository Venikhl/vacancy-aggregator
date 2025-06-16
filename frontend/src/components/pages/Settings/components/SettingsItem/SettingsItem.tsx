import {
    Dialog,
    DialogClose,
    DialogContent,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from '@/components/ui/dialog';
import type { FieldValues, Path } from 'react-hook-form';
import { Button } from '@/components/ui/button';
import { ChevronRight } from 'lucide-react';
import type { ReactNode } from 'react';
import { FormMessage } from '@/components/ui/form';

interface SettingsItemProps<T extends FieldValues = FieldValues> {
    name: Path<T>;
    value: T[keyof T];
    onSave: () => void;
    children: ReactNode;
}

const SettingsItem = <T extends FieldValues = FieldValues>({
    name,
    value,
    onSave,
    children,
}: SettingsItemProps<T>) => {
    return (
        <Dialog>
            <DialogTrigger asChild>
                <Button
                    variant="transparent"
                    className="w-full h-fit flex justify-between items-center py-4 border-b border-primary text-left hover:bg-background transition rounded-none"
                >
                    <div>
                        <div className="text-secondary text-sm">{name}</div>
                        <div className="font-semibold text-[18px] break-words max-w-[70vw]">
                            {value.toString()}
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
                        Изменить {name.toLowerCase()}
                    </DialogTitle>
                </DialogHeader>

                {children}

                <FormMessage />

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
