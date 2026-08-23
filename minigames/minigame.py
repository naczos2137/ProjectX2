from abc import ABC, abstractmethod
from typing import Any, Callable

from player import Player

class MiniGame(ABC):
    @abstractmethod
    def __init__(self, players: dict[str, Player]) -> None:
        pass

    @abstractmethod
    def get_state(self, player_id: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def set_info(self, player_id: str, info: dict[str, Any]) -> None:
        raise NotImplementedError
