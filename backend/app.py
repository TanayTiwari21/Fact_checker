from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from google import genai
from tavily import TavilyClient
from supabase import create_client, Client

# Load env
load_dotenv()

app = Flask(__name__)
CORS(app)

# ---- Lazy init helpers (prevents crash during boot) ----
def get_gemini():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_tavily():
    return TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def get_supabase():
    return create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )

# --------------------------------------------------------

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/fact-check", methods=["POST"])
def fact_check():
    try:
        data = request.get_json()
        claim = data.get("claim")

        if not claim:
            return jsonify({"error": "Claim is required"}), 400

        tavily_client = get_tavily()

        # Web search
        search_results = tavily_client.search(
            query=claim,
            max_results=3
        )

        context = "\n\n".join([
            f"Source: {result.get('title','Unknown')}\n{result.get('content','')}"
            for result in search_results.get("results", [])
        ])

        prompt = f"""
Analyze this claim and determine if it's true, false, or needs more context.

Claim: {claim}

Evidence:
{context}

Format:
VERDICT: TRUE/FALSE/PARTIALLY TRUE
EXPLANATION: short explanation
"""

        gemini_client = get_gemini()

        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        result_text = response.text

        verdict = "UNKNOWN"
        explanation = result_text

        for line in result_text.split("\n"):
            if line.startswith("VERDICT:"):
                verdict = line.replace("VERDICT:", "").strip()
            if line.startswith("EXPLANATION:"):
                explanation = line.replace("EXPLANATION:", "").strip()

        # Save history
        supabase = get_supabase()
        supabase.table("fact_checks").insert({
            "claim": claim,
            "verdict": verdict,
            "explanation": explanation,
            "sources": [r.get("url") for r in search_results.get("results", [])]
        }).execute()

        return jsonify({
            "claim": claim,
            "verdict": verdict,
            "explanation": explanation,
            "sources": search_results.get("results", [])
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/history", methods=["GET"])
def get_history():
    try:
        supabase = get_supabase()
        response = supabase.table("fact_checks") \
            .select("*") \
            .order("created_at", desc=True) \
            .limit(10) \
            .execute()

        return jsonify({"history": response.data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# IMPORTANT: no debug, correct port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
