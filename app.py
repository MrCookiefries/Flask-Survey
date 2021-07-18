import re
from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "TacoCatIsCoolMan"

debug = DebugToolbarExtension(app)

# stores responses from user input on survey
responses = []

@app.route("/")
def landing_page():
    """shows the home page"""
    survey = satisfaction_survey
    return render_template("home.html", survey=survey)

@app.route("/questions/<int:question_num>")
def question_page(question_num):
    """shows the page with the current survey question"""
    num_length = len(responses)
    if question_num != num_length:
        flash("Trying to access an invalid question!", "warning")
        return redirect(f"/questions/{num_length}")
    question = satisfaction_survey.questions[question_num]
    return render_template("question.html", question=question)

@app.route("/answer", methods=["POST"])
def answer_page():
    """gets the answer from the question page & redirects to next question"""
    responses.append(request.form.get("answer"))
    num = len(responses)
    if num < len(satisfaction_survey.questions):
        return redirect(f"/questions/{num}")
    return redirect("/thanks")

@app.route("/thanks")
def thanks_page():
    """shows the thanks page for completing the survey"""
    return render_template("thanks.html")

