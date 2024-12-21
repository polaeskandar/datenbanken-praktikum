from flask import render_template, redirect, url_for, Response

from app.enum.DayOfWeek import DayOfWeek
from app.form.component.admin.SetOpeningHoursForm import SetOpeningHoursForm


def set_opening_hours_component() -> str | Response:
    days = [x.value.capitalize() for x in DayOfWeek]
    opening_hours_form = SetOpeningHoursForm()

    if opening_hours_form.validate_on_submit():
        # raise Exception(len(opening_hours_form.days.entries))
        return redirect(url_for("admin.opening_hours"))

    attributes = {"days": days, "opening_hours_form": opening_hours_form}

    return render_template(
        "components/admin/set_opening_hours.html", attributes=attributes
    )
