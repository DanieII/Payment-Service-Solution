from django import forms


class AddPlaceholdersToFieldMixin:
    placeholders = {}

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super().get_form(form_class)

        for field_name in form.fields.keys():
            current_field = form.fields[field_name]
            try:
                current_field.widget = forms.TextInput(
                    attrs={"placeholder": self.placeholders[field_name]}
                )
            except KeyError:
                pass

        return form
