import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';
import type { UserInfoResponse } from '@/hooks/useUserInfo.ts';

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

export function replaceUrl(user: UserInfoResponse | null | undefined) {
    if (!user || !user.profile_pic_url) return;

    return user.profile_pic_url.replace('127.0.0.1', 'http://localhost:5173');
}
