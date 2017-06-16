from flask import Flask, url_for, render_template, session, redirect, flash, g
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,PasswordField,SelectField
from wtforms.validators import Required, NumberRange, Length, EqualTo
from datetime import datetime
from cache_channel_list import CacheChannel
import Qcloud_live

class NameForm(Form):
    ctime = SelectField('New_ChannelID', coerce=int,validators=[])
    submit = SubmitField('SUBMIT')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ni cai'
manager = Manager(app)
bootstrap = Bootstrap(app)

@app.route('/',methods=['GET', 'POST'])
def index():
    qLive = Qcloud_live.QQlive()
    req = CacheChannel()
    ctime_list = [(x[0]+1, x[1]) for x in enumerate(req)]
    nameForm = NameForm()
    nameForm.ctime.choices = ctime_list

    if nameForm.validate_on_submit():
        ctime = nameForm.ctime.data
        for i in ctime_list:
            if ctime in i:
                cid = i[1][1]

        session['id'] = cid
        session['data'] = qLive.geturl(cid)
        return redirect(url_for('index'))
    return render_template('index.html',form=nameForm,id=session.get('id'), a=session.get('data'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    manager.run()
