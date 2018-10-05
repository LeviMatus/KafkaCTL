import argparse
import sys
import time
import requests
from subprocess import call
from registry import registry
from zookeeper import zookeeper
from termcolor import colored


def main(args: dict):

    CONFIRMATION_STRING = 'YES'

    commands = []

    is_prod_command = args['env'][0] == 'PROD'

    if is_prod_command:
        print(colored("WARNING!", 'red'), "You are about to configure a", colored("PRODUCTION", "red"), "environment!")
        if prompt_for_confirmation(CONFIRMATION_STRING) != CONFIRMATION_STRING:
            abort()

    if host_is_zookeeper(args):
        commands = zookeeper.handle_zookeeper(args)
    elif host_is_schema_registry(args):
        commands = registry.handle_registry(args)

    if is_prod_command:
        print('\n', colored("****WARNING****", 'red'), '\nYou are about to make the following changes to', colored("PRODUCTION", "red"))
        display_pending_changes(commands)
        if prompt_for_confirmation(CONFIRMATION_STRING) != CONFIRMATION_STRING:
            abort()

    for command in commands:
        if host_is_schema_registry(args):
            res = requests.put(command['url'], data=command['payload'], headers=command['headers'])
            print(colored(command['url'], 'blue' if res.status_code == 200 else 'red'))
        elif host_is_zookeeper(args):
            call(command.split())
        time.sleep(1)

    print("\n", colored('FINISHED', 'green'), "\n")


def abort():
    print(colored("Script Aborted!", 'blue'))
    sys.exit()


def prompt_for_confirmation(conf_string):
    return input("Enter {conf} to continue...".format(conf=conf_string))


def display_pending_changes(commands: list):
    for command in commands:
        print(colored(command, 'yellow'))


def host_is_zookeeper(args: dict) -> bool:
    return args.get('host', [None])[0] == 'zookeeper'


def host_is_schema_registry(args: dict) -> bool:
    return args.get('host', [None])[0] == 'schema-registry'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Swiss Army Knife.")

    """ Host connection configuration """
    parser.add_argument('--host', nargs=1, type=str, choices=['zookeeper', 'schema-registry'],
                        help="zookeeper or schema-registry", required=True)
    parser.add_argument('--env', nargs=1, type=str, choices=['DEV', 'QA', 'PROD'],
                        help="Choose DEV, QA, or PROD to affect", required=True)
    parser.add_argument('-p', nargs=1, type=int, help="Enter the target port number", required=False)

    """ Compatibility and Schema Registry """
    parser.add_argument('--compatibility', type=str, nargs=1, help="BACKWARD or NONE")

    """ Zookeeper """
    parser.add_argument('--delete', action='store_true', help="will delete topics")
    parser.add_argument('--retention_ms', nargs='*', help="set 1000 or delete")
    parser.add_argument('--cleanup_policy', nargs='*', help="set compact or delete")
    parser.add_argument('--compaction_time', nargs='*', help="set <num> or delete")
    parser.add_argument('--partitions', nargs='?', type=int, help="set <num>")

    args = vars(parser.parse_args(sys.argv[1:]))

    options = {k: v for k, v in args.items() if v is not None and (v if k == 'delete' else True)}

    main(args=options)
