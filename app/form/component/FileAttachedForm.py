from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed


class FileAttachedForm(FlaskForm):
    def __init__(self, *args, label="File", allowed_extensions=None, **kwargs):
        super(FileAttachedForm, self).__init__(*args, **kwargs)

        self.label = label
        self.allowed_extensions = allowed_extensions
        self.file.label.text = label
        self.file.validators = [
            FileAllowed(
                allowed_extensions or ["jpg", "png"], "File format is not supported."
            )
        ]

    file = FileField("File")
