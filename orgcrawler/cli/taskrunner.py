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
@click.option('--readwrite-role', '-r',
    help='IAM role to assume for executing write actions in accounts.'
)
@click.option('--task-spec-file', '-f',
    required=True,
    default='~/.aws/orgcrawler/task-spec.yaml',
    show_default=True,
    type=click.File('r'),
    help='Path to file containing orgcrawler task specifications.'
)
@click.option('--exec', 'execute',
    is_flag=True,
    help='If unset, all tasks will execute in "DryRun" mode.',
)
def main(readwrite_role, task_spec_file, execute):
    '''
    Usage:

      taskrunner -f /path/to/task-spec.yaml

      taskrunner -f /path/to/task-spec.yaml -r MyIamRole --exec

    '''
    #print('readwrite_role:', readwrite_role)
    #print('task_spec_file:', task_spec_file)
    #print('execute:', execute)
    task_spec = tasks.validate_task_spec(task_spec_file)
    #print(yamlfmt(task_spec))
    org_access_role = task_spec['readonly_role']
    master_account_id = tasks.validate_master_account_id(
        org_access_role,
        task_spec['master_account_id'],
    )

    org = orgcrawler.orgs.Org(master_account_id, org_access_role)
    org.load()

    for task in task_spec['tasks']:

        kwargs = task.get('kwargs', dict())
        kwargs['dryrun'] = not execute
        #print('kwargs:\n{}'.format(yamlfmt(kwargs)))

        crawler = orgcrawler.crawlers.Crawler(
            org,
            access_role=readwrite_role, 
            regions=task['regions'],
            accounts=task['accounts'],
        )
        crawler.load_account_credentials()
        payload = get_payload_function_from_string(task['payload'])
        execution = crawler.execute(payload, list(), kwargs)
        click.echo(jsonfmt(execution.dump()))
