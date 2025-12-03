# PCS Assistant 🚴

AI-powered cycling statistics assistant using ProCyclingStats data and Claude AI.

## Features

- **Natural Language Queries**: Ask questions about riders, races, and rankings in plain language
- **Real-time Data**: Live data from ProCyclingStats.com
- **Interactive Dashboard**: Rankings, statistics, and visualizations
- **Multi-language**: Supports Italian and English queries
- **WebSocket Updates**: Real-time ranking updates

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Claude AI** - Natural language processing (Anthropic)
- **procyclingstats** - Data scraping library
- **WebSockets** - Real-time updates

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Vite** - Build tool

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Anthropic API key

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run server
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The app will be available at http://localhost:5173

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check |
| `POST /api/chat/` | Send chat message |
| `GET /api/riders/{slug}` | Get rider profile |
| `GET /api/races/{slug}?year=2024` | Get race results |
| `GET /api/rankings/individual` | Get UCI rankings |
| `GET /api/teams/{slug}?year=2024` | Get team info |
| `WS /ws/live` | WebSocket for live updates |

## Example Queries

- "Quante vittorie ha Pogacar nel 2024?"
- "Chi ha vinto il Tour de France 2024?"
- "Confronta Vingegaard e Pogacar"
- "Mostra la classifica UCI"
- "Risultati della Milano-Sanremo"
- "Chi sono i corridori dell'UAE Team?"

## Deployment on Render

1. Push code to GitHub
2. Connect repo to Render
3. Render auto-detects `render.yaml`
4. Add `ANTHROPIC_API_KEY` in dashboard
5. Deploy!

**URLs after deployment:**
- Backend: https://pcs-assistant-api.onrender.com
- Frontend: https://pcs-assistant.onrender.com

## Project Structure

```
pcs-assistant/
├── backend/
│   ├── app/
│   │   ├── api/routes/     # API endpoints
│   │   ├── services/       # Business logic
│   │   ├── models/         # Pydantic models
│   │   └── main.py         # FastAPI app
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API client
│   │   └── pages/          # Page components
│   └── package.json
│
├── render.yaml             # Render deployment
└── README.md
```

## Environment Variables

### Backend
| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Claude API key | Yes |
| `ALLOWED_ORIGINS` | CORS origins | Yes |
| `DEBUG` | Debug mode | No |

### Frontend
| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | Backend API URL |
| `VITE_WS_URL` | WebSocket URL |

## License

MIT

## Credits

- Data from [ProCyclingStats](https://www.procyclingstats.com/)
- AI powered by [Anthropic Claude](https://www.anthropic.com/)
