
from flask import Flask, render_template, request, redirect, session
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = "browser_history_key"

@app.route("/", methods=["GET", "POST"])
def home():
    if "back" not in session:
        session["back"] = []
        session["forward"] = []
        session["current"] = ""

    if request.method == "POST":
        action = request.form.get("action")

        if action == "visit":
            url = request.form.get("url", "").strip()
            if url:
                if not url.startswith(("http://", "https://")):
                    url = "https://" + url
                parsed = urlparse(url)
                if parsed.netloc and "." in parsed.netloc:
                    if session["current"]:
                        back = session["back"]
                        back.append(session["current"])
                        session["back"] = back
                    session["current"] = url
                    session["forward"] = []

        elif action == "back" and session["back"]:
            forward = session["forward"]
            forward.append(session["current"])
            session["forward"] = forward
            back = session["back"]
            session["current"] = back.pop()
            session["back"] = back

        elif action == "forward" and session["forward"]:
            back = session["back"]
            back.append(session["current"])
            session["back"] = back
            forward = session["forward"]
            session["current"] = forward.pop()
            session["forward"] = forward

        elif action == "clear":
            session["back"] = []
            session["forward"] = []
            session["current"] = ""

        session.modified = True
        return redirect("/")

    history = session["back"] + ([session["current"]] if session["current"] else [])

    return render_template(
        "index.html",
        current=session["current"],
        history=history,
        can_back=len(session["back"]) > 0,
        can_forward=len(session["forward"]) > 0
    )

if __name__ == "__main__":
    app.run(debug=True)
