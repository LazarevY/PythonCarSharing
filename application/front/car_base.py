import app_context as a

app = a.app()


@app.route('/modeledit')
def model_edit():
    return 'There edit cer models'
