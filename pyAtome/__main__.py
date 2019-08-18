import argparse
import sys
import json

from pyatome import AtomeClient


def main():
    """Main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username',
                        required=True, help='Atome username')
    parser.add_argument('-p', '--password',
                        required=True, help='Password')
    parser.add_argument('action', type=str,
                        default='live', help='Action [live/data]')
    args = parser.parse_args()

    client = AtomeClient(args.username, args.password)

    try:
        client.login()
        if args.action == 'live':
            print(json.dumps(client.get_live(), indent=2))
        else:
            print "Action not implemented. Please use 'live' as an action."

    except BaseException as exp:
        print(exp)
        return 1
    finally:
        client.close_session()

if __name__ == '__main__':
    sys.exit(main())


