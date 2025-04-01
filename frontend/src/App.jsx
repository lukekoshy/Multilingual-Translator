import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

function App() {
  const [inputText, setInputText] = useState("");
  const [translatedText, setTranslatedText] = useState("");
  const [targetLanguage, setTargetLanguage] = useState("es");
  const [service, setService] = useState("google");
  const [languages, setLanguages] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isLoadingLanguages, setIsLoadingLanguages] = useState(true);

  useEffect(() => {
    fetchLanguages();
  }, []);

  const fetchLanguages = async () => {
    try {
      setIsLoadingLanguages(true);
      const response = await axios.get(`${API_URL}/languages`);
      setLanguages(response.data.languages || {});
    } catch (err) {
      setError("Failed to fetch supported languages");
      console.error("Error fetching languages:", err);
    } finally {
      setIsLoadingLanguages(false);
    }
  };

  const handleTranslate = async () => {
    if (!inputText.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_URL}/translate`, {
        text: inputText,
        target_lang: targetLanguage,
        service,
      });

      setTranslatedText(response.data.translated_text);
    } catch (err) {
      setError(err.response?.data?.error || "Translation failed");
      console.error("Translation error:", err);
    } finally {
      setLoading(false);
    }
  };

  if (isLoadingLanguages) {
    return <div className="container">Loading supported languages...</div>;
  }

  return (
    <div className="container">
      <h1>Multilingual Translator</h1>

      <div className="controls">
        <select
          value={targetLanguage}
          onChange={(e) => setTargetLanguage(e.target.value)}
          className="language-select"
        >
          {Object.entries(languages).map(([code, name]) => (
            <option key={code} value={code}>
              {name}
            </option>
          ))}
        </select>

        <select
          value={service}
          onChange={(e) => setService(e.target.value)}
          className="service-select"
        >
          <option value="google">Google Translate</option>
          <option value="openai">OpenAI GPT</option>
        </select>
      </div>

      <div className="translation-area">
        <div className="input-area">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Enter text to translate..."
            rows={5}
          />
        </div>

        <button
          onClick={handleTranslate}
          disabled={loading || !inputText.trim()}
          className="translate-button"
        >
          {loading ? "Translating..." : "Translate"}
        </button>

        <div className="output-area">
          <textarea
            value={translatedText}
            readOnly
            placeholder="Translation will appear here..."
            rows={5}
          />
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}
    </div>
  );
}

export default App;
