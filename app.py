from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField
from wtforms.validators import InputRequired
from wtforms.fields.html5 import IntegerRangeField
from random import randrange

########################
app = Flask(__name__)
app.secret_key = "my_default_nonsecure_secret_key"
########################


class RandomNumberForm(FlaskForm):
    # DataRequired validator was not working properly
    user_guess = IntegerField("Your Guess", validators=[InputRequired()])
    # range max and min values are handled in template file
    num_range_select = IntegerRangeField("Number Range: ")
    num_range_text = StringField()
    submit = SubmitField("Submit")


# GET  - get home page with unfilled form
# POST - submit filled form to server
@app.route('/', methods=['GET', 'POST'])
def index():
    form = RandomNumberForm()
    guess_result = 'NIL'
    system_guess = None
    if form.validate_on_submit():
        app.logger.info("Validated Form")
        user_guess = form.user_guess.data
        num_range = form.num_range_select.data
        app.logger.info("num_range = " + str(num_range))
        system_guess = randrange(num_range)
        app.logger.info("System Guess = " + str(system_guess))
        if user_guess == system_guess:
            guess_result = 'SUCCESS'
        else:
            guess_result = 'FAIL'
        return render_template('home.html', form=form, guess_result=guess_result, system_guess=system_guess)
    # render_template , by default looks for template files in
    # 'templates' directory relative to app.py (or relative to file where blueprint is defined ?)
    return render_template('home.html', form=form, guess_result=guess_result, system_guess=system_guess)


if __name__ == '__main__':
    app.run(debug=True)
