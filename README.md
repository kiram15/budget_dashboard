# Budget Dashboard

Local budgeting and investment tracking with a Django backend and React/Vite
frontend.

## Local setup

```bash
git clone https://github.com/kiram15/budget_dashboard.git
cd budget_dashboard

python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```bash
pip install Django django-environ djangorestframework plaid-python keyring yfinance
```

Create a `.env` file in the repository root. Do not commit it. It must contain
at least:

```dotenv
DJANGO_SECRET_KEY=replace-with-a-local-secret
DJANGO_DEBUG=True
PLAID_CLIENT_ID=your-plaid-client-id
PLAID_SECRET=your-plaid-secret
PLAID_ENV=sandbox
PLAID_REDIRECT_URI=
```

Apply migrations and start the backend:

```bash
python manage.py migrate
python manage.py runserver
```

In a second terminal, start the frontend:

```bash
cd frontend
npm install
npm run dev
```

When finished, deactivate the Python environment:

```bash
deactivate
```
