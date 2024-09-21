from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# we don't want to import Product here, because it would create a circular import


# custom manager


class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(
            obj_type
        )  # dans la bdd, dans la table django_content_type, on a un enregistrement pour chaque modèle de notre application. Celui là c'est l'id 11, store, product

        # la query suivante va chercher tous les tags associés à un produit (le content_type défini ci-dessus) dont l'id est 1
        return TaggedItem.objects.select_related("tag").filter(
            content_type=content_type, object_id=obj_id
        )


# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)


class TaggedItem(models.Model):
    objects = TaggedItemManager()
    # what tag is applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # Type
    # ID
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
