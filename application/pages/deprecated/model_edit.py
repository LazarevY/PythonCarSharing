from flask import render_template, redirect

from app_context import app, db
from application.database.modeles.auto_brand import AutoBrand
from application.database.modeles.auto_model import AutoModel
from application.database.modeles.model_price import ModelPrice
from application.pages.forms.model_edit_form import ModelEditForm

appl = app()


@appl.route('/model/edit')
def model_edit():
    model_edit_form = ModelEditForm()

    models_q = db() \
        .query(AutoModel) \
        .join(AutoBrand, AutoBrand.brand_id == AutoModel.brand_id) \
        .join(ModelPrice, ModelPrice.model_id == AutoModel.model_id) \
        .with_entities(AutoModel.model_name, AutoBrand.brand_name, ModelPrice.price)

    models = models_q.all()

    return render_template("model_edit.html", form=model_edit_form, models=models)


@appl.route('/model/edit/submit', methods=['POST'])
def model_edit_submit():
    form = ModelEditForm()
    form.validate_on_submit()

    if form.update_submit.data:
        form.validate()
        return model_update(form)
    elif form.delete_submit.data:
        form.validate()
        return model_delete(form)

    return redirect("/model/edit")


def model_delete(form: ModelEditForm):
    model_id = form.model_select.data
    db().query(AutoModel).filter(AutoModel.model_id == model_id).delete()
    db().commit_session()
    return redirect("/model/edit")


def model_update(form: ModelEditForm):
    model_id = form.model_select.data

    db() \
        .query(AutoModel) \
        .filter(AutoModel.model_id == model_id) \
        .update({AutoModel.brand_id: form.model_brand.data.brand_id,
                 AutoModel.model_name: form.model_name.data})
    db().commit_session()

    q = db().query(ModelPrice).filter(ModelPrice.model_id == model_id).all()
    if len(q) == 0:
        model_price = ModelPrice(model_id=model_id, price=int(form.model_price.data))
        db().add_entity_object(model_price)
    else:
        db().query(ModelPrice).filter(ModelPrice.model_id == model_id).update(
            {ModelPrice.price: int(form.model_price.data)})
    db().commit_session()
    return redirect("/model/edit")
