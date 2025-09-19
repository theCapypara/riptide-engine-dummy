from __future__ import annotations

import asyncio

from riptide.config.document.command import Command
from riptide.config.document.project import Project
from riptide.config.document.service import Service
from riptide.engine.abstract import AbstractEngine, SimpleBindVolume
from riptide.engine.project_start_ctx import riptide_start_project_ctx
from riptide.engine.results import MultiResultQueue, ResultQueue, StartStopResultStep


async def faux_task(queue: ResultQueue):
    queue.put(StartStopResultStep(current_step=1, steps=None, text="Pretending..."))
    await asyncio.sleep(2)
    queue.end()


class DummyEngine(AbstractEngine):
    def __init__(self):
        self._running_services: dict[str, dict[str, bool]] = {}

    def start_project(
        self, project: Project, services: list[str], quick=False, command_group: str = "default"
    ) -> MultiResultQueue[StartStopResultStep]:
        with riptide_start_project_ctx(project):
            if project["name"] not in self._running_services:
                self._running_services[project["name"]] = {}
            queues = {}
            loop = asyncio.get_event_loop()
            for service_name in services:
                queue: ResultQueue[StartStopResultStep] = ResultQueue()
                queues[queue] = service_name
                self._running_services[project["name"]][service_name] = True
                loop.run_in_executor(
                    None,
                    faux_task,
                    queue,
                )

            return MultiResultQueue(queues)

    def stop_project(self, project: Project, services: list[str]) -> MultiResultQueue[StartStopResultStep]:
        if project["name"] not in self._running_services:
            self._running_services[project["name"]] = {}
        queues = {}
        loop = asyncio.get_event_loop()
        for service_name in services:
            queue: ResultQueue[StartStopResultStep] = ResultQueue()
            queues[queue] = service_name
            self._running_services[project["name"]][service_name] = True
            loop.run_in_executor(
                None,
                faux_task,
                queue,
            )

        return MultiResultQueue(queues)

    def status(self, project: Project) -> dict[str, bool]:
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

    def container_name_for(self, project: Project, service_name: str):
        return f"{project['name']}-{service_name}"

    def address_for(self, project: Project, service_name: str) -> tuple[str, int] | None:
        return None

    def cmd(
        self,
        command: Command,
        arguments: list[str],
        *,
        working_directory: str | None = None,
        extra_mounts: dict[str, SimpleBindVolume] = None,
    ) -> int:
        return 0

    def cmd_in_service(self, project: Project, command_name: str, service_name: str, arguments: list[str]) -> int:
        return 0

    def service_fg(
        self, project: Project, service_name: str, arguments: list[str], command_group: str = "default"
    ) -> None:
        pass

    def exec(self, project: Project, service_name: str, cols=None, lines=None, root=False) -> None:
        pass

    def exec_custom(self, project: Project, service_name: str, command: str, cols=None, lines=None, root=False) -> None:
        pass

    def cmd_detached(self, project: Project, command: Command, run_as_root=False):
        pass

    def pull_images(self, project: Project, line_reset="\n", update_func=lambda msg: None) -> None:
        update_func("Done!\n\n")

    def path_rm(self, path, project: Project):
        pass

    def path_copy(self, fromm, to, project: Project):
        pass

    def performance_value_for_auto(self, key: str, platform: str) -> bool:
        return False

    def list_named_volumes(self) -> list[str]:
        return []

    def delete_named_volume(self, name: str) -> None:
        pass

    def exists_named_volume(self, name: str) -> bool:
        return False

    def copy_named_volume(self, from_name: str, target_name: str) -> None:
        pass

    def create_named_volume(self, name: str) -> None:
        pass

    def get_service_or_command_image_labels(self, obj: Service | Command) -> dict[str, str] | None:
        return None
