#!/usr/bin/env python3
"""
Generate a polished presentation version of the Genesys <-> watsonx Orchestrate
interface diagram with Google's Nano Banana Pro image model, using the
vector-rendered image as the reference so labels stay faithful.

Requires:  GEMINI_API_KEY in the environment (never paste it into chat).
Optional:  GEMINI_IMAGE_MODEL (default gemini-3-pro-image-preview, i.e. Nano Banana Pro;
           set to the newer model id if your account has "Nano Banana Pro 2").

Usage:
  python3 nano_banana_generate.py genesys-wxo-interface-v0.2.jpg out-nano-banana.png
"""
import base64, json, os, sys, urllib.request

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    sys.exit("GEMINI_API_KEY is not set in this environment.")

MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-3-pro-image-preview")
ref_img, out_png = sys.argv[1], sys.argv[2]
mime = "image/jpeg" if ref_img.lower().endswith((".jpg", ".jpeg")) else "image/png"

PROMPT = """You are producing a clean, professional enterprise architecture diagram for Riyadh Air.
Redraw the attached reference diagram as a polished 16:9 presentation slide. Keep EVERY label,
box name, arrow direction, initiator dot, colour assignment and table row EXACTLY as in the
reference; do not invent, drop, paraphrase or reorder any text. Improve only layout spacing,
alignment, typography and visual hierarchy.

Content that must appear verbatim:
- Title: "Riyadh Air Concierge · Genesys Cloud CX ⇄ IBM watsonx Orchestrate (SaaS) · Interface Design v0.2"
- Four zones: "Genesys Cloud CX · RX org · AWS Frankfurt" (green), "RX Edge (Akamai WAF + App Gateway)" (purple),
  "IBM watsonx Orchestrate · SaaS on AWS" (yellow), "RX Concierge Gateway (RX AWS)" (blue).
- Five colour-coded use cases: UC1 voice (purple), UC2 social (green), UC3 web/mobile (blue),
  UC4 agent assist (orange), UC5 callback (grey). A filled dot marks the connection initiator on each arrow.
- Genesys-initiated interfaces: Audio Connector (wss, X-API-KEY + HMAC), Bot Connector (HTTPS POST postUtterance,
  verification token), AudioHook Monitor (wss, API key + secret).
- WXO-initiated interfaces: Notifications API (wss) + Conversations/Knowledge/Callback APIs (HTTPS, OAuth client credentials).
- Session-variable contract: IN Channel, GUEST_MOBILE_NO, GUEST_MOBILE_NO_COUNTRY_CODE, RX_CALLED_NO,
  RX_CALLED_NO_COUNTRY_CODE, GENESYS_CONVERSATION_ID; OUT VA_INTENT, GUEST_TIER, CONVERSATION_LANGUAGE,
  GUEST_VERIFIED, VA_SESSION_ID, VA_CONVERSATION_SUMMARY.
- Web Messaging customAttributes: GUEST_ID, LANGUAGE, ORDER_ID, LAST_Name, VA_SESSION_ID, VA_CONVERSATION_SUMMARY,
  with two deploymentIds (Web, Mobile).
- The ten-row interface contract table and the Legend.
Style: flat vector look, white background, thin rounded boxes, legible sans-serif text at small sizes,
no 3D, no photos, no decorative icons beyond simple phone/chat/agent glyphs."""

with open(ref_img, "rb") as f:
    ref_b64 = base64.b64encode(f.read()).decode()

body = {
    "contents": [{
        "role": "user",
        "parts": [
            {"text": PROMPT},
            {"inline_data": {"mime_type": mime, "data": ref_b64}},
        ],
    }],
    "generationConfig": {
        "responseModalities": ["IMAGE", "TEXT"],
        "imageConfig": {"aspectRatio": "16:9", "imageSize": "4K"},
    },
}

req = urllib.request.Request(
    f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
    data=json.dumps(body).encode(),
    headers={"Content-Type": "application/json", "x-goog-api-key": API_KEY},
)
with urllib.request.urlopen(req, timeout=300) as resp:
    data = json.load(resp)

parts = data["candidates"][0]["content"]["parts"]
img = next((p for p in parts if "inlineData" in p or "inline_data" in p), None)
if not img:
    sys.exit("No image returned: " + json.dumps(data)[:2000])
blob = (img.get("inlineData") or img.get("inline_data"))["data"]
with open(out_png, "wb") as f:
    f.write(base64.b64decode(blob))
print("wrote", out_png)
for p in parts:
    if "text" in p:
        print("model note:", p["text"][:500])
