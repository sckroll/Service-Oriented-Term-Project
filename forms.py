from flask_wtf import FlaskForm
import wtforms as f
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email
from wtforms import BooleanField, validators


class LoginForm(FlaskForm):
    # email = f.StringField('이메일', validators=[DataRequired(), Email()])
    email = EmailField('이메일', validators=[DataRequired()])
    password = f.PasswordField('비밀번호', validators=[DataRequired()])
    display = ['email', 'password']


class UserForm(FlaskForm):
    email = f.StringField('이메일', validators=[DataRequired()])
    password = f.PasswordField('비밀번호', validators=[DataRequired()])
    name = f.StringField('이름', validators=[DataRequired()])
    affiliation = f.StringField('소속', validators=[DataRequired()])
    agreement = BooleanField(
        '<div style="border: #eded 1px solid; padding:10px; ">'
        '<small style="font-size:1.0em;">본 사이트는 회원의 개인정보를 매우 중요시하며, 귀하의 개인정보를 보다 나은 서비스 즉, 유용한 정보에 한하여, 개인정보를 타 기관에 제공할 수 있습니다.</small>'
        '</div><br/>동의',
        validators=[DataRequired()]
    )

    display = ['email', 'password', 'name', 'affiliation', 'agreement']


class MyPageUserForm(FlaskForm):
    # email = f.StringField('이메일', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired()])
    password = f.PasswordField('비밀번호', validators=[DataRequired()])
    name = f.StringField('이름', validators=[DataRequired(), validators.Length(min=3, max=45)])
    affiliation = f.StringField('소속', validators=[DataRequired()])

    display = ['email', 'password', 'name', 'affiliation']


class LostData(FlaskForm):
    LostName = f.StringField('LostName', validators=[DataRequired()])
    LostStartDate = f.StringField('StartDate', validators=[DataRequired()])
    LostEndDate = f.StringField('EndDate', validators=[DataRequired()])
    LostRange = f.StringField('LostRange', validators=[DataRequired()])
    LostPlace = f.StringField('LostPlace', validators=[DataRequired()])

    display = ['LostName', 'LostStartDate', LostEndDate, 'LostRange', 'LostPlace']