import React, { useState } from "react";
import './Form.css'
import axios from "axios";

function Form() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState<string | null>(null);
  const [result_url, setResultUrl] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:5000/predict", {
        url,
      });
      setResult(response.data.prediction);
      setResultUrl(url)
    } 
    catch (error) {
      console.error("Error checking URL:", error);
      setResult("Error processing the URL, try adding http:// or https://");
    }
  };

  return (
    <div className="Layout">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter URL"
        />
        <button type="submit">Check URL</button>
      </form>

      <p>Last Checked URL: {result_url}</p>
      {result && (
        <div
          className={
            result === "Phishing" ? "Phishing" : "Safe"
          }
        >
          Result: {result}
        </div>
      )}
    </div>
  );
}

export default Form;
