# import core flask
from flask import Flask, render_template

# import form class
from flask.ext.wtf import Form
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required

# import session related
from flask import session

# flask misc
from flask import redirect, url_for

# import interpreter package
from hjsintp.htmlast import parseHtml

# create a app instance
app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess hahaha'

@app.route('/', methods=['GET', 'POST'])
def index():
    text = None
    form = CodeForm()
    if form.validate_on_submit():
        text = form.text.data
        session['text'] = form.text.data
        ast = parseHtml(text)
        print(ast)
        session['ast'] = ast
        # form.text.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, text=session.get('text'), ast=session.get('ast')) 
    # session.get()方法的作用：若无此字段返回None 从而避免异常

class CodeForm(Form):
    """ 定义代码输入表单.
    """
    text = TextAreaField('Input your code here..', validators=[Required()])
    submit = SubmitField('Submit')

if __name__ == "__main__":
    app.run(debug=True)
