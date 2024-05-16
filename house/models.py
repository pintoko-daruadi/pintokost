from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from pintokost.helpers import resize_image


def house_dir(instance, filename):
    return "house/{0}/{1}".format(instance.owner.username, filename)


class House(models.Model):
    name = models.CharField(max_length=50)
    name_lower = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=300)
    pln_number = models.CharField(max_length=20, blank=True)
    active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        limit_choices_to={'groups__name': 'owner'}
    )
    image = models.ImageField(null=True, blank=True, upload_to=house_dir)

    class Meta:
        unique_together = ('name_lower', 'owner')

    def __str__(self):
        return self.name

    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

        from django.templatetags.static import static
        return static('default.jpg')

    def save(self, *args, **kwargs):
        if self.image:
            self.image = resize_image(self.image)
        self.name_lower = self.name.lower()
        super(House, self).save(*args, **kwargs)

    def soft_delete(self):
        self.active = False
        self.deleted_at = timezone.now()
        self.save()

    def is_currently_rented(self):
        from rent.models import Rent
        is_exists = Rent.objects.filter(house=self, active=True).exists()
        return is_exists

    def get_current_rent(self):
        from rent.models import Rent
        profile = Rent.objects.get(house=self, active=True)
        return profile
