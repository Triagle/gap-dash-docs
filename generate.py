#!/usr/bin/env python3

from bs4 import BeautifulSoup
import sqlite3


INDEX = "chapInd.html"


def parse_index(html):
    soup = BeautifulSoup(html, "html.parser")
    index = soup.find("div", {"class": "index"})
    doc_link_pairs = []
    for item in index.find_all("code"):
        name = item.text
        link = item.findNext("a").get("href")
        doc_link_pairs.append((name, link))

    return doc_link_pairs


def write_database(db, index):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE searchIndex(id INTEGER PRIMARY KEY,\
                    name TEXT,\
                    type TEXT,\
                    path TEXT);"
        )
        cur.execute("CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);")

        for name, path in index:
            cur.execute("SELECT rowid FROM searchIndex WHERE path = ?", (path,))
            dbpath = cur.fetchone()
            cur.execute("SELECT rowid FROM searchIndex WHERE name = ?", (name,))
            dbname = cur.fetchone()

            if dbpath is None and dbname is None:
                cur.execute(
                    "INSERT OR IGNORE INTO searchIndex(name, type, path)\
                        VALUES (?,?,?)",
                    (name, "Section", path),
                )


def parse_manual(html_fp):
    with open(html_fp, "r") as f:
        html = f.read()
        return parse_index(html)


if __name__ == "__main__":
    # index = parse_manual("gap.docset/Contents/Resources/Documents/" + INDEX)
    # write_database("gap.docset/Contents/Resources/docSet.dsidx", index)
    fining_index = parse_manual("fining.docset/Contents/Resources/Documents/" + INDEX)
    write_database("fining.docset/Contents/Resources/docSet.dsidx", fining_index)
