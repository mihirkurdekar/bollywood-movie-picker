import os
from pathlib import Path

import pandas as pd
from flask import Flask, request, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

QUESTION_POOL = [
    "Act it out without speaking",
    "Describe the movie with only one word",
    "Use sound effects only",
    "Mime the movie title",
    "Give only clues, no movie name",
    "Act like the lead character",
    "Use your body to show the emotion",
    "Hint the plot with three gestures",
    "Pretend to be the soundtrack",
    "Show a scene from the movie",
]


def load_movies():
    return pd.read_parquet(Path(__file__).resolve().parent / "static" / "bollywood_movies.parquet")


movies = load_movies()


def normalize_player_name(raw_name, fallback):
    cleaned_name = (raw_name or "").strip()
    return cleaned_name or fallback


def get_next_question(pool, used_questions=None):
    if used_questions is None:
        used_questions = []

    if not pool:
        return None

    remaining = [question for question in pool if question not in used_questions]
    if not remaining:
        remaining = list(pool)

    next_question = remaining[0]
    used_questions.append(next_question)
    return next_question


def build_wildcard_spinner_html(label):
    return f"""
    <div class='wildcard-spinner text-center p-3 border rounded bg-light'>
        <div class='spinner-ring d-flex align-items-center justify-content-center mx-auto mb-2' style='width: 96px; height: 96px; border-radius: 50%; border: 6px solid #f0c14b; border-top-color: #c77d00; animation: spin 1s linear infinite;'>
            <span style='font-size: 2rem;'>⭐</span>
        </div>
        <h5 class='mb-1'>{label}</h5>
        <p class='small text-muted mb-0'>Use this when the team needs a surprise twist.</p>
    </div>
    <style>@keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}</style>
    """


@app.route("/", methods=["GET", "POST"])
def hello_world():
    player_1 = normalize_player_name(request.form.get("player_1"), "Player 1")
    player_2 = normalize_player_name(request.form.get("player_2"), "Player 2")

    action = request.form.get("action", "")
    question_history = list(session.get("question_history", []))

    if action == "reset_questions":
        question_history = []
        session["question_history"] = []
        session["current_question"] = None
    elif action == "next_question":
        question = get_next_question(QUESTION_POOL, question_history)
        session["question_history"] = question_history
        session["current_question"] = question
    elif not session.get("current_question"):
        question = get_next_question(QUESTION_POOL, question_history)
        session["question_history"] = question_history
        session["current_question"] = question
    else:
        question = session.get("current_question")

    if "current_question" not in session or not session.get("current_question"):
        question = get_next_question(QUESTION_POOL, question_history)
        session["question_history"] = question_history
        session["current_question"] = question

    movie = movies.sample()
    title = movie["title"].values[0]
    title_id = movie["titleId"].values[0]
    imdb_url = f"https://www.imdb.com/title/{title_id}/"
    wildcard_html = build_wildcard_spinner_html("Wild Card")
    question_number = len(question_history)

    html = f"""
    <!doctype html>
    <html lang='en'>
    <head>
        <meta charset='utf-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1'>
        <title>Bollywood Movie Picker</title>
        <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css' rel='stylesheet'>
    </head>
    <body>
    <header class='container py-3'>
        <nav class='navbar navbar-light bg-light rounded px-3'>
            <h1 class='h3 mb-0'>Bollywood Movie Picker!</h1>
        </nav>
    </header>
    <main class='container py-3'>
        <div class='card p-4 mb-4'>
            <form method='post' class='row g-3 align-items-end'>
                <div class='col-md-5'>
                    <label for='player_1' class='form-label'>Player 1</label>
                    <input type='text' class='form-control' id='player_1' name='player_1' maxlength='40' value='{player_1}'>
                </div>
                <div class='col-md-5'>
                    <label for='player_2' class='form-label'>Player 2</label>
                    <input type='text' class='form-control' id='player_2' name='player_2' maxlength='40' value='{player_2}'>
                </div>
                <div class='col-md-2'>
                    <button type='submit' class='btn btn-primary w-100'>Start</button>
                </div>
            </form>
            <p class='mt-3 mb-0'>Players: <strong>{player_1}</strong> and <strong>{player_2}</strong></p>
        </div>

        <div class='card p-4 mb-4'>
            <div class='row g-4 align-items-start'>
                <div class='col-lg-7'>
                    <p class='text-muted mb-2'>Round challenge</p>
                    <h3 class='mb-3'>Question {question_number}: {question}</h3>
                    <form method='post' class='d-flex flex-wrap gap-2'>
                        <input type='hidden' name='action' value='next_question'>
                        <button type='submit' class='btn btn-outline-primary'>Next question</button>
                        <button type='submit' class='btn btn-outline-secondary' formaction='/' formmethod='get'>Refresh movie</button>
                    </form>
                    <form method='post' class='mt-2'>
                        <input type='hidden' name='action' value='reset_questions'>
                        <button type='submit' class='btn btn-link p-0'>Reset question deck</button>
                    </form>
                </div>
                <div class='col-lg-5'>
                    {wildcard_html}
                </div>
            </div>
        </div>

        <div class='container'>
            <p> Movie: <a href='{imdb_url}' target='_blank'>{title}</a></p>
            <button class='btn btn-outline-secondary' onclick='window.location.reload()'>Refresh Movie</button>
        </div>
        <div class='container mt-4'>
            <p>This app is developed for playing Dumb Charades or pictionary kind of games.</p>
            <b>Happy guessing!</b>
        </div>
    </main>
    <footer class='container py-3'>
        <p>Reference from list: <a href='https://www.imdb.com/search/title/?title_type=feature&languages=hi' target='_blank'>imdb filtered list</a></p>
        <p>Code reference: <a target='_blank' href='https://github.com/mihirkurdekar/bollywood-movie-picker/blob/master/notebooks'>Mihir's Jupyter Notebook</a></p>
    </footer>
    </body>
    </html>
    """
    return html


if __name__ == '__main__':
    app.run()
