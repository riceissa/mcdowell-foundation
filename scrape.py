#!/usr/bin/env python3
# License: CC0 https://creativecommons.org/publicdomain/zero/1.0/

import csv
import re
import requests
import sys
from bs4 import BeautifulSoup


def main():
    with open("data.csv", "w", newline="") as f:
        fieldnames = ["year", "grantee", "amount", "six_month_report",
                      "year_end_report"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        response = requests.get("http://www.mcdowellfoundation.org/our-grants")
        soup = BeautifulSoup(response.content, "lxml")
        for table in soup.find_all("table"):
            heading = previous_heading(table).text.strip()
            m = re.match(r"Our Grants For (\d\d\d\d)$", heading)
            year = m.group(1)
            for row in table.find_all("tr")[1:]:
                d = {}
                cols = row.find_all("td")
                d['grantee'] = cols[0].text.strip()
                d['amount'] = (cols[1].text.replace("$", "")
                                      .replace(",", "").strip())
                d['year'] = year

                # Some grantees don't yet have reports so if we can't find a
                # link we just ignore them.
                try:
                    d['six_month_report'] = ("http://www.mcdowellfoundation.org" +
                                             cols[2].find("a").get("href")
                                                    .strip())
                except:
                    pass
                try:
                    d['year_end_report'] = ("http://www.mcdowellfoundation.org" +
                                            cols[3].find("a").get("href")
                                                   .strip())
                except:
                    pass

                writer.writerow(d)


def previous_heading(table):
    """Search upwards to find the heading associated with the given table."""
    tag = table
    while tag.name != "h1" and tag is not None:
        tag = tag.previous_sibling
    return tag


if __name__ == "__main__":
    main()
