from flask import Flask, request, jsonify, render_template
from formatter import format_resume

app = Flask(__name__, template_folder="../frontend")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate_resume", methods=["POST"])
def generate_resume():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data received"}), 400

    resume_text = format_resume(data)

    return jsonify({
        "success": True,
        "resume_text": resume_text
    })

if __name__ == "__main__":
    app.run(debug=True)