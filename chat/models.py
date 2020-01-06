import logging
from django.db import models
from django.core import exceptions

logger = logging.getLogger(__name__)


# Create your models here.
class GetInstanceMixin(object):
    def get_or_none(self, **kwargs):
        """Extends get to return None if no object is found based on query."""
        try:
            logger.debug(
                "Getting instance for %s with %s" % (self.model, kwargs))
            instance = self.values().get(**kwargs)
            logger.info(
                "Got instance primary_key=%s for %s" % (instance.pk, self.model))
            return instance
        except exceptions.ObjectDoesNotExist:
            logger.warning(
                "No instance found for %s with %s" % (self.model, kwargs))
            return None


class DefaultModelManager(GetInstanceMixin, models.Manager):
    pass


class TimeStampedModel(models.Model):

    class Meta(object):
        abstract = True
    cdate = models.DateTimeField(auto_now_add=True)
    udate = models.DateTimeField(auto_now=True)
    objects = DefaultModelManager()

    def save(self, *args, **kwargs):
        #no need to worry about instance.save(update_fields=['udate'])
        #we handle that automatically
        if kwargs and kwargs.get('update_fields'):
            if 'udate' not in kwargs['update_fields']:
                kwargs['update_fields'].append("udate")
        super(TimeStampedModel, self).save(*args, **kwargs)


class Broadcast(TimeStampedModel):
    id = models.AutoField(db_column='broadcast_id', primary_key=True)
    message = models.TextField(blank=True, null=True)