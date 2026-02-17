from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from google import genai
from tavily import TavilyClient
from supabase import create_client, Client

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize APIs
gemini_client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
tavily_client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))
supabase: Client = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/fact-check', methods=['POST'])
def fact_check():
    try:
        data = request.json
        claim = data.get('claim')
        
        if not claim:
            return jsonify({'error': 'Claim is required'}), 400
        
        # Search for relevant information using Tavily
        search_results = tavily_client.search(
            query=claim,
            max_results=3
        )
        
        # Prepare context from search results
        context = "\n\n".join([
            f"Source: {result.get('title', 'Unknown')}\n{result.get('content', '')}"
            for result in search_results.get('results', [])
        ])
        
        # Use Gemini to analyze the claim
        prompt = f"""Analyze this claim and determine if it's true, false, or needs more context.

Claim: {claim}

Evidence from web search:
{context}

Provide a clear verdict (TRUE, FALSE, or PARTIALLY TRUE) and a brief explanation (2-3 sentences).
Format your response as:
VERDICT: [verdict]
EXPLANATION: [explanation]"""
        
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        result_text = response.text
        
        # Parse the response
        lines = result_text.split('\n')
        verdict = 'UNKNOWN'
        explanation = result_text
        
        for line in lines:
            if line.startswith('VERDICT:'):
                verdict = line.replace('VERDICT:', '').strip()
            elif line.startswith('EXPLANATION:'):
                explanation = line.replace('EXPLANATION:', '').strip()
        
        # Save to Supabase
        supabase.table('fact_checks').insert({
            'claim': claim,
            'verdict': verdict,
            'explanation': explanation,
            'sources': [r['url'] for r in search_results.get('results', [])]
        }).execute()
        
        return jsonify({
            'claim': claim,
            'verdict': verdict,
            'explanation': explanation,
            'sources': search_results.get('results', [])
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        response = supabase.table('fact_checks').select('*').order('created_at', desc=True).limit(10).execute()
        return jsonify({'history': response.data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', 5000)))