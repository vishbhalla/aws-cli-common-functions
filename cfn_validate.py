import os
import sys
import boto3
from botocore.exceptions import ClientError


def cfn_validate(args, out=sys.stdout):
    """Entry point for Cloudformation Validate.
    Default behaviour is to validate ALL C.F. templates under current path

    :param args: argparser args object
    :param out: output stream
    """
    v = Validator()

    if os.path.isfile(args.file_or_directory):
        v.validate_template(args.file_or_directory)
    elif os.path.isdir(args.file_or_directory):
        v.validate_templates_in_directory(args.file_or_directory)
    else:
        out.write(
            'ERROR: Argument specified is not a file or a directory...exiting...')
        sys.exit(1)


class Validator:
    """A Class to validate CloudFormation yaml template

    Usage example:
    v = Validator()
    v.validate_templates_in_directory('.')
    v.validate_template('/tmp/modules/vpc/vpc.template')
    """

    def __init__(self):
        self.client = boto3.client('cloudformation')
        # Files to exclude:
        self.excluded_files = ['example.template']

    def template_files(self, path):
        """Find all .template files in the given path.

        :param path: Base path for search
        :type path: string
        """
        template_files = []

        for root, dirs, files in os.walk(path):
            # Ignore hidden files and directories
            files = [f for f in files if not f[0] == '.']
            dirs[:] = [d for d in dirs if not d[0] == '.']

            template_files.extend(
                [os.path.join(root, name)
                 for name in files
                 if '.template' in name
                 and name not in self.excluded_files
                 ]
            )

        return template_files

    def validate_template(self, template_file, out=sys.stdout):
        """Validate a single template.

        :param template_file: The file to validate
        :type template_file: string
        :param out: output stream
        """
        out.write('Validating template: ' + template_file + '\n')
        template_body = open(template_file).read()
        try:
            self.client.validate_template(TemplateBody=template_body)
        except ClientError as e:
            out.write(str(e) + '\n')
            raise

    def validate_templates_in_directory(self, path):
        """Validate all yml files under a path

        :param path: The path to validate all yaml files under
        """
        for template_file in self.template_files(path):
            try:
                self.validate_template(template_file)
            except ClientError as e:
                continue
        if 'e' in locals():
            sys.exit(1)
