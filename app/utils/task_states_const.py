class TaskStatesConst:
    @property
    def created(self) -> str:
        return "created"

    @property
    def in_progress(self) -> str:
        return "in progress"

    @property
    def done(self) -> str:
        return "done"

    @property
    def crashed(self) -> str:
        return "crashed"


task_states = TaskStatesConst()
