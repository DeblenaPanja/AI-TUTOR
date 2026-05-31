from flask import Flask, request, jsonify, render_template_string
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Tutor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
         .container {
            background: white;
            width: 500px;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }

        h1 {
            text-align: center;
        }

        textarea {
            width: 100%;
            height: 100px;
            padding: 10px;
            font-size: 16px;
            margin-top: 10px;
        }
         button {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background: #45a049;
        }

        #answer {
            margin-top: 20px;
            padding: 10px;
            background: #eee;
            border-radius: 5px;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
<div class="container">
        <h1>AI Tutor</h1>
        <textarea id="question" placeholder="Ask any question..."></textarea>
        <button onclick="askQuestion()">Ask</button>
        <div id="answer">Answer will appear here...</div>
    </div>

    <script>
        async function askQuestion() {
            const question = document.getElementById("question").value;
            const answerBox = document.getElementById("answer");

            if (!question.trim()) {
                answerBox.innerText = "Please enter a question.";
                return;
            }

            answerBox.innerText = "Thinking...";

            const response = await fetch("/ask", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ question: question })
            });
             const data = await response.json();
            answerBox.innerText = data.answer || data.error;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({"error": "Please provide a question"}), 400

    question = data["question"]
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI Tutor. Explain clearly and step by step."
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        answer = response.choices[0].message.content
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)