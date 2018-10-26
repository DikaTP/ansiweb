import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase

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
        print(json.dumps({host.name: result._result}, indent=4))

Options=namedtuple('Options',['connection', 'module_path', 'forks', 'become', 'become_method',
                            'become_user', 'check', 'diff'])

loader=DataLoader()
options=Options(connection='local', module_path='', forks=100, become=None, become_method=None,
                become_user=None, check = False, diff=False)

passwords=dict(vault_pass='secret')

results_callback = ResultCallback()

inventory = InventoryManager(loader=loader, sources=['etc/ansible/hosts'])
variable_manager = VariableManager(loader=loader, inventory=inventory)

play_source = dict(
        name = "check",
        hosts = 'localhost',
        gather_facts = 'no',
        tasks = [
            dict(action=dict(module='shell', args='hostname'), register='shell_out'),
            dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
        ]
)
play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

task = None
try:
    task = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            passwords=passwords,
            stdout_callback='results_callback'
    )

    result = task.run(play)
finally:
    if task is not None:
        task.cleanup()
