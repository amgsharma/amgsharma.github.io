# -*- coding: utf-8 -*-
"""
Procedure to scrape a table from wikipedia using python. Uses MediaWikiAPI to get page content.
Allows for cells spanning multiple rows and/or columns. Outputs a Pandas dataframe.
Page used for testing (second table in particular):
https://en.wikipedia.org/wiki/International_Phonetic_Alphabet_chart_for_English_dialects
"""

import pandas as pd
from bs4 import BeautifulSoup
import wikipedia

def wikitable_to_dataframe(table):
    """
    Exports a Wikipedia table parsed by BeautifulSoup. Deals with spanning:
    multirow and multicolumn should format as expected.
    """
    rows=table.findAll("tr")
    nrows=len(rows)
    ncols=max([len(r.findAll(['th','td'])) for r in rows])

    # preallocate table structure
    # (this is required because we need to move forward in the table
    # structure once we've found a row span)
    data=[]
    for i in range(nrows):
        rowD=[]
        for j in range(ncols):
            rowD.append('')
        data.append(rowD)

    # fill the table with data:
    # move across cells and use span to fill extra cells
    for i,row in enumerate(rows):
        cells = row.findAll(["td","th"])
        for j,cell in enumerate(cells):
            cspan=int(cell.get('colspan',1))
            rspan=int(cell.get('rowspan',1))
            l = 0
            for k in range(rspan):
                # Shifts to the first empty cell of this row
                # Avoid replacing previously insterted content
                while data[i+k][j+l]:
                    l+=1
                for m in range(cspan):
                    data[i+k][j+l+m]+=cell.text.strip("\n")

    df = pd.DataFrame(data)
    df.columns = df.iloc[0]
    df = df[1:]
    return df



test_page = wikipedia.WikipediaPage(title='List_of_recently_extinct_mammals')
soup = BeautifulSoup(test_page.html(), 'html.parser')
tables = soup.findAll("table", { "class" : "wikitable" })

extinct = wikitable_to_dataframe(tables[0])
maybe_extinct = wikitable_to_dataframe(tables[2])
import ipdb;ipdb.set_trace()
