import logging
import threading
import random
import time
from typing import Callable
from datetime import datetime, timedelta


class Atode:
    def __init__(self, daemon: bool = False, log_level: int = logging.DEBUG):
        self._tasks = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=daemon)
        self._thread.start()

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        handler = logging.StreamHandler()
        handler.setFormatter(_ColorFormatter("\033[92m%(asctime)s\033[0m | %(levelname)s\t | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
        self.logger.addHandler(handler)

    def _run(self):
        probabilities = {
            "execute_early_task": 0.05,
            "execute_no_deadline_task": 0.05,
            "escapism": 0.1
        }
        while not self._stop_event.is_set():
            now = datetime.now()
            tasks_to_run = []

            with self._lock:
                deadline_tasks = []
                pending_tasks = []
                no_deadline_tasks = []

                for task in self._tasks:
                    if task['deadline'] is not None:
                        if task['deadline'] <= now:
                            deadline_tasks.append(task)
                        else:
                            pending_tasks.append(task)
                    else:
                        no_deadline_tasks.append(task)

                # 夏休みの宿題(8月31日)
                random.shuffle(deadline_tasks)
                for deadline_task in deadline_tasks:
                    self.logger.debug(f"Task added ( standard ): {deadline_task['func'].__name__} *args: {deadline_task['args']} **kwargs: {deadline_task['kwargs']}")
                    tasks_to_run.append(deadline_task)
                    self._tasks.remove(deadline_task)

                # 締め切りよりも早く実行
                if pending_tasks and random.random() < probabilities["execute_early_task"]:
                    early_task = random.choice(pending_tasks)
                    self.logger.debug(f"Task added ( early ): {early_task['func'].__name__} *args: {early_task['args']} **kwargs: {early_task['kwargs']}")
                    tasks_to_run.append(early_task)
                    self._tasks.remove(early_task)

                # 締め切りないタスク
                if no_deadline_tasks and random.random() < probabilities["execute_no_deadline_task"]:
                    nd_task = random.choice(no_deadline_tasks)
                    self.logger.debug(f"Task added ( no_deadline ): {nd_task['func'].__name__} *args: {nd_task['args']} **kwargs: {nd_task['kwargs']}")
                    tasks_to_run.append(nd_task)
                    self._tasks.remove(nd_task)

                # 現実逃避
                valid_pending = sorted(
                    [t for t in (pending_tasks + no_deadline_tasks) if t in self._tasks],
                    key=lambda x: x['deadline'] if x['deadline'] else datetime.max
                )
                if valid_pending and random.random() < probabilities["escapism"] and len(self._tasks) > 1:
                    escapism_task = valid_pending[0]
                    distraction_candidates = [t for t in self._tasks if t != escapism_task]
                    if distraction_candidates:
                        distraction_task = random.choice(distraction_candidates)
                        self.logger.debug(f"Escapism from: {escapism_task['func'].__name__} *args: {escapism_task['args']} **kwargs: {escapism_task['kwargs']}")
                        self.logger.info(f"Distraction to: {distraction_task['func'].__name__} *args: {distraction_task['args']} **kwargs: {distraction_task['kwargs']}")

                        # 現実逃避だからこれだけやっておしまい
                        self._run_task(distraction_task)
                        self._tasks.remove(distraction_task)
                        continue

            for task in tasks_to_run:
                self.logger.info(f"Task executed: {task['func'].__name__} *args: {task['args']} **kwargs: {task['kwargs']}")
                self._run_task(task)

            time.sleep(1)

    def _run_task(self, task):
        try:
            task['func'](*task['args'], **task['kwargs'])
        except Exception as e:
            self.logger.exception(f"Error occurred while executing task: {task['func'].__name__}")

    def yaru(self, func: Callable, deadline_sec: int | None=None, args=(), kwargs={}):
        if deadline_sec is None:
            deadline = None
        else:
            deadline = datetime.now() + timedelta(seconds=deadline_sec)

        with self._lock:
            self._tasks.append({
                "func": func,
                "args": args,
                "kwargs": kwargs,
                "deadline": deadline
            })
        self.logger.info(f"Task scheduled: {func.__name__} in {deadline_sec} seconds")

    def stop(self, force: bool = False):
        try:
            if force:
                self.logger.info("Forcefully stopping the thread...")
                self._stop_event.set()
            else:
                self.logger.info("Waiting for remaining tasks to complete before stopping the thread...")
                while self._tasks != []:
                    time.sleep(1)
                self.logger.info("All tasks have been completed. Stopping the thread.")
                self._stop_event.set()
        except KeyboardInterrupt:
            self.logger.warning("KeyboardInterrupt: Stopping the thread...")
            self._stop_event.set()
        finally:
            self._thread.join()
            self.logger.info("Thread has been successfully stopped.")


class _ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[94m",
        "INFO": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "CRITICAL": "\033[95m"
    }
    RESET = "\033[0m"

    def format(self, record):
        record.levelname = f"{self.COLORS.get(record.levelname, self.RESET)}{record.levelname}{self.RESET}"
        return super().format(record)
