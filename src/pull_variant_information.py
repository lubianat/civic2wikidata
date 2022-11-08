import requests
import json
from pathlib import Path

HERE = Path(__file__).parent.resolve()
RESULTS = HERE.parent.joinpath("results").resolve()


def main():
    url = "https://civicdb.org/api/graphql"

    body = """
  { 
    variants (evidenceStatusFilter: WITH_ACCEPTED) {
    pageInfo {
      endCursor
      startCursor
    } 
    pageCount
    nodes {
      name
      id
      myVariantInfo {
        dbsnpRsid
      }
    }
    }
  }
  """

    response = requests.post(url=url, json={"query": body})
    first_data = response.json()
    n_pages = first_data["data"]["variants"]["pageCount"]
    end_cursor = first_data["data"]["variants"]["pageInfo"]["endCursor"]
    make_body(end_cursor)
    flag = 0

    civic2dbsnip = {}
    civic2dbsnip = extract_civic2dbsnip(first_data, civic2dbsnip)
    while flag < n_pages:
        body = make_body(end_cursor)
        response = requests.post(url=url, json={"query": body})
        page_data = response.json()
        end_cursor = page_data["data"]["variants"]["pageInfo"]["endCursor"]
        flag += 1
        civic2dbsnip = extract_civic2dbsnip(page_data, civic2dbsnip)

    RESULTS.joinpath("civic2dbsnip.json").write_text(
        json.dumps(civic2dbsnip, indent=4, sort_keys=True)
    )


def make_body(end_cursor):
    body = (
        """
{ 
  variants (evidenceStatusFilter: WITH_ACCEPTED """
        + f'after: "{end_cursor}"'
        + """) {
	 pageInfo {
	   endCursor
	   startCursor
	 } 
	 pageCount
   nodes {
    name
    id
    myVariantInfo {
      dbsnpRsid
    }
  }
  }
}
"""
    )
    return body


def extract_civic2dbsnip(data, civic2dbsnip):
    for entry in data["data"]["variants"]["nodes"]:

        if (
            entry["myVariantInfo"] is not None
            and entry["myVariantInfo"]["dbsnpRsid"] is not None
        ):
            civic2dbsnip[entry["id"]] = entry["myVariantInfo"]["dbsnpRsid"]
    return civic2dbsnip


if __name__ == "__main__":
    main()
