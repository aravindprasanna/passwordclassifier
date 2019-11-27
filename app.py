from flask import Flask, jsonify, request,render_template, flash
import pickle
import numpy as np
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# load model
model = pickle.load(open('model.pkl','rb'))

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class ReusableForm(Form):
    pwd = StringField('Password:', validators=[validators.required()])

@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
    print(form.errors)

    if request.method == 'POST':
        pwd = request.form['pwd']
        print(pwd)

        if form.validate():
            res = predict(password_numeric(pwd))
            res_val = int(res)
            if res_val == 0:
                msg = 'Weak'
            elif res_val == 1:
                msg = 'Medium'
            elif res_val == 2:
                msg = 'Strong'

            flash(msg)

        else:
            flash('All the form fields are required. ')

    return render_template('hello.html', form=form)



def predict(pass_word):
    # get data
    # data = request.get_json(force=True)

    # convert data into dataframe
    # data.update((x, [y]) for x, y in data.items())
    # data_df = pd.DataFrame.from_dict(data)

    # predictions
    result = model.predict(pass_word)
    print(type(result))
    print(result.shape)
    # send back to browser
    # output = {'results': int(result[0])}

    # return data
    return result


def password_numeric(password_string):
    num_vector = np.zeros((1, 6), dtype=int)
    num_vector[0][0] = len(password_string)
    num_vector[0][1] = len([x for x in list(password_string) if x.isdigit()])
    num_vector[0][2] = len([x for x in list(password_string) if x.isalpha()])
    num_vector[0][3] = sum([x.islower() for x in list(password_string) if x.isalpha()])
    num_vector[0][4] = num_vector[0][2] - num_vector[0][3]
    num_vector[0][5] = num_vector[0][0] - (num_vector[0][2] + num_vector[0][1])

    return num_vector

if __name__ == '__main__':
    app.run()
