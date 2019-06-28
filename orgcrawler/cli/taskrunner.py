#!/usr/bin/env python

import os
import sys
import json

import yaml
import click
import boto3
from botocore.exceptions import ClientError

import orgcrawler
from orgcrawler.utils import jsonfmt, yamlfmt
from orgcrawler.cli.utils import (
    get_payload_function_from_string,
)

from orgcrawler import tasks


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--master-role', '-r',
    required=True,
    help='IAM role to assume for accessing AWS Organization Master account.'
)
@click.option('--task-spec-file', '-f',
    required=True,
    default='~/.aws/orgcrawler/task-spec.yaml',
    show_default=True,
    type=click.File('r'),
    help='Path to file containing orgcrawler task specifications.'
)
def main(master_role, task_spec_file):
    '''
    Usage:

      task-runner -r MyIamRole -f /path/to/task-spec.yaml

    '''
    print(master_role)
    print(task_spec_file)

    task_spec = tasks.validate_task_spec(task_spec_file)
    master_account_id = tasks.validate_master_account_id(
        master_role,
        task_spec['master_account_id'],
    )
    print(yamlfmt(task_spec))

    org = orgcrawler.orgs.Org(master_account_id, master_role)
    org.load()
    crawler = orgcrawler.crawlers.Crawler(org)

    for task in task_spec['tasks']:
        crawler.update_regions(task['regions'])
        crawler.update_accounts(task['accounts'])
        print(crawler.get_regions())
        payload = get_payload_function_from_string(task['payload'])
        if task['data'] is not None:
            print(yamlfmt(task['data']))
            execution = crawler.execute(payload, task['data'])
        else:
            execution = crawler.execute(payload)
        print(yamlfmt(execution.dump()))

