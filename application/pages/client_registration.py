from flask import render_template, flash, redirect
from sqlalchemy import or_

import app_context as a
from application.database.modeles.client import Client
from application.pages.forms.client_form import ClientForm

app = a.app()
db = a.db()


@app.route('/register', methods=['GET'])
def client_page_gen():
    form = ClientForm()
    return render_template("register_form.html", client_form=form)


@app.route('/register_proc', methods=['POST'])
def register_client():
    form = ClientForm()

    if not form.validate_on_submit():
        flash('Check fields!')
        return redirect('/register')

    passport = form.passport.data
    drive_license = form.drive_license.data

    p = db.query(Client).filter(or_(Client.client_passport == str(passport),
                                    Client.client_drive_license == str(drive_license))).all()
    if len(p) != 0:
        flash('Client with such passport or license already exist!')
        return redirect('/register')

    cl = Client(
        client_name=form.name.data,
        client_second_name=form.surname.data,
        client_passport=str(passport),
        client_drive_license=str(drive_license)
    )

    db.add_entity_object(cl)
    db.commit_session()
    return redirect('/register')

