import datetime
from celery.task import task
from models import Node, Deployment

from plugins import load_plugins


@task
def deploy(hostname):
    """
    Actually do a deployment to a host.

    :param hostname: The remote computer to deploy to.
    :type hostname: str.
    :returns: int -- the return code of the remote yaybu process

    This method really just creates and finalizes the deployment tracking
    record and figures out which config management backend to use.
    """

    node = Node.objects.get(name=hostname)

    # Record that a deployment against a node has started
    d = Deployment(node=node)
    d.save()

    try:
        rv = load_plugins()["yaybu"]().deploy(d)
    except:
        #FIXME: Capture and log any unhandle exceptions
        rv = 256

    # Update the deployment table to show we are finished
    d.finish_date = datetime.datetime.now()
    d.result = rv
    d.save()

    return rv

