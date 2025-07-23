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
import axiosInstance from '@/api';
import { useUserInfo } from '@/hooks/useUserInfo.ts';
import { replaceUrl } from '@/lib/utils.ts';

type ImageUploadSchema = z.infer<typeof settingsAvatarSchema>;

const ImageUpload = () => {
    const form = useForm<ImageUploadSchema>({
        resolver: zodResolver(settingsAvatarSchema),
    });

    const { user } = useUserInfo();

    const [previewUrl, setPreviewUrl] = useState<string | null>(null);

    const onSubmit = async (data: ImageUploadSchema) => {
        const file = data.image[0];
        const formData = new FormData();
        formData.append('profile_pic', file);

        try {
            await axiosInstance.post('/update_profile_pic', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
        } catch (error) {
            console.error('Ошибка загрузки изображения:', error);
        }
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            const img = new Image();
            img.onload = () => {
                if (img.width === img.height) {
                    setPreviewUrl(URL.createObjectURL(file));
                    form.setValue('image', e.target.files);
                    form.clearErrors('image');
                } else {
                    setPreviewUrl(null);
                    form.setError('image', {
                        type: 'manual',
                        message: 'Пожалуйста, загрузите квадратное изображение',
                    });
                }
            };
            img.src = URL.createObjectURL(file);
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
                    src={previewUrl || replaceUrl(user) || '/user-avatar.png'}
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
