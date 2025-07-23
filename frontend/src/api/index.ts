import axios from 'axios';
import TokenService from './tokens';
import type { Filters } from '@/types/filters';

if (!import.meta.env.VITE_API_HOST) {
  throw new Error('VITE_API_HOST is not defined in environment variables');
}
const API_HOST = import.meta.env.VITE_API_HOST;

const API_BASE_URL = `${API_HOST}/api/v1`;
const REFRESH_TOKEN_URL = '/refresh_token';

const axiosInstance = axios.create({
    baseURL: API_BASE_URL,
    headers: { 'Content-Type': 'application/json' },
});

const refreshInstance = axios.create({
    baseURL: API_BASE_URL,
    headers: { 'Content-Type': 'application/json' },
});

axiosInstance.interceptors.request.use(
    (config) => {
        try {
            const token = TokenService.getLocalAccessToken();
            if (token) config.headers['Authorization'] = `Bearer ${token}`;
            return config;
        } catch (error) {
            return Promise.reject(error);
        }
    },
    (error) => Promise.reject(error),
);

axiosInstance.interceptors.response.use(
    (res) => res,
    async (err) => {
        const originalConfig = err.config;

        if (err.response) {
            if (err.response.status === 401 && !originalConfig._retry) {
                originalConfig._retry = true;

                try {
                    const refreshToken = TokenService.getLocalRefreshToken();
                    if (!refreshToken)
                        return Promise.reject('No refresh token');

                    const rs = await refreshInstance.post(REFRESH_TOKEN_URL, {
                        refresh_token: refreshToken,
                    });

                    const { access_token } = rs.data;
                    TokenService.updateLocalAccessToken(access_token);

                    return axiosInstance(originalConfig);
                } catch (refreshError) {
                    return Promise.reject(refreshError);
                }
            } else if (originalConfig._retry) {
                TokenService.removeTokens();
                return Promise.reject('Refresh Token Expired, Re-Sign-In');
            }
        }

        return Promise.reject(err);
    },
);

export default axiosInstance;

export const getVacancies = async (
    offset: number,
    count: number,
    filters: Filters,
) => {
    return axiosInstance.post('/vacancies', {
        filter: filters,
        view: { offset, count },
    });
};

export const getVacancyById = async (id: number | string) => {
    return axiosInstance.get(`/vacancy/${id}`);
};
