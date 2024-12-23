from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # Update with your database URI
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Models
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    postal_codes = db.relationship("PostalCodeRestaurant", back_populates="restaurants")

class PostalCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postal_code = db.Column(db.String(20), nullable=False)
    restaurants = db.relationship("PostalCodeRestaurant", back_populates="postal_codes")

class PostalCodeRestaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Float, nullable=False, default=0.0)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"), nullable=False)
    postal_code_id = db.Column(db.Integer, db.ForeignKey("postal_code.id"), nullable=False)
    restaurants = db.relationship("Restaurant", back_populates="postal_codes")
    postal_codes = db.relationship("PostalCode", back_populates="restaurants")

# Forms
class SetDeliveryRadiusForm(FlaskForm):
    restaurant_id = SelectField("Restaurant", choices=[], coerce=int, validators=[DataRequired()])
    postal_code = SelectField("Postal Code", choices=[], coerce=int, validators=[DataRequired()])
    distance = FloatField("Distance (km)", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Set Delivery Radius")

# View function
def set_delivery_radius_component():
    # Fetch restaurants and postal codes for form choices
    restaurants = Restaurant.query.all()
    postal_codes = PostalCode.query.all()

    restaurant_choices = [(restaurant.id, restaurant.name) for restaurant in restaurants]
    postal_code_choices = [(postal.id, postal.postal_code) for postal in postal_codes]

    # Initialize form and populate choices
    set_delivery_radius_form = SetDeliveryRadiusForm()
    set_delivery_radius_form.restaurant_id.choices = restaurant_choices
    set_delivery_radius_form.postal_code.choices = postal_code_choices

    # Process form submission
    if set_delivery_radius_form.validate_on_submit():
        restaurant_id = set_delivery_radius_form.restaurant_id.data
        postal_code_id = set_delivery_radius_form.postal_code.data
        distance = set_delivery_radius_form.distance.data

        # Check if the relationship already exists
        postal_code_restaurant = PostalCodeRestaurant.query.filter_by(
            restaurant_id=restaurant_id, postal_code_id=postal_code_id
        ).first()

        if postal_code_restaurant:
            # Update existing record
            postal_code_restaurant.distance = distance
            flash("Delivery radius updated successfully!", "success")
        else:
            # Create new record
            new_relationship = PostalCodeRestaurant(
                restaurant_id=restaurant_id,
                postal_code_id=postal_code_id,
                distance=distance
            )
            db.session.add(new_relationship)
            flash("Delivery radius set successfully!", "success")

        # Commit changes to the database
        db.session.commit()

        return redirect(url_for("set_delivery_radius_component"))

    # Render the template with the form
    attributes = {"set_delivery_radius_form": set_delivery_radius_form}
    return render_template(
        "components/admin/set_delivery_radius.html", attributes=attributes
    )

# Route
@app.route('/admin/set_delivery_radius', methods=['GET', 'POST'])
def set_delivery_radius():
    return set_delivery_radius_component()

# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't already exist
    app.run(debug=True)
