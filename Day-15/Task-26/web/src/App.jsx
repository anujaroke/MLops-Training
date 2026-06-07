import { useMemo, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const starterPrompts = [
  "Summarize our remote work policy",
  "What is the expense approval process?",
  "Give me the onboarding checklist",
  "What did we plan for Q2?",
];

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hey, I am OrgMind. Ask me anything about company policies, notes, or plans.",
      sources: [],
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const timestamp = useMemo(() => {
    const now = new Date();
    return now.toLocaleString(undefined, {
      weekday: "short",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  }, []);

  const sendMessage = async (text) => {
    const question = text.trim();
    if (!question || loading) {
      return;
    }

    setMessages((prev) => [...prev, { role: "user", content: question }]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Request failed");
      }

      const data = await response.json();
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources || [],
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `Oops. ${error.message}. Try again in a moment.`,
          sources: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    sendMessage(input);
  };

  return (
    <div className="page">
      <div className="grain" />
      <header className="topbar">
        <div className="logo">OrgMind</div>
        <div className="pulse">
          <span className="dot" />
          <span>Live</span>
        </div>
      </header>

      <section className="hero">
        <div>
          <p className="eyebrow">Warm studio notes</p>
          <h1>
            Company knowledge, 
            <span>collected with care.</span>
          </h1>
          <p className="lead">
            Ask OrgMind for policies, notes, and the truth hidden in your text files.
          </p>
        </div>
        <div className="stat-card">
          <p className="stat-title">Session</p>
          <p className="stat-value">{timestamp}</p>
          <p className="stat-meta">RAG + Groq + Llama3</p>
        </div>
      </section>

      <section className="chat">
        <div className="messages">
          {messages.map((message, index) => (
            <div
              key={`${message.role}-${index}`}
              className={`bubble ${message.role}`}
            >
              <p>{message.content}</p>
              {message.sources && message.sources.length > 0 ? (
                <div className="sources">
                  <span>Sources</span>
                  <div className="source-list">
                    {message.sources.map((source) => (
                      <span key={source} className="chip">
                        {source}
                      </span>
                    ))}
                  </div>
                </div>
              ) : null}
            </div>
          ))}
          {loading ? (
            <div className="bubble assistant typing">
              <p>Thinking in warm tones...</p>
            </div>
          ) : null}
        </div>

        <form className="composer" onSubmit={handleSubmit}>
          <input
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Ask about a policy, meeting note, or process"
            aria-label="Ask OrgMind"
          />
          <button type="submit" disabled={loading}>
            {loading ? "..." : "Send"}
          </button>
        </form>
      </section>

      <section className="prompts">
        {starterPrompts.map((prompt) => (
          <button
            key={prompt}
            className="prompt"
            onClick={() => sendMessage(prompt)}
            type="button"
          >
            {prompt}
          </button>
        ))}
      </section>
    </div>
  );
}
