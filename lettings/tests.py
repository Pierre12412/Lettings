import pytest
from django.urls import reverse

from oc_lettings_site import urls
from lettings.models import Letting, Address


@pytest.mark.django_db(transaction=True)
@pytest.mark.urls(urls)
def test_lettings_index(client):
    assert 'Lettings' in str(client.get(reverse('lettings:index')).content)


@pytest.mark.django_db(transaction=False)
@pytest.mark.urls(urls)
def test_lettings_index1(client):
    address = Address(number=7217,street='Bedford Street',city='Brunswick',state='GA',zip_code=31525,country_iso_code='USA')
    address.save()
    new_one = Letting(title='Joshua Tree Green Haus /w Hot Tub',address=address)
    new_one.save()
    page = str(client.get(reverse('lettings:letting',args=[1])).content)
    first_letting = Letting.objects.filter(id=1).first()
    assert first_letting.title in page