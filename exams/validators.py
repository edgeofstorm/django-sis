from django.core.validators import ValidationError
import os


def validate_file_extension(value):
    ext = os.path.splitext(value)[1]
    valid_exts=['.pdf','.xls','.xlsx','.docx','.doc']
    if not ext.lower() in valid_exts:
        raise ValidationError('unsupported file extension')