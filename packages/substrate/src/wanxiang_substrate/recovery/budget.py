"""Configurable CPU/time/model-call style resource budgets (G06C)."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_substrate.recovery.errors import BudgetExceeded


@dataclass(frozen=True, slots=True)
class ResourceBudget:
    """Bounded loop budget: commands and ticks per window."""

    max_commands: int = 1000
    max_ticks: int = 10_000
    max_model_calls: int = 0  # model calls are absent in this profile

    def __post_init__(self) -> None:
        if self.max_commands < 0 or self.max_ticks < 0 or self.max_model_calls < 0:
            raise ValueError("budget limits must be non-negative")


class BudgetTracker:
    """Tracks consumption against a ResourceBudget (no hidden I/O)."""

    def __init__(self, budget: ResourceBudget | None = None) -> None:
        self._budget = budget or ResourceBudget()
        self._commands = 0
        self._ticks = 0
        self._model_calls = 0

    def consume(self, commands: int = 0, ticks: int = 0, model_calls: int = 0) -> None:
        next_commands = self._commands + commands
        next_ticks = self._ticks + ticks
        next_model_calls = self._model_calls + model_calls
        if next_commands > self._budget.max_commands:
            raise BudgetExceeded(
                f"command budget exceeded ({next_commands} > {self._budget.max_commands})"
            )
        if next_ticks > self._budget.max_ticks:
            raise BudgetExceeded(f"tick budget exceeded ({next_ticks} > {self._budget.max_ticks})")
        if next_model_calls > self._budget.max_model_calls:
            raise BudgetExceeded(
                f"model-call budget exceeded ({next_model_calls} > {self._budget.max_model_calls})"
            )
        self._commands = next_commands
        self._ticks = next_ticks
        self._model_calls = next_model_calls

    def reset(self) -> None:
        self._commands = 0
        self._ticks = 0
        self._model_calls = 0

    def remaining(self) -> dict[str, int]:
        return {
            "commands": self._budget.max_commands - self._commands,
            "ticks": self._budget.max_ticks - self._ticks,
            "model_calls": self._budget.max_model_calls - self._model_calls,
        }
