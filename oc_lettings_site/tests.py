import pytest
from django.urls import reverse

from oc_lettings_site import urls


@pytest.mark.django_db(transaction=True)
@pytest.mark.urls(urls)
def test_site_index(client):
    assert 'Welcome to Holiday Homes' in str(client.get(reverse('index')).content)
