import factory
from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = Profile
    user = factory.SubFactory('accounts.factories.UserFactory', profile=None)


@factory.django.mute_signals(post_save)
class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', raw_password='password123')

    profile = factory.RelatedFactory(ProfileFactory, 'user')

