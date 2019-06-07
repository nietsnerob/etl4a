from dataclasses import dataclass
from typing import Iterator, Tuple, Dict, Iterable, Any, Optional

from polytropos.ontology.aggregation import Aggregation
from polytropos.ontology.variable import Variable
from polytropos.util import composites


@dataclass
class EconomicOverview(Aggregation):
    n_employee_var: Variable
    revenue_var: Variable
    source_zip_var: Variable
    source_city_var: Variable
    source_state_var: Variable

    # Output schema variables
    n_company_var: Variable
    mean_employee_var: Variable
    annual_prod_var: Variable
    target_zip_var: Variable
    target_city_var: Variable
    target_state_var: Variable

    def __post_init__(self):
        # Internal variable used for reduce/analyze step
        self.city_data: Dict[str, Dict] = {}

    def extract(self, composite: Dict) -> Optional[Any]:
        """In this case, the source document is very small and the analysis uses every variable in it, so we just return
        the composite. In real-world cases, only a few variables are likely to be used."""
        return composite

    def analyze(self, extracts: Iterable[Tuple[str, Any]]) -> None:
        for company_id, company in extracts:
            zip_code = composites.get_property(company, self.source_zip_var)
            city = composites.get_property(company, self.source_city_var)
            state = composites.get_property(company, self.source_state_var)

            # Create a transient composite for the city. It will be processed into its final form in emit().
            if zip_code not in self.city_data:
                self.city_data[zip_code] = {'invariant': {
                    "zip": zip_code,
                    "city": city,
                    "state": state
                }}

            for period in composites.get_periods(company):
                if period not in self.city_data[zip_code]:
                    self.city_data[zip_code][period] = {
                        "n_companies": 0,
                        "tot_employees": 0,
                        "tot_revenue": 0.0
                    }

                p_dict = self.city_data[zip_code][period]
                p_dict["n_companies"] += 1
                p_dict["tot_employees"] += composites.get_observation(company, period, self.n_employee_var)
                p_dict["tot_revenue"] += composites.get_observation(company, period, self.revenue_var)

    def emit(self) -> Iterator[Tuple[str, Dict]]:
        for zip_code, transient in self.city_data.items():
            city: Dict = {}
            for period in sorted(composites.get_periods(transient)):
                n_companies = transient[period]["n_companies"]
                tot_employees = transient[period]["tot_employees"]
                tot_revenue = transient[period]["tot_revenue"]

                mean_employees = tot_employees / n_companies
                productivity = tot_revenue / tot_employees

                composites.put_observation(city, period, self.n_company_var, n_companies)
                composites.put_observation(city, period, self.annual_prod_var, productivity)
                composites.put_observation(city, period, self.mean_employee_var, mean_employees)

            composites.put_property(city, self.target_zip_var, transient["invariant"]["zip"])
            composites.put_property(city, self.target_city_var, transient["invariant"]["city"])
            composites.put_property(city, self.target_state_var, transient["invariant"]["state"])
            
            yield zip_code, city