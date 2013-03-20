from django.db import models
from spares.sites.models import WebSite


# News items
class News(models.Model):
    title = models.CharField(max_length=200)
    annotation = models.TextField()
    content = models.TextField()
    pubDate = models.DateTimeField('Date Published')
    webSite = models.ForeignKey(WebSite)

    def __unicode__(self):
        return self.title