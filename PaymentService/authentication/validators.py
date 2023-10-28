from django.core.validators import ValidationError
from django.contrib.auth import get_user_model

UserModel = get_user_model()


def validate_customer_name_length(name):
    name_length = len(name.split())
    if name_length != 2:
        raise ValidationError("You have to enter your first and last name.")


def validate_customer_name_for_only_letters(name):
    only_letters = all([x.isalpha() or x == " " for x in name])
    if not only_letters:
        raise ValidationError("Your name must contain only letters.")


def validate_business_name_for_distinctiveness(name):
    business_name_already_exists = UserModel.objects.filter(name__iexact=name).exists()
    if business_name_already_exists:
        raise ValidationError("A business with this name already exists.")
