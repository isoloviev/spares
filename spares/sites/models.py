from django.db import models

# Create your models here.
class WebSite(models.Model):
    name = models.CharField(max_length=200)
    domain = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.domain)