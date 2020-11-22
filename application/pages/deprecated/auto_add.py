from flask import render_template

from app_context import app, db
from application.database.modeles.auto import Auto
from application.pages.forms.auto_add_form import AutoAdd

appl = app()


@appl.route('/auto/add', methods=['GET', 'POST'])
def auto_page_gen():
    form = AutoAdd()

    if form.validate_on_submit():
        auto = Auto(status_id=0, model_id=form.model_select.data, registration_number=form.number, mileage=form.mileage,
                    quality=form.quality)
        with db()._session.begin():
            db().add_entity_object(auto)
            db().commit_session()

    form = AutoAdd()

    return render_template("auto_add.html", form=form)
