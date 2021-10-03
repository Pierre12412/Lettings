import pytest
from django.urls import reverse
from oc_lettings_site import urls


@pytest.mark.django_db(transaction=True)
@pytest.mark.urls(urls)
def test_lettings_index(client):
    assert 'Lettings' in str(client.get(reverse('index')).content)

