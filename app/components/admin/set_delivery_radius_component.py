from flask import render_template, url_for, redirect

from app.form.component.admin.SetDeliveryRadiusForm import SetDeliveryRadiusForm
from app.models.PostalCode import PostalCode


def set_delivery_radius_component():
    postal_codes = PostalCode.query.all()

    restaurant_choices = [(restaurant.id, restaurant.name) for restaurant in restaurants]
    postal_code_choices = [(postal.id, postal.postal_code) for postal in postal_codes]

    set_delivery_radius_form = SetDeliveryRadiusForm()
    set_delivery_radius_form.restaurant_id.choices = restaurant_choices
    set_delivery_radius_form.postal_code.choices = postal_code_choices

    if set_delivery_radius_form.validate_on_submit():
        restaurant_id = set_delivery_radius_form.restaurant_id.data
        postal_code_id = set_delivery_radius_form.postal_code.data
        distance = set_delivery_radius_form.distance.data

        postal_code_restaurant = PostalCodeRestaurant.query.filter_by(
            restaurant_id=restaurant_id, postal_code_id=postal_code_id
        ).first()

        if postal_code_restaurant:
            postal_code_restaurant.distance = distance
            flash("Delivery radius updated successfully!", "success")
        else:
            new_relationship = PostalCodeRestaurant(
                restaurant_id=restaurant_id,
                postal_code_id=postal_code_id,
                distance=distance
            )
            db.session.add(new_relationship)
            flash("Delivery radius set successfully!", "success")

        db.session.commit()

        return redirect(url_for("set_delivery_radius_component"))

    attributes = {"set_delivery_radius_form": set_delivery_radius_form}
    return render_template(
        "components/admin/set_delivery_radius.html", attributes=attributes
    )

@app.route('/admin/set_delivery_radius', methods=['GET', 'POST'])
def set_delivery_radius():
    return set_delivery_radius_component()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
