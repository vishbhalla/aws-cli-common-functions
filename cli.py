import os
import sys
import argparse

from cfn_validate import cfn_validate
from zip_and_upload_to_s3 import zip_and_upload_to_s3


def main():
    # set up argparse and parent parser
    parser = argparse.ArgumentParser(description='AWS CLI common functions')
    parent_parser = argparse.ArgumentParser(add_help=False)

    # TODO: Common options for ALL sub commands
    # Do we want to add region here?
    # May not need these...

    # parent_parser.add_argument(
    #     '-r', '--role-arn',
    #     help='The ARN of role to assume before running.'
    # )
    #
    # parent_parser.add_argument(
    #    '-m',
    #    '--mfa-token',
    #    help='The MFA token to use. Will prompt if required and not specified.'
    # )

    subparsers = parser.add_subparsers(help='sub-command --help')

    # ##################### Cloudformation validate subparser
    parser_cfn_validate = subparsers.add_parser(
        'cfn_validate',
        help='cfn_validate --help',
        parents=[parent_parser]
    )

    parser_cfn_validate.set_defaults(
        func=cfn_validate, 
        file_or_directory=os.getcwd()
    )

    parser_cfn_validate.add_argument(
        'file_or_directory',
        help=('Validate CloudFormation templates using the AWS CloudFormation '
              'validation API endpoint. A file or directory can be supplied. '
              'Default: current directory'),
        nargs='?'
    )

    # ##################### Lambda zip and upload to S3 subparser
    parser_zip_and_upload_to_s3 = subparsers.add_parser(
        'zip_and_upload_to_s3',
        help='zip_and_upload_to_s3 --help',
        parents=[parent_parser],
    )

    parser_zip_and_upload_to_s3.set_defaults(
        func=zip_and_upload_to_s3
    )

    parser_zip_and_upload_to_s3.add_argument(
        '-d',
        '--directory',
        help='A local directory containing Lambda files to Zip up and upload to S3.',
        nargs='?'
    )

    parser_zip_and_upload_to_s3.add_argument(
        '-b',
        '--s3bucket',
        help='A directory containing Lambda files which to Zip up and upload to S3.',
        nargs='?'
    )

    parser_zip_and_upload_to_s3.add_argument(
        '-k',
        '--s3key',
        help='The S3 key (path) to upload the files to.',
        nargs='?',
        default="lambda"
    )

    parser_zip_and_upload_to_s3.add_argument(
        '-x',
        '--s3extraArgs',
        help="Extra S3 arguments you may want to pass in e.g. {'ACL': 'public-read'}",
        nargs='?',
        default={}
    )

    if len(sys.argv) == 1:
        parser.print_usage()
        # parser.print_usage() # for just the usage line
        parser.exit()
    else:
        # parse the args and call whatever function was selected
        args = parser.parse_args()
        args.func(args)


# Not sure if below needed when installing as a pip:
if __name__ == '__main__':
    main()
