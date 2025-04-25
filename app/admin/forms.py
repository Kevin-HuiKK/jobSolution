from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from flask_babel import lazy_gettext as _l

class JobForm(FlaskForm):
    title = StringField(_l('Job Title (English)'), validators=[DataRequired()])
    title_zh = StringField(_l('Job Title (Chinese)'))
    description = TextAreaField(_l('Job Description (English)'), validators=[DataRequired()])
    description_zh = TextAreaField(_l('Job Description (Chinese)'))
    location = StringField(_l('Location'), validators=[DataRequired()])
    headcount = StringField(_l('Headcount'), validators=[DataRequired()], 
                          description=_l("Enter a number or 'any' for unlimited"))
    submit = SubmitField(_l('Submit'))

    def validate_headcount(self, field):
        if field.data != 'any' and not field.data.isdigit():
            raise ValidationError(_l('Please enter a number or "any"')) 