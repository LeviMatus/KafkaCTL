from constants.constants import SchemaRegistryHosts


def handle_registry(args: dict):
    with open('registered-schemas.txt') as f:
        topics = f.readlines()
        topics = [topic.strip() for topic in topics]

    """ 
    Options is the parameter options to use for the HTTP request to be issued in pyfluent.py
    """
    options = {
        'url': 'http://{host}:{port}/config/'
            .format(host=SchemaRegistryHosts().dict()[args.get('env', ['localhost'])[0]], port=args.get('p', 8081)),
        'headers': {
            'Accept': 'application/vnd.schemaregistry.v1+json, application/vnd.schemaregistry+json, application/json',
            'Content-Type': 'application/vnd.schemaregistry.v1+json'
        },
        'payload': '\"compatibility\": \"{comp_level}\"'.format(comp_level=args.get('compatibility', 'BACKWARD')[0])
    }

    options['payload'] = '{' + options['payload'] + '}'

    commands = []

    for topic in topics:
        options['url'] = options['url'] + '{topic}'.format(topic=topic)
        commands.append(options)

    return commands
