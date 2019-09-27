from abc import ABC
from typing import Any, cast, List

from polytropos.actions.filter.univariate.__univariate import UnivariateFilter
from polytropos.ontology.context import Context
from polytropos.ontology.schema import Schema

class OneOfFilter(UnivariateFilter, ABC):
    def __init__(self, context: Context, schema: Schema, var_id: str, values: List, narrows: bool = True,
                 filters: bool = True):

        super(OneOfFilter, self).__init__(context, schema, var_id, narrows=narrows, filters=filters)
        if values is None or len(values) == 0:
            raise ValueError('Must provide at least one matching value for "one-of" filters.')

        self._validate()

        self.values = {self.variable.cast(value) for value in values}

        if self.variable.data_type == "Text":
            self.values = {value.lower() for value in self.values}
            self.threshold = self.threshold.lower()

    def _validate(self):
        """Check for any class-specific parameter requirements."""
        pass

class MatchesOneOf(OneOfFilter):
    def compares_true(self, candidate: Any) -> bool:
        return candidate in self.values

class ContainsOneOf(OneOfFilter):
    def _validate(self):
        pass

    def compares_true(self, candidate: str) -> bool:
        for value in self.values:
            if value in candidate:
                return True
        return False
