import axiosInstance from '@/api';
import { useEffect, useState } from 'react';

interface UserInfoResponse {
    first_name: string;
    last_name: string;
    email: string;
}

export function useUserInfo() {
    const [isLoading, setIsLoading] = useState(true);
    const [isError, setIsError] = useState(false);

    const [user, setUser] = useState<undefined | UserInfoResponse>();

    useEffect(() => {
        axiosInstance
            .post('/get_me')
            .then((r) => {
                setUser(r.data);
            })
            .catch(() => setIsError(true))
            .finally(() => setIsLoading(false));
    }, []);

    return {
        user,
        isLoading,
        isError,
    };
}
