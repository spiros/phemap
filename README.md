Phemap [![Build Status](https://travis-ci.org/spiros/phemap.svg?branch=master)](https://travis-ci.org/spiros/phemap)
--------------

This utility provides some very basic functions
to map between ICD-10 terms used in hospital diagnoses
for UK Biobank and PheCodes as outlined
in Wu P. et al. https://www.biorxiv.org/content/10.1101/462077v4

Requires the phecode definitions file and the icd10-to-phecode
mapping file - you can grab the latest version of both
files from https://phewascatalog.org/phecodes

Notes
-----

UK Biobank secondary care data are coded using ICD-10 but the dot
has been stripped out i.e. "I21.0 Ischaemic heart disease" is recorded
as 'I210' so you will need to add the dot separator prior to attempting
to match.

Not all ICD-10 terms are mapped to PheCodes and not all PheCodes
which are mapped to ICD-10 terms appear to have a valid definition
in the PheCodes definition file. Mappings are usually one-to-one but can also
be one-to-many: 
> Of all possible ICD-10 codes, 9,165 (76.20%) mapped to at least one PheCode, and 289 (2.40%) mapped to >1 PheCode.  ICD-10 code B21.1 (HIV disease resulting in Burkitt’s lymphoma) maps to two PheCodes: 071.1 (HIV infection, symptomatic) and 202.2 (Non-Hodgkin's lymphoma).

Examples
--------

```
import phemap

>>> phemap = phemap.Phemap( source_file=PHECODE_FILE, mapping_file=PHECODE_MAP )

>>> phemap.get_icd_for_phecode('495')
['J45.8', 'J45', 'J45.1', 'J45.0', 'J45.9']

>>> phemap.get_phecode_for_icd10('J45.1')
'495'

>>> phemap.get_phecode_info('495')
{'phecode': '495',
 'phenotype': 'Asthma',
 'phecode_exclude_range': '490-498.99',
 'sex': nan,
 'rollup': '1',
 'leaf': '0',
 'category_number': '9',
 'category': 'respiratory',
 'phecode_num': 495.0}

>>> phemap.get_phecode_exclusions('495')
['495',
 '495.1',
 '495.11',
 '495.2',
 '496',
 '496.1',
 '496.2',
 '496.21',
 '496.3',
 '497',
 '498']

>>> all_phecodes = phemap.get_all_phecodes()
>>> all_phecodes[10]
{'phecode': '038.1',
 'phenotype': 'Gram negative septicemia',
 'phecode_exclude_range': '010-041.99',
 'sex': 'Both',
 'rollup': '1',
 'leaf': '1',
 'category_number': '1',
 'category': 'infectious diseases',
 'phecode_num': 38.1}
```

Useful reading material
-----------------------

https://www.biorxiv.org/content/10.1101/462077v4

https://www.ncbi.nlm.nih.gov/pubmed/20335276

https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0175508
