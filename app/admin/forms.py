from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l

class JobForm(FlaskForm):
    title = StringField(_l('Job Title (English)'), validators=[DataRequired()])
    title_zh = StringField(_l('Job Title (Chinese)'), validators=[DataRequired()])
    description = TextAreaField(_l('Job Description (English)'), validators=[DataRequired()])
    description_zh = TextAreaField(_l('Job Description (Chinese)'), validators=[DataRequired()])
    location = StringField(_l('Location'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit')) 