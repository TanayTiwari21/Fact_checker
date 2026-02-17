# Fact Checker Backend

Flask REST API for the Fact Checker application.

## Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

4. Add your API keys to `.env`:
```
GEMINI_API_KEY=your_gemini_key_here
TAVILY_API_KEY=your_tavily_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here
```

## Run

```bash
python app.py
```

Server runs on `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /api/health
```

Response:
```json
{
  "status": "ok"
}
```

### Fact Check
```
POST /api/fact-check
Content-Type: application/json

{
  "claim": "Your claim here"
}
```

Response:
```json
{
  "claim": "Your claim here",
  "verdict": "TRUE | FALSE | PARTIALLY TRUE",
  "explanation": "Detailed explanation...",
  "sources": [
    {
      "url": "https://...",
      "title": "Source title"
    }
  ]
}
```

### Get History
```
GET /api/history
```

Response:
```json
{
  "history": [
    {
      "id": 1,
      "claim": "...",
      "verdict": "...",
      "explanation": "...",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

## Dependencies

- **Flask**: Web framework
- **Flask-CORS**: Handle cross-origin requests
- **google-genai**: Google Gemini API client (new unified SDK)
- **tavily-python**: Tavily search API client
- **supabase**: Supabase database client
- **python-dotenv**: Environment variable management

## How It Works

1. Receives claim from frontend
2. Searches web using Tavily (top 3 results)
3. Sends claim + search context to Google Gemini
4. Gemini analyzes and returns verdict + explanation
5. Saves to Supabase database
6. Returns result to frontend