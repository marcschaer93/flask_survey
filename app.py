from flask import Flask, render_template, redirect, request, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'hyptoKrypto'

debug = DebugToolbarExtension(app)

@app.route('/')
def survey_home():
    """
    Shows title and instructions of a Survey with a Start Form
    """

    return render_template('start_survey.html', survey=survey)


@app.route('/start', methods=['POST'])
def start_survey():
    """Starts the choosen Survey"""
    session['responses'] = []

    return redirect('/questions/0')


@app.route('/answer', methods=["POST"])
def handle_question():
    """update the data in session and get the next Question"""
    #post the data of the named Form input field: name='answer'
    choice = request.form['answer']

    responses = session['responses']
    responses.append(choice)
    session['responses'] = responses

    return redirect(f"/questions/{len(responses)}")
    

@app.route('/questions/<int:Id>')
def show_question(Id):
    """shows the actual Question"""
    responses = session.get('responses')

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete_survey")

    if (len(responses) != Id):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {Id}.")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[Id]

    return render_template('questions.html', question_num = Id, question=question)
    

@app.route('/complete_survey')
def thank_you():
    """Survey complete"""

    return render_template('/complete_survey.html')
    
