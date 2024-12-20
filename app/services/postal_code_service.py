from app import db
from app.models.PostalCode import PostalCode


def get_or_create_postal_code(postal_code_data: str) -> PostalCode:
    postal_code = PostalCode.query.filter_by(postal_code=postal_code_data).first()

    if not postal_code:
        postal_code = PostalCode(postal_code=postal_code_data)
        db.session.add(postal_code)

    return postal_code
