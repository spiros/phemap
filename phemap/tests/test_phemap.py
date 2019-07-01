import pytest
import numpy as np

from phemap import Phemap

source_file = 'phecode_definitions1.2.csv'
mapping_file = 'phecode_map_v1_2_icd10_beta.csv'

phemap = Phemap(source_file=source_file, mapping_file=mapping_file)


def test_get_phecode():

    phecode_008 = {'phecode': '008', 'phenotype': 'Intestinal infection',
                   'phecode_exclude_range': '001-009.99', 'sex': np.nan,
                   'rollup': '1', 'leaf': '0', 'category_number': '1',
                   'category': 'infectious diseases', 'phecode_num': 8.0}

    assert phemap.get_phecode_info('008') == phecode_008

    with pytest.raises(ValueError):
        phemap.get_phecode_info('ABC123')


def test_match_icd_to_phecode():
    assert phemap.get_phecode_for_icd10('I50') == '428.2'
    assert phemap.get_phecode_for_icd10('C55') == '182'
    assert phemap.get_phecode_for_icd10('C50.9') == '174.11'

    with pytest.raises(ValueError):
        phemap.get_phecode_for_icd10('ABC123')


def test_get_phecode_exclusions():
    mi_exclude = ['411', '411.1', '411.2',
                  '411.3', '411.4', '411.41',
                  '411.8', '411.9', '414', '414.2']

    assert phemap.get_phecode_exclusions('411.2') == mi_exclude


def test_get_all_phecodes():
    assert len(phemap.get_all_phecodes()) == 1866


def test_get_icd_for_phecode():
    cvd_icd = ['I65.1', 'I65.3', 'I65', 'I65.2',
               'I65.9', 'I65.0', 'I65.8']

    d_icd = ['E10', 'E10.0', 'E10.9', 'E10.6',
             'E10.8', 'E10.7']

    c_icd = ['C50.5', 'C50.3', 'C50.6', 'C50.2',
             'C50.8', 'C50', 'C50-C50.9', 'C50.0', 'C50.4',
             'C50.1', 'Z85.3', 'C50.9']

    # use set to ignore order
    assert set(phemap.get_icd_for_phecode('433.1')) == set(cvd_icd)
    assert set(phemap.get_icd_for_phecode('250.1')) == set(d_icd)
    assert set(phemap.get_icd_for_phecode('174.11')) == set(c_icd)

    with pytest.raises(ValueError):
        phemap.get_icd_for_phecode('ABC123')
