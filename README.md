# DIGIBIZ Python MVP

Verified business-growth talent marketplace MVP built in Python/Flask.

## Included
- Business owner registration/login
- Professional & agency registration/login
- Admin login
- Digital marketing, creative, web, promoter, influencer, CA/professional-service and agency roles
- Business requirements
- Expert matching
- Contact requests
- Assessments and admin verification
- DIGIBIZ scoring and verification statuses

## Local run
```bash
python -m venv .venv
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000/setup` once, then use the app.

Prototype admin: `admin@digibiz.in` / `admin123`

## Vercel
This repository includes `vercel.json`. The current SQLite `/tmp` database is suitable only for a prototype on serverless hosting. Replace it with managed PostgreSQL before real public use.
