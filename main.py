from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'
ckeditor = CKEditor(app)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Cafes(db.Model):
    __tablename__ = 'cafe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(250), unique=True, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False, default=False, server_default="false")
    has_toilet = db.Column(db.Boolean, nullable=False, default=False, server_default="false")
    has_wifi = db.Column(db.Boolean, nullable=False, default=False, server_default="false")
    can_take_calls = db.Column(db.Boolean, nullable=False, default=False, server_default="false")
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)

class CreateNewCafe(FlaskForm):
    name = StringField("Name of Cafe", validators=[DataRequired()])
    map_url = StringField("Maps of Cafe", validators=[DataRequired(), URL()])
    img_url = StringField("Image of Cafe", validators=[DataRequired(), URL()])
    location = StringField("Location of Cafe", validators=[DataRequired()])
    has_sockets = BooleanField("Has Sockets", validators=[DataRequired()])
    has_toilet = BooleanField("Has Toilets", validators=[DataRequired()])
    has_wifi = BooleanField("Has Wi-fi", validators=[DataRequired()])
    can_take_calls = BooleanField("Can Take Calls", validators=[DataRequired()])
    seats = StringField("Seats in Cafe", validators=[DataRequired()])
    coffee_price = StringField("Price of Coffee", validators=[DataRequired()])
    submit = SubmitField("New Cafe")


@app.route("/")
def home():
    cafes = Cafes.query.all()
    return render_template("index.html", all_cafes=cafes)


@app.route("/cafe/<int:index>")
def cafe(index):
    requested_cafe = Cafes.query.get(index)
    # for cafe in cafes:
    #     if cafe["id"] == index:
    #         requested_cafe = cafe
    return render_template("cafe.html", cafe=requested_cafe)


@app.route("/search")
def search():
    key = request.args.get("key")
    if key:
        all_cafes = Cafes.query.filter(Cafes.location.contains(key) | Cafes.name.contains(key))
    else:
        all_cafes = Cafes.query.all()
    return render_template('index.html', all_cafes=all_cafes)


@app.route("/add", methods=["GET", "POST"])
def add_new_cafe():
    form = CreateNewCafe()
    if form.validate_on_submit():
        new_cafes = Cafes(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
        )
        db.session.add(new_cafes)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("new_cafe.html", form=form)


@app.route("/edit-cafe/<int:cafe_id>", methods=["GET", "POST"])
def edit_cafe(cafe_id):
    cafe = Cafes.query.get(cafe_id)
    edit_form = CreateNewCafe(
        name=cafe.name,
        map_url=cafe.map_url,
        img_url=cafe.img_url,
        location=cafe.location,
        has_sockets=cafe.has_sockets,
        has_toilet=cafe.has_toilet,
        has_wifi=cafe.has_wifi,
        can_take_calls=cafe.can_take_calls,
        seats=cafe.seats,
        coffee_price=cafe.coffee_price
    )
    if edit_form.validate_on_submit():
        cafe.name = edit_form.name.data
        cafe.map_url = edit_form.map_url.data
        cafe.img_url = edit_form.img_url.data
        cafe.location = edit_form.location.data
        cafe.has_sockets = edit_form.has_sockets.data
        cafe.has_toilet = edit_form.has_toilet.data
        cafe.has_wifi = edit_form.has_wifi.data
        cafe.can_take_calls = edit_form.can_take_calls.data
        cafe.seats = edit_form.seats.data
        cafe.coffee_price = edit_form.coffee_price.data
        db.session.commit()
        return redirect(url_for('cafe', index=cafe_id))
    return render_template("new_cafe.html", form=edit_form, is_edit=True)


@app.route("/delete/<int:cafe_id>")
def delete(cafe_id):
    cafe_to_delete = Cafes.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
