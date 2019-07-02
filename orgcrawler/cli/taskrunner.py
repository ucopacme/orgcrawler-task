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
@click.option('--write-access-role', '-r',
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
def main(write_access_role, task_spec_file, execute):
    '''
    Usage:

      taskrunner -r MyIamRole -f /path/to/task-spec.yaml
      taskrunner -r MyIamRole -f /path/to/task-spec.yaml --exec

    '''
    print(write_access_role)
    print(task_spec_file)
    print(execute)

    task_spec = tasks.validate_task_spec(task_spec_file)
    org_access_role = task_spec['readonly_role']
    account_access_role = None
    master_account_id = tasks.validate_master_account_id(
        org_access_role,
        task_spec['master_account_id'],
    )
    #print(yamlfmt(task_spec))

    org = orgcrawler.orgs.Org(master_account_id, org_access_role)
    org.load()

    for task in task_spec['tasks']:
        if not task['readonly'] and execute:
            account_access_role = write_access_role
        crawler = orgcrawler.crawlers.Crawler(
            org,
            access_role=account_access_role, 
            regions=task['regions'],
            accounts=task['accounts'],
        )
        #print(yamlfmt(task))
        #crawler.update_regions(task['regions'])
        #crawler.update_accounts(task['accounts'])
        #print(crawler.get_regions())
        payload = get_payload_function_from_string(task['payload'])

        if not task['readonly']:
            task['data']['dryrun'] = not execute
        if task['data'] is not None:
            print(yamlfmt(task['data']))
            execution = crawler.execute(payload, task['data'])
        else:
            execution = crawler.execute(payload)
            pass
        print(yamlfmt(execution.dump()))
