from .models import Organisation
import django_filters

class OrganisationFilter(django_filters.FilterSet):
    class Meta:
        model = Organisation
        fields = ['division', 'district', 'thana', 'name' ]