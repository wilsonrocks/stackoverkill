from flask import Flask, render_template, abort, url_for, redirect, request, Markup, jsonify
from models import Question, Answer, db, Famq
from forms import New_Question, New_Answer
import secrets

import re

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.SECRET_KEY
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.before_request
def db_connect():
    db.get_conn()

@app.after_request
def db_disconnect(response):
    if not db.is_closed():
        db.close()
    return response #because response could be modified and this is what does it?

@app.route('/')
def Index():
    return(redirect(url_for('All_questions')))

@app.route('/question/<id>')
def Question_view(id):
    form = New_Answer(id=id,test="test")
    try:
        question = Question.get(id=id)
        return(render_template("question.html",question=question,form=form))
    except Question.DoesNotExist:
        abort(404)

@app.route('/all')
def All_questions():
    questions = Question.select().order_by(-Question.timestamp)
    return(render_template("question_set.html",questions=questions))

@app.route('/unanswered')
def Unanswered():
    answers = {a.question.id for a in Answer.select().join(Question)}
    questions = Question.select().where(~(Question.id << answers))
    return render_template('question_set.html',questions=questions) 

@app.route('/ask', methods=['GET', 'POST'])
def Ask():
    form = New_Question()
    if form.validate_on_submit(): 
        q = Question.create(text=form.text.data) #was adding all confusing "<textarea>" stuff till I realised to add .data on the end
        return redirect(url_for('Question_view',id=q.id))

    return render_template('newquestion.html', form=form)

@app.route('/answer', methods=['POST'])
def Submit_Answer():
    form = New_Answer()
    if form.validate_on_submit():
        Answer.create(text=form.text.data,question=Question.get(id=form.id.data))
        return redirect(url_for('Question_view',id=form.id.data))

@app.route('/search')
def Search():
    term = request.args.get("searchterm",'')
    questions = Question.select().where(Question.text.contains(term))
    return render_template('question_set.html',questions=questions)

@app.route('/get_likes', methods=['POST'])
def Get_likes():
    """Returns the number of likes for the answer with id 'id'. Defaults to 0."""

    id = request.form.get('id', default=0)
    try:
        likes = Answer.get(id=int(id)).likes
        return jsonify(likes)
    except Answer.DoesNotExist:
        return jsonify(0)

@app.route('/like/<question>/<answer>')
def Like(question,answer):
    a = Answer.get(id=answer)
    a.likes +=1
    a.save()
    return redirect(url_for('Question_view',id=question)+"#answer{}".format(answer))

@app.route('/famq')
def Famqs():
    return render_template('famq.html',famqs=Famq.select())


#filters

@app.template_filter('our_timestamp')
def our_timestamp_filter(timestamp):
    return timestamp.strftime("%a %d/%m/%y")


def add_hash(matchobj):
    s = matchobj.group(0)
    return Markup('<a href="{}">{}</a>'.format(url_for('Search',searchterm=s[1:]),s))

@app.template_filter('hashtagize')
def hashtag_filter(text):
    
    return re.sub(r'#(\w|\d)*',add_hash,text)
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9988,debug=True)
