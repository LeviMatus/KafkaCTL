from constants.constants import ZookeeperHosts, TopicConfigs


def handle_zookeeper(args: dict):
    with open('topics-to-configure.txt') as f:
        topics = f.readlines()
        topics = [topic.strip() for topic in topics]

    host = ZookeeperHosts().dict()[args.get('env', ['localhost'])[0]]
    commands = []

    if [cmd for cmd in ["delete", "partitions"] if cmd in args.keys()]:
        base = "kafka-topics --zookeeper {host}:{p}".format(host=host, p=args.get('p', 2181))
        alterations = None
        if args.get("delete", None):
            base += " --delete --topic"

        elif args.get("partitions", None):
            base += " --alter"
            alterations = " --partitions {p}".format(p=args.get("partitions"))

        for topic in topics:
            command = base + " --topic {topic}".format(topic=topic)
            if alterations:
                command += alterations
            commands.append(command)

    else:
        CONFIG_OPS = TopicConfigs()
        base = "kafka-configs --zookeeper {host}:{port} --alter --entity-type topics"\
            .format(host=host, port=args.get('p', 2181))

        configs_to_add = []
        configs_to_delete = []

        for key in {k: v for k, v in args.items() if k not in ['host', 'env']}.keys():
            config = CONFIG_OPS.dict()[str(key).upper()]
            if args[key][0] == 'set':
                configs_to_add.append('{config}={value}'.format(config=config, value=args[key][1]))
            elif args[key][0] == 'delete':
                configs_to_delete.append('{config}'.format(config=config))

        for topic in topics:

            command = base + " --entity-name {topic}".format(topic=topic)

            if len(configs_to_add) > 0:
                command += ' {operation} {configs}'.format(operation=CONFIG_OPS.SET, configs=','.join([str(x) for x in configs_to_add]))

            if len(configs_to_delete) > 0:
                command += ' {operation} {configs}'.format(operation=CONFIG_OPS.DELETE, configs=','.join([str(x) for x in configs_to_delete]))

            commands.append(command)

    return commands
