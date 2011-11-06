from django.conf import settings

from yaybu.core.change import ChangeLog, ResourceFormatter
from yaybu.core.remote import RemoteRunner
from yaybu.core.runcontext import RunContext

from models import LogLine


class OvermindChangeLog(ChangeLog):

    """
    This class overrides log handling so Overmind can redirect log lines to the database
    """

    def configure_session_logging(self):
        """ Normally this is where yaybu would set up logging to stdout - stop
        that. This is actually a good place to set up a formatter to deal with
        logging info capture in ``handle`` """
        self.formatter = ResourceFormatter("%(message)s")

    def configure_audit_logging(self):
        """ Under some circumstances Yaybu will try to log to syslog - by
        overriding this method to do nothing we stop that """
        pass

    def handle(self, record):
        """
        This method gets called by the logging machinery every time a new
        log-line is received from the yaybu process running remotely.

        :param record: Raw data as passed around by the ``logging`` module internally.
        :type record: dict.
        """
        ChangeLog.handle(self, record)

        for line in self.formatter.format(record).splitlines():
            l = LogLine(deployment=self.ctx.deployment, line=line)
            l.save()


class OvermindContext(RunContext):

    def __init__(self, configfile, opts, deployment):
        """
        :param opts: Options to pass to Yaybu
        :param deployment: The deployment database record
        :type deployment: models.Deployment
        """
        super(OvermindContext, self).__init__(configfile, opts)
        self.deployment = deployment

    def setup_changelog(self):
        """ Setup a custom overmind-specific changelog handler """
        self.changelog = OvermindChangeLog(self)


class Driver(object):

    display_name = "Yaybu"

    def deploy(deployment, config=settings.DEPLOY_FILE):
        """
        Actually do a deployment to a host using Yaybu.
    
        :param deployment: A deploy record to track the deployment status
        :type deployment: overmind.configuration.models.Deployment
        :param conf: The path to a configuration to deploy
        :type conf: str
        :returns: int -- the return code of the remote yaybu process
    
        We use the RemoteRunner API to actually establishes an SSH connection to
        the target computer and initiate a deployment.
    
        Because the Yay config is parsed from within Django it can use the
        ``djangostore`` data binding API to access service metadata directly in the
        database.
        """
    
        node = deployment.node
    
        # The bulk of the parameters to the RunContext object would normally come
        # from an OptionParser, in the absence of a proper API we just provide an
        # object with attributes with the correct settings on.
        class opts:
            log_level = "info"
            logfile = "-"
            host = "%s@%s" % (node.username or "root", note.hostname)
            user = "root"
            ypath = []
            simulate = False
            verbose = False
            resume = True
            no_resume = False
            env_passthrough = []
    
        ctx = OvermindContext(config, opts, d)
    
        r = RemoteRunner()
        r.set_interactive(False)
        r.set_identity_file(settings.DEPLOY_SSH_KEY)
        r.set_missing_host_key_policy("no")
        r.load_host_keys(settings.DEPLOY_SSH_KNOWN_HOSTS)
        rv = r.run(ctx)
    
        return rv
    
