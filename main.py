from flask import redirect, render_template, request, session, abort, url_for
import os
from random import randint

# user-defined imports
from app import app, SignUpForm, mail
from user import check_user_password, create_user, get_name
from question import check_one_answer, get_next_question, update_attempts
from leaderboard import get_rankings
# from question import get_questions, check_answers  # deprecated


@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:  # user is logged in
        return render_template('index.html')

@app.route('/leaderboard')
def leaderboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    rankings = get_rankings()
    return render_template('leaderboard.html', rankings = rankings)

'''
@app.route('/play', methods = ['GET', 'POST'])  # deprecated
def play():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    questions = get_questions()
    if request.method == 'GET':
        session['questionIDs'] = [question.QuestionID for question in questions]
        return render_template('play.html', questions = questions)
    elif request.method == 'POST':
        user_answers = {}
        for questionID in session['questionIDs']:
            user_answer = request.form['answer_'+str(questionID)]
            user_answers[questionID] = int(user_answer)
        results = check_answers(user_answers)
        score = sum([results[key] for key in results])
        return render_template('review.html', results=results, questions=questions, score=score)
'''

@app.route('/play', methods=['GET', 'POST'])
def play():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'GET':
        question = get_next_question(session.get('userid'))
        if question:
            session['questionid'] = question.QuestionID
            session['flipped'] = randint(0, 1)==1

        return render_template('play.html', questions=[question])

    elif request.method == 'POST':
        questionid = session.get('questionid')
        user_answer = request.form['answer_'+str(questionid)]

        update_attempts(session.get('userid'), questionid, user_answer)
        correct, question = check_one_answer(questionid, user_answer)
        results = {questionid:correct}

        return render_template('review.html', results=results, questions=[question], score=int(correct))
        

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        form = SignUpForm()
        return render_template('signup.html', form=form)  # prompt user to sign up
    elif request.method == "POST":
        password = request.form['password']
        userid = request.form['userid']
        user_name = request.form['user_name']
        email = request.form['email']
        log_in = request.form.getlist('log_in')   # log me in too!
        if not get_name(userid):  # if user doesn't exist
            create_user(userid, user_name, password, email)
            if len(log_in)>0:
                return redirect(url_for('login'), code=307)  # continue post request to log user in
            else:
                return redirect(url_for('login'))
        else:  # userid already taken
            form = SignUpForm()
            return render_template('signup.html', res=1, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')  # prompt user to log in
    elif request.method == "POST":
        password = request.form['password']
        userid = request.form['userid']
        res = check_user_password(userid, password)
        if res == 1:  # correct password
            session['logged_in'] = True
            session['userid'] = userid
            session['user_name'] = get_name(userid)
            return redirect(url_for('index'))
        else:  # wrong password or wrong userid
            print(res)
            return render_template('login.html', res = res)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('userid', None)
    session.pop('user_name', None)
    return redirect(url_for('login'))
    
'''
@app.route('/forgot_pw', methods=['GET', 'POST'])
def forgot_pw():
    if request.method == "GET":
        return render_template('forgot-pw.html')  # prompt user to log in
    elif request.method =="POST":
        return render_template('forgot-pw.html')

'''

@app.after_request
def add_header(response):
    '''
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    '''
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=1'
    return response


@app.errorhandler(404)
def page_not_found(error):
    # Custom 404 page handler
    return render_template('404.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    # for local deployment
    #app.run(debug=True)
    # for heroku
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
