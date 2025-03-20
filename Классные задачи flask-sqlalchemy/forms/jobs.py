from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = StringField('Описание работы', validators=[DataRequired()])
    team_leader = IntegerField('Айди тим лида', validators=[DataRequired()])
    work_size = IntegerField('Объем работы в часах')
    collaborators = StringField('Список id участников', validators=[DataRequired()])
    is_finished = BooleanField('Работа завершена?', default=False)
    submit = SubmitField('Применить')
