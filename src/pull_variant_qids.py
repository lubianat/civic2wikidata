from wdcuration import lookup_multiple_ids
import json
from pathlib import Path

HERE = Path(__file__).parent.resolve()
DATA = HERE.parent.joinpath("data").resolve()
RESULTS = HERE.parent.joinpath("results").resolve()

civic_ids_dict = json.loads(RESULTS.joinpath("civic2dbsnip.json").read_text())

civic_ids = civic_ids_dict.keys()

wikidata_ids = lookup_multiple_ids(civic_ids, "P3329")


RESULTS.joinpath("civic2wikidata.json").write_text(
    json.dumps(wikidata_ids, indent=4, sort_keys=True)
)
