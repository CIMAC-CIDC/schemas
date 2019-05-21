# -*- coding: utf-8 -*-

"""The underlying data representation of an assay or shipping manifest template."""

import logging
import json
from typing import List, Optional, Dict
from collections import OrderedDict

from .json_validation import load_and_validate_schema

logger = logging.getLogger('cidc_schemas.template')


class Template:
    """
    Configuration describing a manifest or assay template

    Properties:
        template_schema {dict} -- a validated template JSON schema
        worksheets {Dict[str, dict]} -- a mapping from worksheet names to worksheet schemas
    """

    def __init__(self, template_schema: dict):
        """
        Load the schema defining a manifest or assay template.

        Arguments:
            template_schema {dict} -- a valid JSON schema describing a template
        """
        self.template_schema = template_schema
        self.worksheets = self._extract_worksheets()

    def _extract_worksheets(self) -> Dict[str, dict]:
        """Build a mapping from worksheet names to worksheet section schemas"""

        template_id = self.template_schema['$id']
        assert 'worksheets' in self.template_schema[
            'properties'], f'{template_id} schema missing "worksheets" property'
        worksheet_schemas = self.template_schema['properties']['worksheets']

        worksheets = {}
        for name, schema in worksheet_schemas.items():
            self._validate_worksheet(name, schema)
            worksheets[name] = schema

        return worksheets

    # XlTemplateReader only knows how to format these types of sections
    VALID_WS_SECTIONS = set(['preamble_rows', 'data_columns'])

    @staticmethod
    def _validate_worksheet(ws_title: str, ws_schema: dict):
        # Ensure all worksheet sections are supported
        ws_sections = set(ws_schema.keys())
        unknown_props = ws_sections.difference(
            Template.VALID_WS_SECTIONS)
        assert not unknown_props, \
            f'unknown worksheet sections {unknown_props} - only {Template.VALID_WS_SECTIONS} supported'

    @staticmethod
    def from_json(template_schema_path: str, schema_root: str):
        """
        Load a Template from a template schema.

        Arguments:
            template_schema_path {str} -- path to the template schema file
            schema_root {str} -- path to the directory where all schemas are stored
        """
        template_schema = load_and_validate_schema(
            template_schema_path, schema_root)

        return Template(template_schema)

    def to_excel(self, xlsx_path: str):
        """Write this `Template` to an Excel file"""
        from .template_writer import XlTemplateWriter

        XlTemplateWriter().write(xlsx_path, self)

    def validate_excel(self, xlsx_path: str) -> bool:
        """Validate the given Excel file against this `Template`"""
        from .template_reader import XlTemplateReader

        return XlTemplateReader.from_excel(xlsx_path).validate(self)


Template