from wtforms import StringField
from wtforms.compat import text_type
from html import escape


class EscapeStringField(StringField):
    def process_formdata(self, valuelist):
        if valuelist:
            self.data = escape(valuelist[0])
        elif self.data is None:
            self.data = ''

    def _value(self):
        return text_type(escape(self.data)) if self.data is not None else ''
