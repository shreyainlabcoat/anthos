import os
import json
import re
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

_api_key = os.environ.get("OPENAI_API_KEY", "")
if not _api_key:
    raise RuntimeError("Set OPENAI_API_KEY environment variable before running.")
client = OpenAI(api_key=_api_key)

SYSTEM_PROMPT = (
    "You are a flower detector. Two flowers only. Strict rules:\n"
    "- Only return flower_detected=true if a flower is CLEARLY the main subject. "
    "Person/room/hands/screen = {\"flower_detected\":false}.\n"
    "- If less than 90% confident = {\"flower_detected\":false}.\n"
    "\n"
    "TULIP (orange, red, yellow, or pink tulip):\n"
    "{\"flower_detected\":true,\"flower_name\":\"Tulip\",\"key\":\"D major\",\"tempo_bpm\":132,\"voice\":\"sine\","
    "\"melody\":["
    "{\"pitch\":\"D5\",\"duration\":0.15,\"velocity\":0.9},"
    "{\"pitch\":\"F#5\",\"duration\":0.15,\"velocity\":0.8},"
    "{\"pitch\":\"A5\",\"duration\":0.2,\"velocity\":1.0},"
    "{\"pitch\":\"D5\",\"duration\":0.15,\"velocity\":0.8},"
    "{\"pitch\":\"B4\",\"duration\":0.15,\"velocity\":0.9},"
    "{\"pitch\":\"A4\",\"duration\":0.15,\"velocity\":0.7},"
    "{\"pitch\":\"F#4\",\"duration\":0.2,\"velocity\":0.9},"
    "{\"pitch\":\"D4\",\"duration\":0.25,\"velocity\":1.0}]}\n"
    "\n"
    "EASTERN REDBUD (Cercis canadensis - small rosy-pink or purplish-pink pea-like "
    "flowers blooming directly on bare branches/trunk of a tree, early spring):\n"
    "{\"flower_detected\":true,\"flower_name\":\"Eastern Redbud\",\"key\":\"B minor\",\"tempo_bpm\":52,\"voice\":\"sine\","
    "\"melody\":["
    "{\"pitch\":\"B3\",\"duration\":0.9,\"velocity\":0.6},"
    "{\"pitch\":\"D4\",\"duration\":0.8,\"velocity\":0.7},"
    "{\"pitch\":\"F#4\",\"duration\":1.0,\"velocity\":0.8},"
    "{\"pitch\":\"A4\",\"duration\":0.9,\"velocity\":0.9},"
    "{\"pitch\":\"G4\",\"duration\":0.8,\"velocity\":0.7},"
    "{\"pitch\":\"E4\",\"duration\":0.9,\"velocity\":0.8},"
    "{\"pitch\":\"D4\",\"duration\":0.8,\"velocity\":0.6},"
    "{\"pitch\":\"B3\",\"duration\":1.2,\"velocity\":0.9}]}\n"
    "\n"
    "Return the exact JSON for whichever flower is clearly visible. "
    "Anything else: {\"flower_detected\":false}\n"
    "Return ONLY raw JSON. No explanation. No markdown."
)


def clean_json_response(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(force=True)
    image_b64 = data.get("image_base64", "")

    if not image_b64:
        return jsonify({"flower_detected": False, "error": "No image provided"}), 400

    if not image_b64.startswith("data:"):
        image_b64 = "data:image/jpeg;base64," + image_b64

    raw = ""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=512,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": SYSTEM_PROMPT},
                        {"type": "image_url", "image_url": {"url": image_b64, "detail": "low"}},
                    ],
                }
            ],
        )
        raw = response.choices[0].message.content or ""
        cleaned = clean_json_response(raw)
        result = json.loads(cleaned)
        return jsonify(result)

    except json.JSONDecodeError as e:
        app.logger.warning("JSON parse error: %s | raw: %s", e, raw[:200])
        return jsonify({"flower_detected": False, "error": "parse_error"})
    except Exception as e:
        app.logger.error("OpenAI call failed: %s", e)
        return jsonify({"flower_detected": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
