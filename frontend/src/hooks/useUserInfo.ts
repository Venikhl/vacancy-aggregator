import axiosInstance from '@/api';
import { useEffect, useState } from 'react';

export interface UserInfoResponse {
    first_name: string;
    last_name: string;
    email: string;
    gender: string;
    profile_pic_url: string;
    birth_date: string;
}

export function useUserInfo() {
    const [isLoading, setIsLoading] = useState(true);
    const [isError, setIsError] = useState(false);

    const [user, setUser] = useState<null | undefined | UserInfoResponse>(
        undefined,
    );

    useEffect(() => {
        axiosInstance
            .post('/get_me')
            .then((r) => {
                setUser(r.data);
            })
            .catch(() => {
                setIsError(true);
                setUser(null);
            })
            .finally(() => setIsLoading(false));
    }, []);

    return {
        user,
        isLoading,
        isError,
    };
}
