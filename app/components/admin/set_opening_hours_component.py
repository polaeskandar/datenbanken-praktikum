from flask import render_template, redirect, url_for, request
from app.enum.DayOfWeek import DayOfWeek
from app.form.component.admin.SetOpeningHoursForm import SetOpeningHoursForm

def set_opening_hours_component():
    days = [x.value.capitalize() for x in DayOfWeek]
    opening_hours_form = SetOpeningHoursForm()

    if request.method == "POST" and opening_hours_form.validate_on_submit():
        # Example logic: Save submitted opening hours to a database or process data
        opening_hours_data = []
        for day_entry in opening_hours_form.days.entries:
            day = day_entry.data.get("day")
            opening_time = day_entry.data.get("opening_time")
            closing_time = day_entry.data.get("closing_time")
            opening_hours_data.append({
                "day": day,
                "opening_time": opening_time,
                "closing_time": closing_time
            })

        # Simulate saving the data (replace this with actual database logic)
        print("Saved Opening Hours:", opening_hours_data)

        return redirect(url_for("admin.opening_hours"))

    attributes = {
        "days": days,
        "opening_hours_form": opening_hours_form
    }

    return render_template(
        "components/admin/set_opening_hours.html", **attributes
    )
