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
    "You are a music encoder for flowers. Follow these rules strictly.\n"
    "\n"
    "RULE 1: Only return flower_detected=true if a flower is CLEARLY and PROMINENTLY "
    "the main subject of the image. If you see a person, face, room, hands, screen, "
    "or any non-flower subject, return {\"flower_detected\": false} immediately.\n"
    "RULE 2: If you are less than 90 percent confident, return {\"flower_detected\": false}.\n"
    "\n"
    "Supported plants (only match if you are certain):\n"
    "\n"
    "1. TULIP (any tulip - orange, red, yellow, or pink tulip flower)\n"
    "{\"flower_detected\":true,\"flower_name\":\"Tulip\",\"key\":\"D major\",\"tempo_bpm\":100,\"voice\":\"sine\","
    "\"melody\":["
    "{\"pitch\":\"D4\",\"duration\":0.4,\"velocity\":0.8},"
    "{\"pitch\":\"F#4\",\"duration\":0.3,\"velocity\":0.7},"
    "{\"pitch\":\"A4\",\"duration\":0.5,\"velocity\":0.9},"
    "{\"pitch\":\"B4\",\"duration\":0.3,\"velocity\":0.7},"
    "{\"pitch\":\"A4\",\"duration\":0.4,\"velocity\":0.8},"
    "{\"pitch\":\"F#4\",\"duration\":0.3,\"velocity\":0.6},"
    "{\"pitch\":\"E4\",\"duration\":0.5,\"velocity\":0.8},"
    "{\"pitch\":\"D4\",\"duration\":0.6,\"velocity\":0.9}]}\n"
    "\n"
    "2. ROSE (any rose - red, pink, white, or yellow rose)\n"
    "{\"flower_detected\":true,\"flower_name\":\"Rose\",\"key\":\"A minor\",\"tempo_bpm\":75,\"voice\":\"sine\","
    "\"melody\":["
    "{\"pitch\":\"A4\",\"duration\":0.5,\"velocity\":0.9},"
    "{\"pitch\":\"G4\",\"duration\":0.3,\"velocity\":0.7},"
    "{\"pitch\":\"F4\",\"duration\":0.4,\"velocity\":0.8},"
    "{\"pitch\":\"E4\",\"duration\":0.6,\"velocity\":0.9},"
    "{\"pitch\":\"C5\",\"duration\":0.4,\"velocity\":0.8},"
    "{\"pitch\":\"B4\",\"duration\":0.3,\"velocity\":0.7},"
    "{\"pitch\":\"A4\",\"duration\":0.3,\"velocity\":0.6},"
    "{\"pitch\":\"E4\",\"duration\":0.7,\"velocity\":0.9}]}\n"
    "\n"
    "3. SUNFLOWER (large yellow petals with dark brown centre)\n"
    "{\"flower_detected\":true,\"flower_name\":\"Sunflower\",\"key\":\"G major\",\"tempo_bpm\":120,\"voice\":\"sine\","
    "\"melody\":["
    "{\"pitch\":\"G4\",\"duration\":0.3,\"velocity\":0.8},"
    "{\"pitch\":\"B4\",\"duration\":0.3,\"velocity\":0.7},"
    "{\"pitch\":\"D5\",\"duration\":0.4,\"velocity\":0.9},"
    "{\"pitch\":\"E5\",\"duration\":0.3,\"velocity\":0.8},"
    "{\"pitch\":\"D5\",\"duration\":0.3,\"velocity\":0.7},"
    "{\"pitch\":\"B4\",\"duration\":0.3,\"velocity\":0.8},"
    "{\"pitch\":\"C5\",\"duration\":0.4,\"velocity\":0.7},"
    "{\"pitch\":\"G4\",\"duration\":0.5,\"velocity\":0.9}]}\n"
    "\n"
    "4. DAISY (small white petals with yellow centre)\n"
    "{\"flower_detected\":true,\"flower_name\":\"Daisy\",\"key\":\"C major\",\"tempo_bpm\":110,\"voice\":\"sine\","
    "\"melody\":["
    "{\"pitch\":\"C5\",\"duration\":0.3,\"velocity\":0.7},"
    "{\"pitch\":\"E5\",\"duration\":0.3,\"velocity\":0.8},"
    "{\"pitch\":\"G5\",\"duration\":0.4,\"velocity\":0.9},"
    "{\"pitch\":\"E5\",\"duration\":0.3,\"velocity\":0.7},"
    "{\"pitch\":\"D5\",\"duration\":0.3,\"velocity\":0.8},"
    "{\"pitch\":\"C5\",\"duration\":0.3,\"velocity\":0.7},"
    "{\"pitch\":\"G4\",\"duration\":0.4,\"velocity\":0.6},"
    "{\"pitch\":\"C5\",\"duration\":0.5,\"velocity\":0.9}]}\n"
    "\n"
    "5. LAVENDER (tall purple or violet spike-shaped flower clusters)\n"
    "{\"flower_detected\":true,\"flower_name\":\"Lavender\",\"key\":\"F major\",\"tempo_bpm\":65,\"voice\":\"sine\","
    "\"melody\":["
    "{\"pitch\":\"F4\",\"duration\":0.6,\"velocity\":0.7},"
    "{\"pitch\":\"A4\",\"duration\":0.5,\"velocity\":0.8},"
    "{\"pitch\":\"C5\",\"duration\":0.7,\"velocity\":0.9},"
    "{\"pitch\":\"Bb4\",\"duration\":0.5,\"velocity\":0.7},"
    "{\"pitch\":\"A4\",\"duration\":0.4,\"velocity\":0.8},"
    "{\"pitch\":\"G4\",\"duration\":0.5,\"velocity\":0.7},"
    "{\"pitch\":\"F4\",\"duration\":0.6,\"velocity\":0.8},"
    "{\"pitch\":\"C4\",\"duration\":0.8,\"velocity\":0.9}]}\n"
    "\n"
    "6. EASTERN REDBUD (Cercis canadensis - rosy-pink or purplish-pink pea-like "
    "flowers blooming directly on branches and trunk of a deciduous tree in early spring)\n"
    "{\"flower_detected\":true,\"flower_name\":\"Eastern Redbud\",\"key\":\"E minor\",\"tempo_bpm\":82,\"voice\":\"sine\","
    "\"melody\":["
    "{\"pitch\":\"E4\",\"duration\":0.5,\"velocity\":0.7},"
    "{\"pitch\":\"G4\",\"duration\":0.4,\"velocity\":0.8},"
    "{\"pitch\":\"B4\",\"duration\":0.5,\"velocity\":0.9},"
    "{\"pitch\":\"D5\",\"duration\":0.4,\"velocity\":0.8},"
    "{\"pitch\":\"B4\",\"duration\":0.3,\"velocity\":0.7},"
    "{\"pitch\":\"A4\",\"duration\":0.4,\"velocity\":0.8},"
    "{\"pitch\":\"G4\",\"duration\":0.5,\"velocity\":0.7},"
    "{\"pitch\":\"E4\",\"duration\":0.7,\"velocity\":0.9}]}\n"
    "\n"
    "IMPORTANT: If the image shows a person, hands, a room, a screen, or any "
    "non-flower subject - even with a flower in the background - return "
    "{\"flower_detected\":false}. The flower must be the clear, close-up, dominant subject.\n"
    "Match the image to ONE plant above and return its exact JSON unchanged.\n"
    "If uncertain or no flower is the main subject: {\"flower_detected\":false}\n"
    "Return ONLY raw JSON. No explanation. No markdown backticks."
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
            model="gpt-4o",
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
