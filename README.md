# dblp conference to journal tracker

How to run is:

```bash
rm -f dupes.txt \
&& python db.py dblp.xml.gz \
&& python readjson.py dblp_items.json > dupes.txt \
&& ./filter.sh
```


You need `wget https://dblp.uni-trier.de/xml/dblp.xml.gz` first.

To get the final result, one can also

```bash
cat count.csv | trim | ph query count 5 | ph columns count conf journal > out.csv
```

```bash
jq 'map(select(.venue == "opodis"))' dblp_items.json
```

## The results are in

Check out [the results](results.md).
