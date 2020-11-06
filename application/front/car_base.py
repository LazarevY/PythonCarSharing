from flask import render_template, redirect

import app_context as a
from application.database.modeles.auto_brand import AutoBrand
from application.database.modeles.auto_model import AutoModel
from application.front.forms.brand_form import BrandForm
from application.front.forms.model_form import ModelForm

app = a.app()
brands_backup = []
brand_for_model = None
error_msg = ''


def add_brand(form: BrandForm):
    global error_msg
    brand = form.new_brand_name.data

    l = a.db().query(AutoBrand).filter(AutoBrand.brand_name == brand).all()
    if len(l) != 0:
        error_msg = f'{brand} already exist!'

    a.db().add_entity_object(AutoBrand(brand_name=brand))
    a.db().commit_session()
    error_msg = ''
    return redirect('/modeledit')


def view_models(form: ModelForm):
    global brand_for_model
    brand_for_model = form.brand_name.data
    return redirect('/modeledit')


def model_form_action(form: ModelForm):
    pass


@app.route('/modeledit', methods=['GET', 'POST'])
def page_gen():
    global error_msg
    global brands_backup
    form = BrandForm()
    model_form = ModelForm()

    brands_q = a.db().query(AutoBrand).all()
    brands = brands_q
    brands_backup = brands
    model_form.set_brands([(b.brand_id, b.brand_name) for b in brands])

    model_q = a.db().query(AutoModel).filter(AutoModel.brand_id == brand_for_model).all()
    model_form.set_models([m.model_name for m in model_q])

    error_msg = ''
    return render_template("model_edit.html",
                           model_form=model_form,
                           brand_form=form)


@app.route('/model_action', methods=['POST'])
def model_action():
    global error_msg
    global brands_backup
    form = BrandForm()
    model_form = ModelForm()

    if model_form.view_models.data:
        return view_models(model_form)

    if model_form.validate_on_submit():
        return model_form_action(model_form)

    error_msg = ''
    return redirect('/modeledit')


@app.route('/brand_action', methods=['POST'])
def brand_action():
    global error_msg
    global brands_backup
    form = BrandForm()
    model_form = ModelForm()


    if form.validate_on_submit():
        return add_brand(form)
    form.error_string = error_msg

    error_msg = ''
    return redirect('/modeledit')
