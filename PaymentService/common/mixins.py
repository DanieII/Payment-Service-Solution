from django import forms
from django.shortcuts import redirect


class AddPlaceholdersToFieldMixin:
    placeholders = {}

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super().get_form(form_class)

        for field_name, placeholder in self.placeholders.items():
            try:
                form.fields[field_name].widget = forms.TextInput(
                    attrs={"placeholder": placeholder}
                )
            except KeyError:
                pass

        return form


class ProhibitBusinessUsersMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_business:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)


class ProhibitCustomerUsersMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_business:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
