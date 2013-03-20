from django.db import models
from spares.sites.models import WebSite


class Dealer(models.Model):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    address = models.TextField()
    comment = models.TextField()
    phone = models.CharField(max_length=50)
    fax = models.CharField(max_length=50)
    webSite = models.ForeignKey(WebSite)

    def __unicode__(self):
        return self.name

    def _get_url(self):
        return u'/dealers/%s/' % self.code

    url = property(_get_url)