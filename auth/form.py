from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,FileField,TextAreaField
from wtforms.validators import InputRequired,Length,ValidationError



from application.models import *

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"User Name"})

    password = PasswordField(validators=[InputRequired(),Length(min=8,max=20)],render_kw={"placeholder":"Password"})
    keys = StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Security Key"})

    name = StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Name"})
    age = StringField(validators=[InputRequired(),Length(min=1,max=2)],render_kw={"placeholder":"age"})
    address=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Address"})
    about = StringField(validators=[InputRequired(),Length(min=4,max=200)],render_kw={"placeholder":"About you"})
    email = StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"email"})
    submit = SubmitField("Register")

    def validation_username(self,username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()

        if existing_user_username:
            raise ValidationError("This username already exist")

    def validation_age(self,age):
       

        if age.data<18:
            raise ValidationError("This username already exist")



class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"username"})

    password = PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Password"})

    submit = SubmitField("Login")

class Resetpass(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"User Name"})
    
    newpassword = PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"New Password"})
    keys = StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Security Key"})
    submit = SubmitField("Submit")

class Edit_Profile(FlaskForm):
    # username = StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"User Name"})
    keys = StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Security Key"})

    name = StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Name"})
    age = StringField(validators=[InputRequired(),Length(min=1,max=2)],render_kw={"placeholder":"age"})
    address=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Address"})
    about = StringField(validators=[InputRequired(),Length(min=4,max=200)],render_kw={"placeholder":"About you"})
    email = StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"email"})
    submit = SubmitField("Save")

    
class Search(FlaskForm):
    word = StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"search"})
    submit = SubmitField("search")