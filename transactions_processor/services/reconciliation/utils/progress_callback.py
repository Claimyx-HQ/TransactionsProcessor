from typing import Callable


class ProgressCallback:
    def __init__(self):
        self._callback: Callable[[float], None] | None = None

    def __call__(self, progress: float) -> None:
        if self._callback:
            self._callback(progress)

    @property
    def callback(self) -> Callable[[float], None] | None:
        return self._callback

    @callback.setter
    def callback(self, new_callback: Callable[[float], None]) -> None:
        self._callback = new_callback
