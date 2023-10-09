import os

from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)
# to run this from command line, first navigate to folder using cd FlaskStuff, then run > python 'filename.py'
posts = [
    {
        'subject': '1',
        'title': 'Blue Case Study',
        'content': 'It was mixed with red to make purple',
        'endexperiment': '2/4/12'
    },
    {
        'subject': '2',
        'title': 'Red Case Study',
        'content': 'It was mixed with yellow to make orange',
        'endexperiment': '3/5/16'
    }
]

@app.route("/") #basically url
def home():
    return render_template('home.html', posts=posts) #want to display home html using data stored in posts

@app.route("/buttons", methods=["POST","GET"])
def buttons():
    if request.method == "POST":
        if request.form['action'] == 'home' :
            return redirect(url_for("home"))
        elif request.form['action'] == 'continue':
            return redirect(url_for("boxes"))
        elif request.form['action'] == 'button 12478':
            return redirect(url_for("graph"))
        else:
            return redirect(url_for("buttons"))
    else:
        return render_template('buttons.html')
    #opening the buttons url is a GET method because it's taking information from us
    #in the buttons url, we have a bunch of post methods (from the input sections in buttons.html
    #if these are activated, meaning we get "POST", it will send us to the boxes page using
    #redirect and url_for function. Note name in url_for is name of function

    #based on what button you click, you will either get redirected or stay on buttons page

@app.route("/boxes", methods=["POST","GET"])
def boxes():
    if request.method == "POST":
        colorpicked = request.form["clr"]
        x1 = request.form.get('x1')
        x2 = request.form.get('x2')
        x3 = request.form.get('x3')
        y1 = request.form.get('y1')
        y2 = request.form.get('y2')
        y3 = request.form.get('y3')
        xs = [x1, x2, x3]
        ys = [y1, y2, y3]
        return render_template('graph.html', labels=xs, values=ys)
    else:
        return render_template('boxes.html')

@app.route("/<clr>")
def color(clr):
    return f"<h1>{clr}</h1>"



@app.route("/about")
def about():
    return render_template('about.html', title = 'about')

@app.route("/graph")
def graph():

    return render_template('graph.html', labels=labels, values=values)

@app.route("/test")
def test():
    return render_template('test.html')

if __name__ == "__main__":
    app.run(debug=True)