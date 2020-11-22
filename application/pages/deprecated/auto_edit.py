from flask import render_template, redirect

from app_context import app, db
from application.database.modeles.auto import Auto
from application.database.modeles.auto_brand import AutoBrand
from application.database.modeles.auto_model import AutoModel
from application.database.modeles.model_price import ModelPrice
from application.pages.forms.auto_edit_form import AutoEdit

appl = app()


@appl.route('/auto/edit')
def gen_auto_edit():
    form = AutoEdit()
    autos_q = db() \
        .query(Auto).join(AutoModel, Auto.model_id == AutoModel.model_id) \
        .join(AutoBrand, AutoBrand.brand_id == AutoModel.brand_id) \
        .join(ModelPrice, ModelPrice.model_id == Auto.model_id) \
        .with_entities(AutoModel.model_name, AutoBrand.brand_name, Auto.registration_number, Auto.mileage, Auto.quality)
    autos = autos_q.all()
    return render_template("auto_edit.html", form=form, autos=autos)


@appl.route('/auto/edit/submit', methods=['POST'])
def auto_edit_action():
    form = AutoEdit()

    if form.update_submit.data and form.validate():
        return auto_update(form)
    elif form.delete_submit.data and form.validate():
        return auto_delete(form)

    return redirect('/auto/edit')


def auto_delete(form: AutoEdit):
    auto_id = form.number_select.data

    db().query(Auto).filter(Auto.auto_id == auto_id).delete()
    return redirect('/auto/edit')


def auto_update(form: AutoEdit):
    auto_id = form.number_select.data

    db() \
        .query(Auto) \
        .filter(Auto.auto_id == auto_id) \
        .update(
        {Auto.registration_number: form.number.data,
         Auto.mileage: form.mileage.data,
         Auto.quality: form.quality.data})
    db().commit_session()

    return redirect('/auto/edit')
