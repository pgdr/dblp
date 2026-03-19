# dblp conference to journal tracker

How to run is:

```bash
rm -f dupes.txt && python db.py dblp.xml.gz && python readjson.py dblp_items.json > dupes.txt && ./filter.sh
```


You need `wget https://dblp.uni-trier.de/xml/dblp.xml.gz` first.
