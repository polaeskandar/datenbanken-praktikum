from datetime import datetime

from flask import render_template, redirect, url_for, Response, flash
from flask_login import current_user

from app import db
from app.enum.DayOfWeek import DayOfWeek
from app.form.admin.SetOpeningHoursForm import SetOpeningHoursForm
from app.models.OpeningHour import OpeningHour
from app.models.Restaurant import Restaurant
from app.services.component_service import flash_errors


def set_opening_hours_component() -> str | Response:
    days = [x.value.capitalize() for x in DayOfWeek]
    opening_hours_form = SetOpeningHoursForm()

    if opening_hours_form.validate_on_submit():
        return set_opening_hours(opening_hours_form, current_user.restaurant)

    populate_form_from_db(opening_hours_form, current_user.restaurant)
    flash_errors(opening_hours_form)

    attributes = {"days": days, "opening_hours_form": opening_hours_form}

    return render_template(
        "components/admin/set_opening_hours.html", attributes=attributes
    )


def populate_form_from_db(opening_hours_form, restaurant):
    opening_hours_by_day = {oh.day_of_week.value: oh for oh in restaurant.opening_hours}

    for i, day_form in enumerate(opening_hours_form.days):
        day_enum = list(DayOfWeek)[i]
        opening_hour_record = opening_hours_by_day.get(day_enum.value)

        if opening_hour_record:
            # Convert the DB string "HH:MM" -> datetime.time
            day_form.opening_hour.data = datetime.strptime(
                opening_hour_record.opening_time, "%H:%M"
            ).time()  # => datetime.time(9, 0), for example

            day_form.closing_hour.data = datetime.strptime(
                opening_hour_record.closing_time, "%H:%M"
            ).time()
        else:
            # Provide default times
            day_form.opening_hour.data = datetime.strptime("09:00", "%H:%M").time()
            day_form.closing_hour.data = datetime.strptime("17:00", "%H:%M").time()


def set_opening_hours(
    opening_hours_form: SetOpeningHoursForm, restaurant: Restaurant
) -> Response:
    opening_hours_by_day = {oh.day_of_week.value: oh for oh in restaurant.opening_hours}

    for i, day_form in enumerate(opening_hours_form.days):
        day_enum = list(DayOfWeek)[i]
        existing_opening_hour = opening_hours_by_day.get(day_enum.value)

        opening_str = day_form.opening_hour.data.strftime("%H:%M")
        closing_str = day_form.closing_hour.data.strftime("%H:%M")

        if existing_opening_hour:
            existing_opening_hour.opening_time = opening_str
            existing_opening_hour.closing_time = closing_str
        else:
            new_opening_hour = OpeningHour(
                day_of_week=day_enum,
                opening_time=opening_str,
                closing_time=closing_str,
                restaurant_id=restaurant.id,
            )

            db.session.add(new_opening_hour)

    db.session.commit()
    flash("Opening hours set successfully.", "success")

    return redirect(url_for("admin.opening_hours"))
