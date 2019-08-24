import argparse
import sys
import json
import logging

from pyAtome import AtomeClient


def main():
    """Main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username',
                        required=True, help='Atome username')
    parser.add_argument('-p', '--password',
                        required=True, help='Password')
    parser.add_argument('--debug', action='store_true', help='Print debug messages to stderr')
    parser.add_argument('action', type=str,
                        default='live', help='Action [live/data]')
    args = parser.parse_args()

    client = AtomeClient(args.username, args.password)

    try:
        if args.debug:
            # You must initialize logging, otherwise you'll not see debug output.
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True



        client.login()
        if args.action == 'live':
            print(json.dumps(client.get_live(), indent=2))
        else:
            print("Action not implemented. Please use 'live' as an action.")

    except BaseException as exp:
        print(exp)
        return 1
    finally:
        client.close_session()

if __name__ == '__main__':
    sys.exit(main())


