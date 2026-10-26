# NetworkHub
Full-stack Kenya-first networking equipment and ICT services marketplace MVP.

## Included
- React + Vite responsive frontend: homepage, product search/filter/detail, technician directory, service detail, login/register, customer/seller/technician dashboards, staff dashboard.
- Django REST Framework API: JWT auth, role profiles, product and service CRUD, favorites, enquiries, analytics-consent endpoint, admin overview, health endpoint.
- PostgreSQL-ready configuration, optional Redis cache, API throttling, CORS and production security settings.
- Cookie consent banner and responsive UI.

## Structure
`frontend/` React application for Vercel. `backend/` Django API for Render.

## Local run
Backend: `cd backend`, create/activate a Python virtual environment, `pip install -r requirements.txt`, copy `.env.example` to `.env`, run `python manage.py migrate`, `python manage.py createsuperuser`, `python manage.py runserver`.
Frontend: `cd frontend`, copy `.env.example` to `.env`, run `npm install`, then `npm run dev`.
Set `VITE_API_BASE_URL=http://127.0.0.1:8000`.

## Deployment
Read `DEPLOYMENT.md`. Set secrets in the hosting provider, never commit `.env`. This is a functional MVP foundation, not a finished payment/escrow platform. M-Pesa, email, uploads, live chat, identity verification and production moderation are not integrated.
