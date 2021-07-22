from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "TacoCatIsCoolMan"

debug = DebugToolbarExtension(app)

@app.route("/")
def landing_page():
    """shows the home page"""
    survey = satisfaction_survey
    return render_template("home.html", survey=survey)

@app.route("/start", methods=["POST"])
def start_request():
    """starts the survey"""
    # stores responses from user input on survey
    session["responses"] = []
    return redirect("/questions/0")

@app.route("/questions/<int:question_num>")
def question_page(question_num):
    """shows the page with the current survey question"""
    num_length = len(session["responses"])
    if question_num != num_length:
        flash("Trying to access an invalid question!", "warning")
        return redirect(f"/questions/{num_length}")
    question = satisfaction_survey.questions[question_num]
    return render_template("question.html", question=question)

@app.route("/answer", methods=["POST"])
def answer_page():
    """gets the answer from the question page & redirects to next question"""
    resps = session["responses"]
    answer = request.form.get("answer")
    resps.append(answer)
    session["responses"] = resps
    num = len(session["responses"])
    if num < len(satisfaction_survey.questions):
        return redirect(f"/questions/{num}")
    return redirect("/thanks")

@app.route("/thanks")
def thanks_page():
    """shows the thanks page for completing the survey"""
    return render_template("thanks.html")

