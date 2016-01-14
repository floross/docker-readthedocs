import os
import config
from django.contrib.auth.models import User

try:
    User.objects.create_superuser(
        config.ADMIN_USERNAME,
        config.ADMIN_EMAIL,
        config.ADMIN_PASSWORD
    )
    print "Created {0} superuser".format(config.ADMIN_USERNAME)
except:
    print "Failed to create {0} user".format(config.ADMIN_USERNAME)

try:
    slumber = User.objects.create(
        username=config.SLUMBER_USERNAME,
        email=config.SLUMBER_EMAIL,
        is_staff=True,
        is_active=True
    )

    slumber.set_password(config.SLUMBER_PASSWORD)

    slumber.save()

    print "Created {0} user".format(config.SLUMBER_USERNAME)
except:
    print "Failed to create {0} user".format(config.SLUMBER_USERNAME)

