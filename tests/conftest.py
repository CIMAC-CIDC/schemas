# -*- coding: utf-8 -*-

"""Global test configuration and shared fixtures"""

import os

import pytest

from cidc_schemas.manifest import ShippingManifest

from .constants import SCHEMA_DIR


@pytest.fixture
def pbmc_manifest():
    pbmc_manifest_path = os.path.join(SCHEMA_DIR, 'manifests', 'pbmc.json')
    return ShippingManifest.from_json(pbmc_manifest_path, SCHEMA_DIR)


@pytest.fixture
def tiny_manifest():
    """A small, valid """

    test_property = {'$id': 'success', 'type': 'string'}
    test_date = {'type': 'string', 'format': 'date'}
    test_time = {'type': 'string', 'format': 'time'}

    tiny_manifest_schema = {
        '$id': 'tiny_manifest',
        'title': 'Tiny Manifest',
        'properties': {
            'worksheets': {
                'properties': {
                    'TEST_SHEET': {
                        'properties': {
                            'preamble_rows': {
                                'properties': {
                                    'test_property': test_property,
                                    'test_date': test_date,
                                    'test_time': test_time
                                }
                            },
                            'data_columns': {
                                'properties': {
                                    'a header for this table': {
                                        'properties': {
                                            'test_property': test_property,
                                            'test_date': test_date,
                                            'test_time': test_time
                                        }
                                    },
                                    'a header for this adjacent table': {
                                        'properties': {
                                            'test_property': test_property,
                                            'test_date': test_date,
                                            'test_time': test_time
                                        }
                                    }
                                }
                            },
                        }
                    }
                }
            }
        }
    }

    return ShippingManifest(tiny_manifest_schema)
