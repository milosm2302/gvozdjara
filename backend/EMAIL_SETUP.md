# Email Konfiguracija za Django

Ovaj dokument objašnjava kako konfigurisati email funkcionalnost za kontakt formu.

## Opcije za slanje email-ova

### 1. Gmail (najpopularnije za testiranje i male aplikacije)

U `backend/settings.py` dodaj:

```python
# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'vas.email@gmail.com'  # Tvoj Gmail
EMAIL_HOST_PASSWORD = 'app_password'      # App password (ne obična lozinka!)
DEFAULT_FROM_EMAIL = 'vas.email@gmail.com'
```

**VAŽNO za Gmail:**
1. Moraš kreirati "App Password" (ne možeš koristiti običnu lozinku)
2. Idi na: https://myaccount.google.com/apppasswords
3. Generiši novi app password za "Mail"
4. Koristi taj 16-karakterni password u `EMAIL_HOST_PASSWORD`

### 2. Office 365 / Outlook (za poslovne email-ove)

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'office@betapack.co.rs'
EMAIL_HOST_PASSWORD = 'vasa_lozinka'
DEFAULT_FROM_EMAIL = 'office@betapack.co.rs'
```

### 3. SMTP2GO ili SendGrid (za production)

Za veće volume email-ova, preporučujem servise kao što su:
- SMTP2GO (besplatno do 1000 emailova/mesec)
- SendGrid (besplatno do 100 emailova/dan)
- Mailgun

## Bezbedno čuvanje kredencijala

**NIKAD nemoj čuvati lozinke direktno u settings.py!**

Koristi `.env` fajl:

1. Instaliraj: `pipenv install python-decouple`

2. Kreiraj `.env` fajl u `backend/` folderu:
```
EMAIL_HOST_USER=vas.email@gmail.com
EMAIL_HOST_PASSWORD=app_password
```

3. U `settings.py`:
```python
from decouple import config

EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
```

4. Dodaj `.env` u `.gitignore`!

## Testiranje

Za testiranje bez pravog email-a, možeš koristiti:

```python
# Console backend (ispisuje email u terminal)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## Primer korišćenja

```python
from django.core.mail import send_mail

send_mail(
    subject='Nova kontakt poruka',
    message='Poruka od korisnika...',
    from_email='office@betapack.co.rs',
    recipient_list=['office@betapack.co.rs'],
    fail_silently=False,
)
```
