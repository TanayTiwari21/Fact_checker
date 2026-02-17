# Fact Checker App

A minimal AI-powered fact checker that verifies claims using Google Gemini API and Tavily search. Built with React, Flask, and Supabase.

## DEPLOYED LIVE LINK
[Live link](https://fact-checker-4iby.vercel.app/)
## Tech Stack

### Frontend
- React 18
- Axios for API calls
- Plain CSS (no UI frameworks)

### Backend
- **Python 3.10+** (3.12 recommended)
- **Flask** (REST API)
- **Google Gemini API** (google-genai package)
- **Tavily Search API**
- **Supabase** (PostgreSQL database)

## Prerequisites

Before you begin, you need:

1. **Python 3.10+** installed (3.12 recommended for best compatibility)
2. **Node.js 16+** and npm installed
3. **Google Gemini API Key** - Get it from [Google AI Studio](https://makersuite.google.com/app/apikey)
4. **Tavily API Key** - Get it from [Tavily](https://tavily.com/)
5. **Supabase Account** - Sign up at [Supabase](https://supabase.com/)

## Supabase Setup

1. Create a new project on Supabase
2. Go to the SQL Editor and run this query to create the table:

```sql
CREATE TABLE fact_checks (
  id BIGSERIAL PRIMARY KEY,
  claim TEXT NOT NULL,
  verdict TEXT NOT NULL,
  explanation TEXT,
  sources TEXT[],
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

3. Get your project URL and anon key from Settings > API

## Installation

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

Edit the `.env` file and add your API keys:

```
GEMINI_API_KEY=your_actual_gemini_api_key
TAVILY_API_KEY=your_actual_tavily_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

## Running the App

### Start Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python app.py
```

The backend will run on `http://localhost:5000`

### Start Frontend (Terminal 2)

```bash
cd frontend
npm start
```

The frontend will run on `http://localhost:3000`

## Usage

1. Open `http://localhost:3000` in your browser
2. Enter a claim you want to fact-check
3. Click "Check Fact"
4. The app will:
   - Search for relevant information using Tavily
   - Analyze the claim with Google Gemini
   - Show the verdict (TRUE, FALSE, or PARTIALLY TRUE)
   - Display an explanation and sources
   - Save the result to Supabase
5. View your fact-check history below

## API Endpoints

### GET /api/health
Check if the API is running

### POST /api/fact-check
Check a fact claim

**Request Body:**
```json
{
  "claim": "The Earth is flat"
}
```

**Response:**
```json
{
  "claim": "The Earth is flat",
  "verdict": "FALSE",
  "explanation": "The Earth is round...",
  "sources": [...]
}
```

### GET /api/history
Get recent fact-check history (last 10)

## Project Structure

```
tanay/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example        # Environment variables template
│   └── .gitignore
├── frontend/
│   ├── public/
│   │   └── index.html      # HTML template
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   ├── App.css         # Styles
│   │   ├── index.js        # React entry point
│   │   └── index.css       # Global styles
│   ├── package.json        # Node dependencies
│   └── .gitignore
└── README.md
```

## How It Works

1. **User submits a claim** via the React frontend
2. **Frontend sends POST request** to Flask backend
3. **Backend searches the web** using Tavily API (gets top 3 results)
4. **Backend sends claim + search results** to Google Gemini for analysis
5. **Gemini analyzes** and returns verdict (TRUE/FALSE/PARTIALLY TRUE) with explanation
6. **Backend saves result** to Supabase PostgreSQL database
7. **Frontend displays** the verdict, explanation, and sources
8. **History is loaded** from Supabase and shown below

## Troubleshooting

### Backend issues:
- Make sure all API keys are correct in `.env`
- Check if virtual environment is activated
- Verify Python version: `python --version`

### Frontend issues:
- Delete `node_modules` and run `npm install` again
- Clear browser cache
- Check if backend is running on port 5000

### Database issues:
- Verify Supabase credentials are correct
- Make sure the table was created properly
- Check Supabase dashboard for errors

## Notes for Assessment

This project demonstrates:
- **Clean Code**: Minimal, well-organized, easy to understand
- **REST API Design**: Simple Flask endpoints
- **React Best Practices**: Functional components, hooks (useState, useEffect)
- **Database Integration**: Supabase (PostgreSQL) for persistent storage
- **External API Integration**: Google Gemini and Tavily
- **Error Handling**: Try-catch blocks and user feedback
- **Responsive Design**: Works on mobile and desktop

## License

MIT
