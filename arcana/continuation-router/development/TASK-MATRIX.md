# Task Matrix

| ID | Complexity | Scenario | Expected Output | Status |
| --- | --- | --- | --- | --- |
| route-low | low | Planning-drift handoff without apply authorization. | Ranked Invoke route, no dispatch, source block preserved. | fixture-ready |
| route-medium | medium | Exact Invoke Refresh apply authorization with complete owner inputs. | One selected dispatch, joined owner receipt, returned Task Session route. | fixture-ready |
| route-complex | complex | Ambiguous owners plus repeated source fingerprint. | Two probable routes, no selection, repeated Task Session re-entry blocked. | fixture-ready |
| route-legacy | medium | Legacy receipt with free-text refresh advice. | Conservative adaptation without silent apply authority. | fixture-ready |
| route-unknown | medium | Unknown capability and mode. | Blocked selection and no dispatch. | fixture-ready |
