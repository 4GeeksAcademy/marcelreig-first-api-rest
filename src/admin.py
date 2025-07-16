import os
from flask_admin import Admin
from models import db, User, Planet, Character
from flask_admin.contrib.sqla import ModelView


class UserAdmin(ModelView):
    column_list = ["email", "favorite_planet",
                   "favorite_character", "is_active"]
    form_columns = ["email", "password", "is_active",
                    "favorite_planet", "favorite_character"]


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserAdmin(User, db.session))

    admin.add_view(ModelView(Character, db.session))
    admin.add_view(ModelView(Planet, db.session))
    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
   