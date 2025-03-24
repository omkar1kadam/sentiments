
from flask import Flask, request

import google.generativeai as genai

# Configure API
API_KEY = "AIzaSyB2yxeiFcUsEp2dZoekeRka5hX4FHI4C2U"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

app = Flask(__name__)

def analyze_sentiment(comment):
    """Sends a comment to Gemini API for sentiment analysis."""
    if not comment.strip():
        return "No comment provided."

    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"You are an expert in sentiment analysis. Explain your reasoning.\nComment: {comment}"
    
    response = model.generate_content(prompt)
    return response.text if response else "Error analyzing sentiment."

@app.route("/", methods=["GET", "POST"])
def index():
    sentiment = None
    comment = ""

    if request.method == "POST":
        comment = request.form.get("comment", "").strip()
        if comment:
            sentiment = analyze_sentiment(comment)
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sentiment Analysis</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; margin: 40px; }}
            .container {{ max-width: 500px; margin: auto; }}
            textarea {{ width: 100%; height: 80px; margin-bottom: 10px; }}
            button {{ padding: 10px 20px; margin-top: 10px; }}
            .result-box {{ border: 1px solid #ddd; padding: 15px; margin-top: 20px; background: #f9f9f9; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Sentiment Analysis</h2>
            <form method="POST">
                <textarea name="comment" placeholder="Enter your comment here..." required>{comment}</textarea><br>
                <button type="submit">Analyze</button>
            </form>
            
            {f'<div class="result-box"><strong>Analysis:</strong> {sentiment}</div>' if sentiment else ""}
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
