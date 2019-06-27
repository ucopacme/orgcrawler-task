AWS Organization configuration engine based on OrgCrawler
=========================================================



TODO:

- DONE add master_account_id to task_spec
- validate task_spec using cerebus
- add logger facility
  - can this just use orgcrawler logger?
- add support for dryrun vs. exec
- Crawler.execute must rely on kwargs
  - what to do when task['data'] is not defined?
- support in orgcrawler for update_accounts():
  - Crawler.accounts is just a list of account names
  - Crawler.load_account_credentials checks if credentials exist in an account before
    loading.  eventually, most all account credentials will be set.
- support in orgcrawler for excluded accounts or regions
- add ability to generate account lists using OU
- allow `ALL` keyword to accounts/regions in task_spec
- default is None for accounts/regions in task_spec
- support default_regions in task_spec





TODO maybe:

- make a Task object:
  what would this do for me:
  - help with logging
  - error handling
  - 
- add config file for user executing task-runner
  - set org_access_role, account_access_role
- Payload modules?:
  - define thier own data validation
