# 📋 Deployment Checklist - Brza Referenca

## Pre-Deployment (Lokalno)

- [x] ✅ requirements.txt kreiran
- [x] ✅ runtime.txt kreiran (Python 3.12.3)
- [x] ✅ Procfile kreiran
- [x] ✅ settings.py pripremljen za production
- [x] ✅ whitenoise instaliran i konfigurisan
- [x] ✅ dj-database-url instaliran
- [x] ✅ psycopg2-binary instaliran (PostgreSQL driver)
- [x] ✅ gunicorn instaliran
- [x] ✅ .env.production.example kreiran
- [x] ✅ Frontend API konfigurisan za environment variables
- [x] ✅ .env.example fajlovi kreirani za frontend

## Railway.app Setup (Backend)

- [ ] Kreiran nalog na Railway.app
- [ ] GitHub repo povezan
- [ ] Novi projekat kreiran
- [ ] Root directory postavljen na `backend`
- [ ] PostgreSQL baza dodata
- [ ] Environment varijable postavljene:
  - [ ] SECRET_KEY (generiši novi!)
  - [ ] DEBUG=False
  - [ ] ALLOWED_HOSTS
  - [ ] CORS_ALLOWED_ORIGINS
  - [ ] EMAIL_HOST_USER
  - [ ] EMAIL_HOST_PASSWORD
  - [ ] EMAIL_HOST
  - [ ] EMAIL_PORT
  - [ ] EMAIL_USE_TLS
  - [ ] DEFAULT_FROM_EMAIL
  - [ ] OWNER_EMAILS
  - [ ] CONTACT_EMAIL_RECIPIENT
- [ ] Deploy uspešan
- [ ] Migrations izvršeni
- [ ] Superuser kreiran

## Frontend Deployment (Vercel/Netlify)

- [ ] Nalog kreiran
- [ ] Repo povezan
- [ ] Root directory postavljen na `frontend`
- [ ] Build command: `npm run build`
- [ ] Output directory: `dist` (za Netlify)
- [ ] Environment varijabla dodata:
  - [ ] VITE_API_BASE_URL=https://tvoj-backend.railway.app/api
- [ ] Deploy uspešan

## Cloudinary Setup (Za slike)

- [ ] Cloudinary nalog kreiran
- [ ] Cloud Name, API Key, API Secret kopirani
- [ ] Environment varijable dodate na Railway:
  - [ ] CLOUDINARY_CLOUD_NAME
  - [ ] CLOUDINARY_API_KEY
  - [ ] CLOUDINARY_API_SECRET
- [ ] django-cloudinary-storage instaliran (opciono za sada)
- [ ] settings.py uncommented Cloudinary sekcija (opciono za sada)

## Email Setup (Gmail)

- [ ] Gmail App Password generisan
  - Idi na: https://myaccount.google.com/apppasswords
  - Generiši novi App Password
  - Kopiraj i dodaj u EMAIL_HOST_PASSWORD
- [ ] Email testiran

## Post-Deployment Testiranje

- [ ] Backend URL radi (https://tvoj-backend.railway.app)
- [ ] Frontend URL radi (https://tvoj-frontend.vercel.app)
- [ ] Admin panel dostupan (/admin)
- [ ] Prijava radi
- [ ] Proizvodi se prikazuju
- [ ] Kategorije rade
- [ ] Kontakt forma šalje poruke
- [ ] Emailovi stižu
- [ ] Kreiranje narudžbine radi
- [ ] Admin panel za narudžbine radi
- [ ] Kontakt poruke u admin panelu rade

## Komande za Reference

### Generisanje SECRET_KEY:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Lokalni test production build (Frontend):
```bash
cd frontend
npm run build
npm run preview
```

### Provera requirements.txt:
```bash
cd backend
pipenv requirements
```

## Troubleshooting Brzih Problema

### Backend ne startuje:
1. Proveri logove na Railway
2. Proveri da li su sve env varijable postavljene
3. Proveri DATABASE_URL

### Frontend ne vidi backend:
1. Proveri VITE_API_BASE_URL
2. Proveri CORS_ALLOWED_ORIGINS na backend-u
3. Proveri da backend URL ima HTTPS://

### Slike ne rade:
1. Za sada koristi lokalne slike
2. Cloudinary setup kasnije ako treba

## Sledeći Koraci Posle Deploya

1. **Testiranje sa klijentom** - Podeli URL-ove
2. **Dodaj custom domain** (ako treba)
3. **SSL/HTTPS** - Automatski na Railway/Vercel/Netlify
4. **Monitoring** - Prati logove i greške
5. **Backup baze** - Railway automatski backup-uje

---

## 🎉 Kada sve radi:

Aplikacija je spremna za testiranje od strane klijenta!
Podeli URL-ove i prati feedback.
