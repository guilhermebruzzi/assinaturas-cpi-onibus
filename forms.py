from flask.ext.mongoengine.wtf import model_form
from flask.ext.wtf import RecaptchaField

from models import User

UserForm = model_form(User)

class UserCaptchaForm(UserForm):
    captcha = RecaptchaField()