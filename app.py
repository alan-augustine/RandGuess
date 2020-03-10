from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField
from wtforms.validators import InputRequired
from wtforms.fields.html5 import IntegerRangeField
from random import randrange

########################
app = Flask(__name__)
app.secret_key = "my_default_secret_key"
########################

class RandomNumberForm(FlaskForm):
    # DataRequired validator was not working properly
    user_guess = IntegerField("Your Guess", validators=[InputRequired()])
    # range max and min is handled in template file
    num_range_select = IntegerRangeField("Number Range: ")
    num_range_text = StringField()
    submit = SubmitField("Submit")

# GET  - get unfilled form
# POST - post filled form
@app.route('/', methods=['GET', 'POST'])
def index():
    form = RandomNumberForm()
    guess_result = 'NIL'
    if form.validate_on_submit():
        app.logger.info("hey")
        user_guess = form.user_guess.data
        num_range = form.num_range_select.data
        app.logger.info("num_range = " + str(num_range))
        system_guess = randrange(num_range)
        app.logger.info("System Guess = " + str(system_guess))
        if user_guess == system_guess:
            guess_result='SUCCESS'
        else:
            guess_result='FAIL'
        return render_template('home.html', form=form, guess_result=guess_result)
    # render_template , by default looks for template files in
    # 'templates' directory relative to app.py (or file where blueprint is defined ?)
    return render_template('home.html', form=form, guess_result=guess_result)

if __name__ == '__main__':
    app.run(debug=True)