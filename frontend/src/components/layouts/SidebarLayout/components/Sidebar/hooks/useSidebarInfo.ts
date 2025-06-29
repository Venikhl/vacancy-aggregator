import axiosInstance from '@/api';
import { useEffect, useState } from 'react';

interface UserSidebarInfo {
    first_name: string;
    last_name: string;
    email: string;
}

export function useSidebarInfo() {
    const [value, setValue] = useState<undefined | UserSidebarInfo>();

    useEffect(() => {
        axiosInstance.post('/get_me').then((r) => {
            setValue(r.data);
        });
    }, []);

    return {
        value,
    };
}
