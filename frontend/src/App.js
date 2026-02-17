import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = 'http://localhost:5000/api';

function App() {
  const [claim, setClaim] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await axios.get(`${API_URL}/history`);
      setHistory(response.data.history || []);
    } catch (err) {
      console.error('Failed to fetch history:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!claim.trim()) return;

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/fact-check`, { claim });
      setResult(response.data);
      setClaim('');
      fetchHistory();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to check fact');
    } finally {
      setLoading(false);
    }
  };

  const getVerdictColor = (verdict) => {
    if (verdict.includes('TRUE') && !verdict.includes('PARTIALLY')) {
      return { bg: '#003300', color: '#00ff00', border: '#00aa00' };
    }
    if (verdict.includes('FALSE')) {
      return { bg: '#330000', color: '#ff4444', border: '#aa0000' };
    }
    return { bg: '#332200', color: '#ffaa00', border: '#aa7700' };
  };

  return (
    <div className="App">
    <div className="container">
      <h1>Fact Checker</h1>
      <p className="subtitle">AI-powered fact verification</p>

        <form onSubmit={handleSubmit} className="fact-form">
          <textarea
            value={claim}
            onChange={(e) => setClaim(e.target.value)}
            placeholder="Enter a claim to fact-check..."
            rows="4"
            disabled={loading}
          />
          <button type="submit" disabled={loading || !claim.trim()}>
            {loading ? (
              <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                <span className="spinner"></span>
                Analyzing...
              </span>
            ) : (
              'Check Fact'
            )}
          </button>
        </form>

        {error && (
          <div className="error-box">
            <strong>Error:</strong> {error}
          </div>
        )}

        {result && (
          <div className="result-box">
            <div 
              className="verdict" 
              style={{ 
                backgroundColor: getVerdictColor(result.verdict).bg,
                color: getVerdictColor(result.verdict).color,
                border: `1px solid ${getVerdictColor(result.verdict).border}`
              }}
            >
              {result.verdict}
            </div>
            <div className="explanation">
              <h3>Explanation</h3>
              <p>{result.explanation}</p>
            </div>
            {result.sources && result.sources.length > 0 && (
              <div className="sources">
                <h3>Sources</h3>
                <ul>
                  {result.sources.map((source, idx) => (
                    <li key={idx}>
                      <a href={source.url} target="_blank" rel="noopener noreferrer">
                        {source.title || source.url}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        <div className="history-section">
          <h2>Recent Checks</h2>
          {history.length > 0 ? (
            <div className="history-list">
              {history.map((item) => (
                <div key={item.id} className="history-item">
                  <div className="history-claim">{item.claim}</div>
                  <div 
                    className="history-verdict"
                    style={{ 
                      color: getVerdictColor(item.verdict).color,
                      backgroundColor: getVerdictColor(item.verdict).bg,
                      border: `1px solid ${getVerdictColor(item.verdict).border}`
                    }}
                  >
                    {item.verdict}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <p>No fact checks yet. Submit a claim above to get started.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;