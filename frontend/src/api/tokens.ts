const ACCESS_TOKEN_KEY = 'vaAccessToken';
const REFRESH_TOKEN_KEY = 'vaRefreshToken';

const TokenService = {
    getLocalAccessToken() {
        return localStorage.getItem(ACCESS_TOKEN_KEY);
    },

    getLocalRefreshToken() {
        return localStorage.getItem(REFRESH_TOKEN_KEY);
    },

    updateLocalAccessToken(token: string) {
        localStorage.setItem(ACCESS_TOKEN_KEY, token);
    },

    setTokens({
        access_token,
        refresh_token,
    }: {
        access_token: string;
        refresh_token: string;
    }) {
        localStorage.setItem(ACCESS_TOKEN_KEY, access_token);
        localStorage.setItem(REFRESH_TOKEN_KEY, refresh_token);
    },

    removeTokens() {
        localStorage.removeItem(ACCESS_TOKEN_KEY);
        localStorage.removeItem(REFRESH_TOKEN_KEY);
    },
};

export default TokenService;
