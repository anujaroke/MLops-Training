from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

from rag_core import RagEngine

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

engine = RagEngine()
startup_error = None
startup_done = False


@app.before_request
def startup():
    global startup_error, startup_done
    if startup_done:
        return

    startup_done = True
    load_dotenv()
    try:
        engine.build()
    except Exception as exc:
        startup_error = str(exc)


@app.get("/health")
def health():
    if startup_error:
        return jsonify({"status": "error", "detail": startup_error})
    return jsonify({"status": "ok"})


@app.post("/chat")
def chat():
    if startup_error:
        return jsonify({"detail": startup_error}), 500

    payload = request.get_json(silent=True) or {}
    question = str(payload.get("question", "")).strip()
    if not question:
        return jsonify({"detail": "Question cannot be empty"}), 400

    answer, sources = engine.answer(question)
    return jsonify({"answer": answer, "sources": sources})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
