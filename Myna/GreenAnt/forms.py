
from wtforms import StringField, TextAreaField, SubmitField, SelectField, FieldList


class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')

