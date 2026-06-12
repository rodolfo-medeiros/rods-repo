from __future__ import annotations

from datetime import datetime
from urllib.parse import quote_plus
import os
from pathlib import Path

from flask import Flask, redirect, render_template, request


app = Flask(__name__)


def build_whatsapp_url(name: str, company: str, email: str, goal: str) -> str:
	phone = os.getenv("TOKEN_WHATSAPP_NUMBER", "5511999999999")
	message = (
		f"Oi! Sou {name or 'um contato interessado'} da empresa {company or '—'}. "
		f"Quero conversar sobre branding para {goal or 'crescimento de marca'}. "
		f"Meu e-mail é {email or '—'}."
	)
	return f"https://wa.me/{phone}?text={quote_plus(message)}"


@app.get("/")
def home() -> str:
	year = datetime.now().year
	slides_dir = Path(app.static_folder or "static") / "img" / "pdf-pages"
	slide_files = sorted(slides_dir.glob("page-*.jpg"))
	slides = [f"img/pdf-pages/{item.name}" for item in slide_files]
	return render_template("index.html", year=year, slides=slides)


@app.post("/briefing")
def briefing() -> object:
	whatsapp_url = build_whatsapp_url(
		name=request.form.get("name", "").strip(),
		company=request.form.get("company", "").strip(),
		email=request.form.get("email", "").strip(),
		goal=request.form.get("goal", "").strip(),
	)
	return redirect(whatsapp_url)


@app.get("/contato")
def contato() -> object:
	return redirect(build_whatsapp_url("", "", "", ""))


if __name__ == "__main__":
	app.run(debug=True)
