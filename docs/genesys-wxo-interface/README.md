# Genesys Cloud CX to watsonx Orchestrate (SaaS) interface design v0.2

Corrected replacement for the v0.1 "GeneSys / WXO SaaS Interface" Miro sketch, prepared 30 Sep 2026
for the "Genesys Concierge Design Documents" thread (Veda, Nithya, TPI/IST).

Files:

- `genesys-wxo-interface-v0.2.html` - editable source (absolute-positioned boxes plus SVG arrows).
- `genesys-wxo-interface-v0.2.png` - 2620 x 2010 render, the version to circulate.
- `genesys-wxo-interface-v0.2.jpg` - lighter reference for the image model.
- `render.js` - re-renders the HTML with Chromium: `NODE_PATH=$(npm root -g) node render.js <in.html> <out.png>`.
- `nano_banana_generate.py` - Gemini image generation using the render as reference; needs `GEMINI_API_KEY`.

Sources: TPI PI3 LLD (May 2025), TPI Genesys CCaaS HLD v3 sections 16.3 and 17.4.7 (Sep 2025),
Watson-RX Integration Governance v1.0 (May 2026), IST/RX design-documents email thread (20-27 Sep 2026).

Draft for review, not an approved design.
