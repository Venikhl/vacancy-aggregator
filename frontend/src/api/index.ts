import axios from 'axios';
import TokenService from './tokens';

const API_BASE_URL = 'http://localhost:5173/api/v1';
const REFRESH_TOKEN_URL = '/refresh_token';

const axiosInstance = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

const refreshInstance = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

axiosInstance.interceptors.request.use(
    (config) => {
        try {
            const token = TokenService.getLocalAccessToken();
            if (token) {
                config.headers['Authorization'] = `Bearer ${token}`;
            }
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
                    if (!refreshToken) {
                        return Promise.reject('No refresh token');
                    }

                    const rs = await refreshInstance.post(REFRESH_TOKEN_URL, {
                        refresh_token: refreshToken,
                    });

                    const { access_token } = rs.data;
                    TokenService.updateLocalAccessToken(access_token);

                    return axiosInstance(originalConfig);
                } catch (refreshError) {
                    return Promise.reject(refreshError);
                }
            }
        }

        return Promise.reject(err);
    },
);

export default axiosInstance;
