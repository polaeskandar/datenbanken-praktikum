from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms.fields.numeric import DecimalField
from wtforms.fields.simple import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError

from app.models.MenuItem import MenuItem


class MenuItemForm(FlaskForm):
    image = FileField(
        "Image",
        validators=[
            FileAllowed(["jpg", "png"]),
        ],
    )

    item_name = StringField(
        "Item's name", validators=[DataRequired(), Length(min=3, max=255)]
    )

    price = DecimalField("Price", validators=[DataRequired()])

    description = TextAreaField(
        "Description",
        validators=[DataRequired()],
        render_kw={"rows": 10},
    )

    def validate_item_name(self, item_name):
        """
        Validates the uniqueness of the item name within the same menu.
        Ensures that no other item in the same menu has the same name,
        except for the current item being edited.
        """

        item = MenuItem.query.filter_by(name=item_name.data, menu_id=current_user.restaurant.menu.id).first()


        if item is not None and (not hasattr(self, 'item_id') or item.id != self.item_id):
            raise ValidationError("Item with the same name exists in the menu.")
