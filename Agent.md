# Agent Guide

## Project Overview

This project is a residential community access control information system.

- Backend: Django 6.0.6
- Admin UI: django-simpleui
- Frontend: Vue 3 + Vite
- Database: SQLite, stored at `db.sqlite3`
- Python virtual environment: `.venv`

The Django admin remains available at `/admin/`. The public frontend is served by Django from the Vue production build in `frontend/dist`.

## Directory Layout

- `manage.py`: Django management entry point.
- `config/`: Django project settings, URL routing, ASGI, and WSGI configuration.
- `access_control/`: Django app for access-control business logic.
- `frontend/`: Vue 3 + Vite frontend project.
- `frontend/dist/`: Built Vue assets served by Django.
- `requirements.txt`: Python dependency lock list for the current environment.
- `db.sqlite3`: Local development SQLite database.
- `django-server.log` and `django-server.err.log`: Development server logs.

## Backend Commands

Run commands from the project root:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

If PowerShell blocks virtual environment activation, use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\.venv\Scripts\Activate.ps1
```

Direct `.venv` commands are preferred because they do not depend on shell activation.

## Frontend Commands

Run commands from `frontend/`:

```powershell
npm install
npm run dev
npm run build
```

After editing Vue source files, run `npm run build` so Django can serve the updated frontend from `frontend/dist`.

If `npm` is blocked by PowerShell script policy, use:

```powershell
& 'C:\Program Files\nodejs\npm.cmd' run build
```

## Runtime URLs

- Public Vue frontend: `http://127.0.0.1:8000/`
- Django admin: `http://127.0.0.1:8000/admin/`

## Existing Admin Account

Local development superuser:

- Username: `ljd`
- Password: `ljd`
- Email: `3103192799@qq.com`
- Display name: `ho_ok`

The display name is stored in Django's default `first_name` field.

## Django Integration Notes

- `config/settings.py` registers `simpleui` before `django.contrib.admin`.
- `LANGUAGE_CODE` is `zh-hans`.
- `TIME_ZONE` is `Asia/Shanghai`.
- `TEMPLATES["DIRS"]` includes `BASE_DIR / "frontend" / "dist"`.
- `STATICFILES_DIRS` maps Vue build assets to `/static/frontend/`.
- `config/urls.py` serves Vue's `index.html` for `/` and other non-admin SPA paths.

Keep `/admin/` before the SPA catch-all route so the Django admin is not intercepted by Vue routing.

## Development Guidance

- Keep backend business logic inside `access_control/`.
- Keep Vue UI changes inside `frontend/src/`.
- Do not edit generated files in `frontend/dist/` directly; edit `frontend/src/` and rebuild.
- Do not commit or depend on local log files for application behavior.
- Prefer Django ORM and migrations for database changes.
- For new Python dependencies, install them into `.venv` and update `requirements.txt`.
- For new frontend dependencies, install them under `frontend/` and keep `package.json` and `package-lock.json` in sync.

## Verification Checklist

Before handing off changes, run:

```powershell
.\.venv\Scripts\python.exe manage.py check
```

For frontend changes, also run:

```powershell
cd frontend
npm run build
```

Then verify:

- `http://127.0.0.1:8000/` loads the Vue frontend.
- `http://127.0.0.1:8000/admin/` loads the Django simple-ui admin.
