#!/usr/bin/env python
# coding: utf-8

# In[7]:


"""get_ipython().system('pip3 install flask')
get_ipython().system('pip3 install flash')
get_ipython().system('pip3 install wtforms')"""


# In[8]:


from flask import Flask, render_template, request, flash
from wtforms import Form, FloatField, SubmitField, validators, ValidationError
import numpy as np
import joblib


# In[9]:


def predict(parameters):
    mdoel = joblib.load('/Users/akosuke/data-glacier/Flask\ /Iris\ Predict/nn.pkl')
    params = parameters.reshape(1,-1)
    pred = model.predict(params)
    return pred


# In[10]:


def getName(label):
    print(label)
    if label == 0:
        return "Iris Setosa"
    elif label == 1:
        return "Iris Versicolor"
    elif label == 2:
        return "Iris Virginica"
    else:
        return "Error"

app = Flask(__name__)
app.config.from_object(__name__)
app.config["SECRET_KEY"] = "zJe09C5c3tMf5FnNL09C5d6SAzZoY"


# In[ ]:


class IrisForm(Form):
    SepalLength = FloatField("Sepal Length(cm)",
                            [validators.InputRequired("Input Required"),
                            validators.NumberRange(min = 0, max = 10)])

    SepalWidth = FloatField("Sepal Width(cm)",
                           [validators.InputRequired("Input Required"),
                           validators.NumberRange(min = 0, max = 10)])

    PetalLength = FloatField("Petal Length(cm)",
                            [validators.InputRequired("Input Required"),
                            validators.NumberRange(min = 0, max = 10)])

    PetalWidth = FloatField("Petal Width(cm)",
                           [validators.InputRequired("InputRequired"),
                           validators.NumberRange(min = 0, max = 10)])

    submit = SubmitField("Classify")

    @app.route('/',methods = ['GET','POST'])

    def predicts():
        form = IrisForm(request.form)
        if request.method == "POST":
            if form.validate() == False:
                flash("Input Required.")
                return render_template("index.html", form = form)
            else:
                SepalLength = float(request.form["SepalLength"])
                SepalWidth = float(request.form["SepalWidth"])
                PetalLength = float(request.form["PetalLength"])
                PetalWidth = float(request.form["PetalWidth"])

                x = np.array([SepalLength, SepalWidth, PetalLength, PetalWidth])

                pred = predict(x)
                irisName = getName(pred)

                return render_template("result.html",irisName = irisName)
        elif request.method == "GET":
            return render_template("index.html", form = form)

if __name__ == "__main__":
    app.debug = True
    app.run()
