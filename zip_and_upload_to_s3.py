import os
import shutil
import sys
import boto3
from botocore.exceptions import ClientError


def zip_and_upload_to_s3(args, out=sys.stdout):
    """Entry point for - Zip lambdas and upload to S3.

    :param args: argparse args object
    :param out: output stream
    """
    z = ZipAndUploadToS3()

    if os.path.isdir(args.directory):
        z.upload_to_s3(
            # z.zip(args.filename, args.directory),
            z.zip(args.directory),
            args.s3bucket,
            args.s3key + "/" + get_file_name_from_path(args.directory) + ".zip",
            args.s3extraArgs
        )
    else:
        out.write('ERROR: Argument specified is not a directory. Exiting...')
        sys.exit(1)


def get_file_name_from_path(file_path):
    file_path_components = file_path.split('/')
    file_name_and_extension = file_path_components[-1]
    return file_name_and_extension


class ZipAndUploadToS3:

    def __init__(self):
        self.client = boto3.client('s3')

    @staticmethod
    def zip(directory, out=sys.stdout):
        """Zip files in a given directory

        :param directory: The path where our files to Zip live
        :param out: output stream
        """
        # Use the directory name as the filename for the Zip file
        filename = get_file_name_from_path(directory)

        # Remove any existing Zip files
        if os.path.exists(directory + '/' + filename + '.zip'):
            out.write('Removing existing zipfile: ' + directory + '/' + filename + '.zip\n')
            os.remove(directory + '/' + filename + '.zip')

        # Create the ZIP file
        zipfile = shutil.make_archive(
            directory + '/' + filename,
            'zip',
            directory
        )

        out.write('Zip file created: ' + zipfile + '\n')

        return zipfile

    def upload_to_s3(self, file, s3_bucket, key, extra_args, out=sys.stdout):
        """Upload zip file to S3

        :param file: The full local path if the file to upload to S3
        :param s3_bucket: The S3 bucket to upload the file to
        :param key: The key (path) in S3 to upload the file to
        :param extra_args: Extra S3 arguments you may want to pass in e.g. {'ACL': 'public-read'}
        :param out: output stream
        """

        try:
            self.client.upload_file(
                file,
                s3_bucket,
                key,
                ExtraArgs=extra_args
            )
        except ClientError as e:
            out.write(str(e) + '\n')
            raise

        out.write('Zip file uploaded to: s3://' + s3_bucket + '/' + key + '\n')
