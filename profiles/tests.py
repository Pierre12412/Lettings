import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from oc_lettings_site import urls
from profiles.models import Profile


@pytest.mark.django_db(transaction=True)
@pytest.mark.urls(urls)
def test_profiles_index(client):
    assert 'Profiles' in str(client.get(reverse('profiles:index')).content)

@pytest.mark.django_db(transaction=True)
@pytest.mark.urls(urls)
def test_profiles_profile(client):
    user = User(password='12345678@P',is_superuser=0,username='henry',first_name='marc',email='j@j.fr',is_staff=0,is_active=1,last_name='marc')
    user.save()
    new_one = Profile(user=user,favorite_city='Berlin')
    new_one.save()
    page = str(client.get(reverse('profiles:profile',args=['henry'])).content)
    user_db = User.objects.filter(username='henry').first()
    profile = Profile.objects.filter(user=user_db).first()
    assert user_db.first_name in page
    assert user_db.last_name in page
    assert user_db.email in page
    assert user_db.username in page
    assert profile.favorite_city in page
