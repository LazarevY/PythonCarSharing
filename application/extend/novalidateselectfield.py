from wtforms import SelectField


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass
