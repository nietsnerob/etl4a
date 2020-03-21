from typing import List

import pytest

from polytropos.actions.filter.logical_operators.or_operator import Or
from polytropos.ontology.composite import Composite
from test.test_functional.action.filter.logical_operator.conftest import check_passes_and_narrow, DummyContainsFilter, create_composite


def test_no_operands(context, schema):
    with pytest.raises(AssertionError):
        Or(context, schema, [], narrows=True, filters=True)


@pytest.mark.parametrize("narrows", [True, False])
@pytest.mark.parametrize("filters, narrow_content", [
    (True,
     [
         {"immutable": "immutable_1", "p1": "p1_1", "p2": "p2_1"},
         None,
     ]),
    (False,
     [
         {"immutable": "immutable_1", "p1": "p1_1", "p2": "p2_1"},
         {"immutable": "immutable_2", "p1": "p1_2", "p2": "p2_2"},
     ]),
])
def test_single_operand(context, schema, narrows, filters, narrow_content):
    operator = Or(context, schema, [
        DummyContainsFilter(context, schema, narrows, filters, composite_part="1", period_part="p"),
    ], narrows=narrows, filters=filters)

    composites: List[Composite] = [
        create_composite(schema, "1", ["p1", "x", "p2", "immutable"]),
        create_composite(schema, "2", ["immutable", "p1", "x", "p2"])
    ]

    check_passes_and_narrow(composites, narrows, operator, narrow_content)


@pytest.mark.parametrize("narrows", [True, False])
@pytest.mark.parametrize("filters, narrow_content", [
    (True,
     [
         {"immutable": "immutable_12", "p": "p_12", "q": "q_12", "pq": "pq_12", "py": "py_12"},
         {"immutable": "immutable_21", "pq": "pq_21", "qp": "qp_21", "p": "p_21"},
         {"immutable": "immutable_31", "pq": "pq_31", "p": "p_31"},
         None,
     ]),
    (False,
     [
         {"immutable": "immutable_12", "p": "p_12", "q": "q_12", "pq": "pq_12", "py": "py_12"},
         {"immutable": "immutable_21", "pq": "pq_21", "qp": "qp_21", "p": "p_21"},
         {"immutable": "immutable_31", "pq": "pq_31", "p": "p_31", "q": "q_31"},
         {"immutable": "immutable_33", "qp": "qp_33", "q": "q_33"},
     ]),
])
def test_two_operands(context, schema, narrows, filters, narrow_content):
    operator = Or(context, schema, [
        DummyContainsFilter(context, schema, narrows, filters, composite_part="1", period_part="p"),
        DummyContainsFilter(context, schema, narrows, filters, composite_part="2", period_part="q"),
    ], narrows=narrows, filters=filters)

    composites: List[Composite] = [
        create_composite(schema, "12", ["p", "q", "pq", "py", "immutable"]),
        create_composite(schema, "21", ["qp", "pq", "p", "x", "immutable"]),
        create_composite(schema, "31", ["immutable", "pq", "x", "p", "q"]),
        create_composite(schema, "33", ["immutable", "qp", "y", "q"]),
    ]

    check_passes_and_narrow(composites, narrows, operator, narrow_content)
