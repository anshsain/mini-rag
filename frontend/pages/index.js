import { useState } from "react";

export default function Home() {
  console.log("Backend URL:", process.env.NEXT_PUBLIC_BACKEND_URL);
  
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    setLoading(true);
    setAnswer("");

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/query`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question }),
        }
      );

      const data = await res.json();
      setAnswer(data.answer || "No answer returned");
    } catch (err) {
      setAnswer("Error contacting backend");
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "600px" }}>
      <h1>Mini RAG</h1>

      <textarea
        rows={4}
        style={{ width: "100%" }}
        placeholder="Ask a question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <br /><br />

      <button onClick={askQuestion} disabled={loading}>
        {loading ? "Thinking..." : "Ask"}
      </button>

      <br /><br />

      {answer && (
        <div>
          <strong>Answer:</strong>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}
