# Installation script for AWS Cli common functions
from setuptools import setup, find_packages

setup(
    name='aws_cli_common_functions',
    version="0.0.1",
    description='AWS Cli Common Functions',
    url='https://github.com/vishbhalla/aws-cli-common-functions',
    license='Apache 2.0',
    author='Vishal Bhalla',
    author_email='v.bhalla@reply.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['boto3>=1.28.65', 'cfn-lint>=0.82.2'],
    classifiers=[
        'Development Status :: Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Topic :: Utilities',
        'Topic :: Software Development :: Build Tools'
    ],
    entry_points={
        'console_scripts': [
            'aws_cli_common_functions = cli:main'
        ]
    }
)
