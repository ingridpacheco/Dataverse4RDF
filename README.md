# Dataverse4RDF

Script to update variables in DDI file from RDF metadata stored in Dataverse.

### Libs:

* [pyDataverse](https://pydataverse.readthedocs.io/en/latest/)
* [subprocess](https://docs.python.org/3/library/subprocess.html)

### Inputs:

* Datafile ID (file must be RDF with turtle extension (.ttl))
* User token

### Steps:

1. RDF file is downloaded from Dataverse
2. Descriptors and complementary metadata are extracted from file
3. XML file is created considering these descriptors as variables and variable groups
4. Variables from DDI file are updated using the XML file generated

### How to run:

```
python main.py
```
