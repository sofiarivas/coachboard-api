# Coachboard API

A lightweight FastAPI backend for swimming workout coaching platform.

## Setup

1. Clone the repo
2. Create `.env` from `.env.example`
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `uvicorn app.main:app --reload`

## API Endpoints

### Auth
- `POST /auth/coach/register` - Register coach
- `POST /auth/coach/login` - Login coach
- `POST /auth/trainee/register` - Register trainee
- `POST /auth/trainee/login` - Login trainee

### Coaches
- `GET /coaches` - List all coaches
- `GET /coaches/{id}` - Get coach details

### Boards
- `GET /boards` - List public boards
- `GET /boards/{id}` - Get board details
- `POST /boards` - Create board (coach auth)

### Subscriptions
- `POST /boards/{id}/subscribe` - Subscribe to board (trainee auth)
- `DELETE /boards/{id}/subscribe` - Unsubscribe (trainee auth)
- `GET /me/boards` - Get my boards (trainee auth)

### Workouts
- `GET /workouts/{id}` - Get workout
- `GET /today` - Get today's workouts (trainee auth)
- `GET /upcoming` - Get upcoming workouts (trainee auth)
- `POST /boards/{id}/workouts` - Create workout (coach auth)
