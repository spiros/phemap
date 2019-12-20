"""Phemap

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

Not all ICD-10 terms are mapped to phecodes and not all phecodes
which are mapped to ICD-10 terms appear to have a valid definition
in the phecode code.

Examples
--------

from phemap import Phemap

source_file = 'data/phecode_definitions1.2.csv'
mapping_file = 'data/phecode_map_v1_2_icd10_beta.csv'

phemap = Phemap(source_file=source_file, mapping_file=mapping_file)

>>> phemap.get_icd_for_phecode('495')
['J45.8', 'J45', 'J45.1', 'J45.0', 'J45.9']

>>> phemap.get_phecode_for_icd10('J45.1')
['495']

>>> phemap.get_phecode_for_icd10('B21.1')
['202.2', '71.1']

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

Useful reading material
-----------------------

https://www.biorxiv.org/content/10.1101/462077v4
https://www.ncbi.nlm.nih.gov/pubmed/20335276
https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0175508


"""

import pandas as pd


class Phemap:

    def __init__(self, source_file, mapping_file):
        cols_phecodes = [
            'phecode',
            'phenotype',
            'phecode_exclude_range',
            'sex',
            'rollup',
            'leaf',
            'category_number',
            'category']

        dtypes_phecodes = {x: 'str' for x in cols_phecodes}

        cols_phecodemap = [
            'icd10',
            'phecode',
            'phecode_exclude_range',
            'phenotype_exlude']

        dtypes_map = {x: 'str' for x in cols_phecodemap}

        self.phecodes = pd.read_csv(
            source_file,
            dtype=dtypes_phecodes,
            names=cols_phecodes,
            header=0)

        self.phecodes['phecode_num'] = pd.to_numeric(
            self.phecodes['phecode'])

        self.phecodemap = pd.read_csv(
            mapping_file,
            dtype=dtypes_map,
            names=cols_phecodemap,
            header=0)

        self.phecodemap['phecode_num'] = pd.to_numeric(
            self.phecodemap['phecode'])

    def get_phecode_info(self, phecode):
        """
        Given a phecode, returns a dictionary of
        all available information.

        Parameters
        ----------
        p : string
            A valid PheCode term.

        Returns
        -------
        phecode : dict

        Raises
        ------
        ValueError
            The phecode supplied was not found in the definition
            file or is not properly formatted.

        Examples
        --------

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
        """

        m = self.phecodes['phecode_num'] == float(phecode)
        matches = self.phecodes.loc[m].to_dict(orient='records')

        if matches:
            return matches[0]
        else:
            raise ValueError("Phecode not found: %s" % phecode)

    def get_phecode_for_icd10(self, icd10):
        """
        Given an ICD-10 term, returns the phecode.

        Parameters
        ----------
        icd10 : string
            A valid ICD-10 term.


        Returns
        -------
        phecodes : list of strings

        Raises
        ------
        ValueError
            A match for the supplied ICD-10 term
            could not be located in the mapping file.

        Examples
        --------

        >>> phemap.get_phecode_for_icd10('J45.1')
        ['495']

        >>> phemap.get_phecode_for_icd10('B21.1')
        ['202.2', '71.1']

        """

        m = self.phecodemap['icd10'] == icd10
        phecode_match = self.phecodemap.loc[m].to_dict(orient='records')

        if phecode_match:
            return [p['phecode'] for p in phecode_match]
        else:
            raise ValueError("Mapping for term not found: %s" % icd10)

    def get_icd_for_phecode(self, phecode):
        """
        Given a phecode, returns a list of ICD-10
        terms which are associated with the phecode
        in the mapping file.

        Parameters
        ----------
        phecode : string
            A valid phecode

        Returns
        -------
        icd : list of strings

        Raises
        ------
        ValueError
            A match for the supplied phecode term
            could not be located in the mapping file.

        Examples
        --------

        >>> phemap.get_icd_for_phecode('495')
        ['J45.8', 'J45', 'J45.1', 'J45.0', 'J45.9']

        """

        m = self.phecodemap['phecode_num'] == float(phecode)
        phecode_match = self.phecodemap.loc[m]

        if len(phecode_match) > 0:
            return phecode_match.icd10.tolist()
        else:
            raise ValueError("No map found for phecode %s" % phecode)

    def get_phecode_exclusions(self, phecode):
        """
        Given a valid phecode, returns a list of
        strings with all phecodes in the
        phenotype's exclude range.

        Parameters
        ----------
        phecode : string
            A valid phecode.

        Returns
        -------
        v : array of strings

        Raises
        ------
        ValueError:
            The phecode could not be located in the phecode
            definitions file.

        Examples
        --------

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

        """

        phecode = self.get_phecode_info(phecode)
        excl_range = phecode['phecode_exclude_range']
        (ex_start, ex_end) = excl_range.split('-')

        phecodes_in_exclude_range = self.phecodes[
            (self.phecodes['phecode_num'] >= float(ex_start)) &
            (self.phecodes['phecode_num'] <= float(ex_end))]

        v = phecodes_in_exclude_range.phecode.tolist()
        return v

    def get_all_phecodes(self):

        """
        Returns a list of dictionaries of all
        the phecodes loaded from the definitions
        file.

        Returns
        -------
        d : list of dictionaries

        Examples
        --------

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

        """

        return self.phecodes.to_dict(orient='records')
