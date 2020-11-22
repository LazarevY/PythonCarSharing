from flask import render_template

import app_context as a

app = a.app()


@app.route('/')
def hello_world():
    return render_template("start_page.html", modeledit='/modeledit')
