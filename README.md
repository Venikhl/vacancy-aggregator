# vacancy-aggregator

## Dependencies

- `Docker`
- `Docker Compose`

## Running

### 1. Configuration

You must configure the application before running.
The configuration is done either through environment
variables or using the `.env` file.

**Variables**:
- **HOST** - host address of the application (`127.0.0.1` or `localhost` for running locally)
- **PROTOCOL** - `http` or `https` depending on the way of hosting
- **APP_NAME** - name of the application
- **JWT_KEY** - JWT key for the authentication
- **ACCESS_TOKEN_EXPIRE_MINUTES** - access token expiration
- **REFRESH_TOKEN_EXPIRE_DAYS** - refresh token expiration
- **HH_CLIENT_ID** - client id for hh.ru
- **HH_CLIENT_SECRET** - client secret for hh.ru
- **HH_ACCESS_TOKEN** - access token for hh.ru

### 2. Starting the application

```bash
docker-compose up -d
```
