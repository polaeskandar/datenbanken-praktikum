import os
import random
import string

from flask import request
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename

from app import app
from app.form.FileAttachedForm import FileAttachedForm


def upload_file(
    form: FileAttachedForm,
    upload_directory: str = None,
) -> str | None:
    try:
        return upload_required_file(form, upload_directory)
    except BadRequest:
        return None


def upload_required_file(
    form: FileAttachedForm,
    upload_directory: str = None,
    err: str = "File has to be provided.",
) -> str | None:
    # Default the upload directory to the app's configuration
    upload_directory = upload_directory or app.config.get("UPLOAD_DIRECTORY", "uploads")

    # Ensure the file exists in the request
    if not form.file.name in request.files:
        raise BadRequest(err)

    file = request.files[form.file.name]

    # Ensure a file was provided
    if not file or file.filename == "":
        raise BadRequest(err)

    # Use secure_filename to sanitize the original filename
    original_filename = secure_filename(file.filename)
    file_extension = os.path.splitext(original_filename)[1].lower().lstrip(".")

    # Check if the file extension is allowed
    if file_extension not in form.allowed_extensions:
        raise BadRequest(f"File type '{file_extension}' is not allowed.")

    # Create the upload directory if it does not exist
    os.makedirs(upload_directory, exist_ok=True)

    # Generate a unique filename
    unique_filename = f"{''.join(random.choices(string.ascii_uppercase + string.digits, k=32))}.{file_extension}"
    file_path = os.path.join(upload_directory, unique_filename)

    # Save the file
    file.save(file_path)

    return unique_filename
