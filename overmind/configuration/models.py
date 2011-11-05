from django.db import models

from provisioning.models import Node


class Deployment(models.Model):
    """ A record of a single deployment against a single server """

    node = models.ForeignKey(Node, related_name='deployments')
    """ The server that this deployment happened (or is happening) to """

    start_date = models.DateField(auto_now_add=True)
    """ The date and time a deployment started. As this record won't exist
    until a deployment is underway this will never be NULL. The default value
    is the return value of datetime.datetime.now() """

    finish_date = models.DateField(blank=True, null=True)
    """ The date and time a deployment finished. NULL if the deployment is
    still in progress """

    result = models.IntegerField(default=-1)
    """ The state of the deployment. -1 indicates still in progress, otherwise
    it is the exit code of a remote Yaybu process. 0 indicates success. """


class LogLine(models.Model):
    """ A single line of log from a deployment """

    deployment = models.ForeignKey(Deployment, related_name='lines')
    """ The deployment that this log entry is for """

    line = models.CharField(max_length=255)
    """ The line of test """

