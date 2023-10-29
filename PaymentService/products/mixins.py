from django.http import Http404


class CheckForObjectOwnerMixin:
    def get_object(self, queryset=None):
        object = super().get_object(queryset)

        if object.user != self.request.user:
            raise Http404("You don't have permission to do this.")

        return object
