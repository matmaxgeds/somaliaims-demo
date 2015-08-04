import django_filters
from data_entry.models import Project


class ProjectFilter(django_filters.FilterSet):

    class Meta:
        model = Project
        fields = {'value': ['lt', 'gt'],
                  'name': ['icontains'],
                  'startDate': ['gt'],
                  'endDate': ['lt'],
                  'funders': ['icontains'],
                  'implementers': ['icontains'],

        }
