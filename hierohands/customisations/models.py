import re
from digipal import models

# change the label of the table in the admin interface


def set_verbose_name(model, singular, plural=None):
    model._meta.verbose_name = singular
    model._meta.verbose_name_plural = plural or (singular + 's')


set_verbose_name(models.Place, 'City', 'Cities')
set_verbose_name(models.Repository, 'Tomb')
# set_verbose_name(models.CurrentItem, 'Chamber')
set_verbose_name(models.ItemPart, 'Wall')
set_verbose_name(models.Image, 'Decorum Section')

