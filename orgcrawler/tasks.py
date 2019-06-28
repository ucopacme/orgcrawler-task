import yaml
import orgcrawler


def validate_master_account_id(role, given_id):
    master_account_id = orgcrawler.utils.get_master_account_id(role)
    if not str(given_id) == master_account_id:
        raise RuntimeError(
            "The Organization Master Account Id '{}' does not match the "
            "'master_account_id' set in your task-spec-file".format(master_account_id)
        )
    return master_account_id


def validate_task_spec(task_spec_file):
    task_spec = yaml.safe_load(task_spec_file.read())
    # validations goes here...
    return task_spec
