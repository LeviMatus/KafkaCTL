class ConstantDict(object):
    """an Enumeration class"""
    _dict = None

    @classmethod
    def dict(cls):
        """Dictionary of all uppper-case constants."""
        if cls._dict is None:
            val = lambda x: getattr(cls, x)
            cls._dict = dict(((c, val(c)) for c in dir(cls) if c == c.upper()))
        return cls._dict

    def __contains__(self, value):
        return value in self.dict().values()

    def __iter__(self):
        for value in self.dict().values():
            yield value


class SchemaRegistryHosts(ConstantDict):
    """Schema Registry Hosts by Env"""
    DEV = ''     # localhost, for instance
    QA = ''      # hostname only
    PROD = ''    # hostname only


class ZookeeperHosts(ConstantDict):
    """Zookeeper Hosts by Env"""
    DEV = ''        # localhost, for instance
    QA = ''         # host name only
    PROD = ''       # host name only


class CompatibilityLevels(ConstantDict):
    """Supported Compatibility Levels"""
    NONE = 'NONE'
    BACKWARD = 'BACKWARD'


class TopicConfigs(ConstantDict):
    """Supported Kafka Topic Configurations"""
    """ This enum defines what we expect our command options to evaluate to """
    SET = '--add-config'
    DELETE = '--delete-config'
    RETENTION_MS = 'retention.ms'
    CLEANUP_POLICY = 'cleanup.policy'
    COMPACTION_TIME = 'min.compaction.lag.ms'