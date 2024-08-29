from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import Pet, db, connect_db 
from forms import AddPetForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def show_homepage():
    pets = Pet.query.all()
    return render_template('homepage.html', pets=pets)

@app.route('/add', methods=["GET", "POST"])
def add_pet():
    form = AddPetForm()

    if form.validate_on_submit():
        new_pet = Pet(
            name=form.name.data,
            species=form.species.data,
            photo_url=form.photo_url.data,
            age=form.age.data,
            notes=form.notes.data,
            available=True
        )
        db.session.add(new_pet)
        db.session.commit()
        return redirect(url_for('show_homepage'))
    
    return render_template('add_pet.html', form=form)

