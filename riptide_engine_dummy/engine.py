import asyncio
from typing import Tuple, Dict, Union, List, Optional

from riptide.config.document.command import Command
from riptide.config.document.project import Project
from riptide.engine.abstract import AbstractEngine
from riptide.engine.project_start_ctx import riptide_start_project_ctx
from riptide.engine.results import StartStopResultStep, MultiResultQueue, ResultQueue
from riptide_engine_docker import named_volumes


async def faux_task(queue: ResultQueue):
    queue.put(StartStopResultStep(current_step=1, steps=None, text='Pretending...'))
    await asyncio.sleep(2)
    queue.end()


class DummyEngine(AbstractEngine):
    def __init__(self):
        self._running_services: Dict[str, Dict[str, bool]] = {}

    def start_project(self,
                      project: Project,
                      services: List[str],
                      quick=False,
                      command_group: str = "default") -> MultiResultQueue[StartStopResultStep]:

        with riptide_start_project_ctx(project):
            if project["name"] not in self._running_services:
                self._running_services[project["name"]] = {}
            queues = {}
            loop = asyncio.get_event_loop()
            for service_name in services:
                queue = ResultQueue()
                queues[queue] = service_name
                self._running_services[project["name"]][service_name] = True
                loop.run_in_executor(
                    None,
                    faux_task,

                    queue,
                )

            return MultiResultQueue(queues)

    def stop_project(self, project: Project, services: List[str]) -> MultiResultQueue[StartStopResultStep]:
        if project["name"] not in self._running_services:
            self._running_services[project["name"]] = {}
        queues = {}
        loop = asyncio.get_event_loop()
        for service_name in services:
            queue = ResultQueue()
            queues[queue] = service_name
            self._running_services[project["name"]][service_name] = True
            loop.run_in_executor(
                None,
                faux_task,

                queue,
            )

        return MultiResultQueue(queues)

    def status(self, project: Project) -> Dict[str, bool]:
        if project["name"] not in self._running_services:
            self._running_services[project["name"]] = {}
        for service_name in project["app"]["services"].values():
            if service_name not in self._running_services[project["name"]]:
                self._running_services[project["name"]][service_name] = False
        return self._running_services[project["name"]]

    def service_status(self, project: Project, service_name: str) -> bool:
        if project["name"] not in self._running_services:
            self._running_services[project["name"]] = {}
        if service_name not in self._running_services[project["name"]]:
            return False
        return self._running_services[project["name"]][service_name]

    def container_name_for(self, project: 'Project', service_name: str):
        return f"{project['name']}-{service_name}"

    def address_for(self, project: Project, service_name: str) -> Union[None, Tuple[str, int]]:
        return None

    def cmd(self,
            project: 'Project',
            command_name: str,
            arguments: List[str],
            unimportant_paths_unsynced=False) -> int:
        pass

    def cmd_in_service(self,
                       project: 'Project',
                       command_name: str,
                       service_name: str,
                       arguments: List[str]) -> int:
        pass

    def service_fg(self,
                   project: 'Project',
                   service_name: str,
                   arguments: List[str],
                   unimportant_paths_unsynced=False,
                   command_group: str = "default") -> None:
        pass

    def exec(self, project: Project, service_name: str, cols=None, lines=None, root=False) -> None:
        pass

    def exec_custom(self, project: Project, service_name: str, command: str, cols=None, lines=None, root=False) -> None:
        pass

    def cmd_detached(self, project: 'Project', command: 'Command', run_as_root=False):
        pass

    def pull_images(self, project: 'Project', line_reset='\n', update_func=lambda msg: None) -> None:
        update_func("Done!\n\n")

    def path_rm(self, path, project: 'Project'):
        pass

    def path_copy(self, fromm, to, project: 'Project'):
        pass

    def performance_value_for_auto(self, key: str, platform: str) -> bool:
        return False

    def list_named_volumes(self) -> List[str]:
        return []

    def delete_named_volume(self, name: str) -> None:
        named_volumes.delete(self.client, name)

    def exists_named_volume(self, name: str) -> bool:
        return named_volumes.exists(self.client, name)

    def copy_named_volume(self, from_name: str, target_name: str) -> None:
        named_volumes.copy(self.client, from_name, target_name)

    def create_named_volume(self, name: str) -> None:
        pass

    def get_service_or_command_image_labels(self, obj: Union['Service', 'Command']) -> Optional[Dict[str, str]]:
        return None
