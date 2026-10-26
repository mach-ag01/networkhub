# Deployment guide
## GitHub
Upload the contents of this project folder so `frontend/` and `backend/` are at repository root.

## Render API
Create PostgreSQL, then create a Web Service with root directory `backend`.
Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
Start: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 60`
Set `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=your-api.onrender.com`, `DATABASE_URL` (Render DB URL), `CORS_ALLOWED_ORIGINS=https://your-site.vercel.app`, `CSRF_TRUSTED_ORIGINS=https://your-site.vercel.app`, `SECURE_SSL_REDIRECT=True`; optionally `REDIS_URL`.
Create a staff user with Render Shell: `python manage.py createsuperuser`. Verify `/health/` and `/api/v1/products/`.

## Vercel frontend
Import the repository; root directory `frontend`, build `npm run build`, output `dist`. Set `VITE_API_BASE_URL=https://your-api.onrender.com`, then redeploy.

## Production notes
DRF throttles are application-level rate limits, not DDoS protection. Use provider edge protections, shared Redis when scaling multiple API instances, database backups and load testing. Review all security and privacy requirements before production use.
