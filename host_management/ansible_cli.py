import json
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import ansible.constants as C


class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """

    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """

        host = result._host
        rv = json.dumps({host.name: result._result})
#         print(json.dumps({host.name: result._result}, indent="\t"))
        return rv


def shell_cli(hosts: list, **kwargs):
    Options = namedtuple('Options',
                         ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff'])
    options = Options(connection='ssh', module_path=[], forks=10, become=None, become_method=None, become_user=None, check=False, diff=False)
    loader = DataLoader()
    passwords = dict(vault_pass='secret')
    results_callback = ResultCallback()
    inventory = InventoryManager(loader=loader, sources=hosts)
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    play_source = dict(
            name="Shell Exce",
            hosts=hosts,
            remote_user=kwargs.get('remote_user'),
            gather_facts='no',
            tasks=[
                dict(action=dict(module=kwargs.get('module'),
                                 args=kwargs.get('shell_cmd'))),
             ]
        )
    
    play = Play()
    play = play.load(play_source, variable_manager=variable_manager, loader=loader)
    tqm = None
    try:
        tqm = TaskQueueManager(
                  inventory=inventory,
                  variable_manager=variable_manager,
                  loader=loader,
                  options=options,
                passwords=passwords,
                  stdout_callback=results_callback,
              )
        rv = tqm.run(play)
    finally:
        if tqm is not None:
            tqm.cleanup()
    
        # Remove ansible tmpdir
        tmp_dir = C.DEFAULT_LOCAL_TMP
        shutil.rmtree(tmp_dir)
    return rv
