from flask import render_template

from app.enum.DayOfWeek import DayOfWeek
from app.form.component.admin.OpeningHoursForm import OpeningHoursForm


def opening_times_component():
    days = [x.value.capitalize() for x in DayOfWeek]
    opening_hours_form = OpeningHoursForm()

    if opening_hours_form.validate_on_submit():
        # raise Exception(len(opening_hours_form.days.entries))
        pass

    attributes = {"days": days, "opening_hours_form": opening_hours_form}

    return render_template("components/admin/opening_times.html", attributes=attributes)
