from typing import Set

from polytropos.ontology.composite import Composite

from polytropos.actions.filter import Filter

class LatestFilter(Filter):
    """Filters out all temporal periods except the latest period."""

    def narrow(self, composite: Composite) -> None:
        to_retain: Set[str] = {max(composite.periods)}
        to_remove: Set[str] = set(composite.periods) - to_retain
        for period in to_remove:
            del composite.content[period]

class EarliestFilter(Filter):
    """Filters out all temporal periods except the earliest period."""

    def narrow(self, composite: Composite) -> None:
        to_retain: Set[str] = {min(composite.periods)}
        to_remove: Set[str] = set(composite.periods) - to_retain
        for period in to_remove:
            del composite.content[period]
