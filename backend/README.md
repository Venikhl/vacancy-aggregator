# vacancy-aggregator-backend

## Dependencies
- `python 3.11`
- `uv`

## Running

### 1. Setting up environment

```bash
pip install uv
uv sync --frozen
```

### 2. Application Configuration

You must configure the application before running.
The configuration is done either through environment
variables or using the `.env` file.

**Variables**:
- **HOST** - host address of the application (`127.0.0.1` or `localhost` for running locally)
- **PROTOCOL** - `http` or `https` depending on the way of hosting
- **APP_NAME** - name of the application
- **DATABASE_URL** - URL for the application to connect to the database

  example: `postgresql+asyncpg://<user>:<password>@<host>:<port>/`

- **JWT_KEY** - JWT key for the authentication
- **PROFILE_PICTURE_DIRECTORY** - directory to store profile pictures in
- **ACCESS_TOKEN_EXPIRE_MINUTES** - access token expiration
- **REFRESH_TOKEN_EXPIRE_DAYS** - refresh token expiration
- **HH_CLIENT_ID** - client id for hh.ru
- **HH_CLIENT_SECRET** - client secret for hh.ru
- **HH_ACCESS_TOKEN** - access token for hh.ru

### 3. Database Migration

```bash
uv run alembic upgrade head
```

### 4. Starting the application

```bash
uv run uvicorn app.main:app
```

## API Documentation

See `/docs` endpoint inside the app.
