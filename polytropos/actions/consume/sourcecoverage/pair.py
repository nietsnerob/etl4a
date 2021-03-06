from typing import NamedTuple

from polytropos.ontology.variable import VariableId


class SourceTargetPair(NamedTuple):
    """Represents a pair of source/target variable identifiers."""

    source_var_id: VariableId
    target_var_id: VariableId
