from pathlib import Path
import json

HERE = Path(__file__).parent.resolve()
DATA = HERE.parent.joinpath("data").resolve()
RESULTS = HERE.parent.joinpath("results").resolve()

civic2dbsnip = json.loads(RESULTS.joinpath("civic2dbsnip.json").read_text())
civic2wikidata = json.loads(RESULTS.joinpath("civic2wikidata.json").read_text())

qs = ""

for key, value in civic2wikidata.items():

    qs += f'{civic2wikidata[key]}|P6861|"{civic2dbsnip[key]}"|S248|Q27612411' + "\n"


RESULTS.joinpath("quickstatements.txt").write_text(qs)
