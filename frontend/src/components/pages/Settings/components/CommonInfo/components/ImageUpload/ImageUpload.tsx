import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { useState } from 'react';
import { settingsAvatarSchema } from '@/schemas/settings.ts';

type ImageUploadSchema = z.infer<typeof settingsAvatarSchema>;

const ImageUpload = () => {
    const form = useForm<ImageUploadSchema>({
        resolver: zodResolver(settingsAvatarSchema),
    });

    const [previewUrl, setPreviewUrl] = useState<string | null>(null);

    const onSubmit = (data: ImageUploadSchema) => {
        const file = data.image[0];
        console.log('Отправка файла:', file);
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            setPreviewUrl(URL.createObjectURL(file));
        }
    };

    return (
        <Form {...form}>
            <form
                onSubmit={form.handleSubmit(onSubmit)}
                className="space-y-4 pl-3"
            >
                <h3 className="text-secondary text-sm font-semibold">
                    Изображение профиля
                </h3>

                <img
                    src={previewUrl ? previewUrl : '/user-avatar.png'}
                    alt="Аватар"
                    className="w-20 h-20 rounded-full"
                />

                <FormField
                    control={form.control}
                    name="image"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Загрузить изображение</FormLabel>
                            <FormControl className="cursor-pointer">
                                <Input
                                    type="file"
                                    accept="image/*"
                                    onChange={(e) => {
                                        field.onChange(e.target.files);
                                        handleFileChange(e);
                                    }}
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <Button type="submit" disabled={!previewUrl}>
                    Загрузить
                </Button>
            </form>
        </Form>
    );
};

export default ImageUpload;
