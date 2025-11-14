# ChargeCast Backend

A Django REST API for retrieving UK carbon intensity data to help users optimize EV charging times based on grid carbon emissions.

## Features

- Fetch current and historical carbon intensity data for the UK
- Get carbon intensity forecasts
- RESTful API endpoints for integration with frontend applications

## Setup

### Prerequisites

- Python 3.12+
- PostgreSQL
- Virtual environment tool (venv)

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd chargecast-backend
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start development server:
```bash
python manage.py runserver
```

## Environment Variables

See `.env.example` for required environment variables:

- `DEBUG`: Set to `True` for development, `False` for production
- `SECRET_KEY`: Django secret key (generate a secure one for production)
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: PostgreSQL database configuration
- `CARBON_INTENSITY_BASE_URL`: Carbon Intensity API base URL
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

## API Endpoints

(Document your endpoints here)

## Deployment

This project is configured for deployment on Render.com. See deployment instructions in your Render dashboard.

## License

(Add your license here)
