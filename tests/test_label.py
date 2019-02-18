"""Test for the label module"""
import unittest
import os

from label import label
from label.populate_residential_green_addendum import write_green_addendum_pdf
from pdfrw import PdfWriter, PdfReader, IndirectPdfDict, PdfName, PdfDict

INPUT_TEMPLATE_PATH = './templates/'
ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_TEXT_KEY = '/Tx'
ANNOT_BUTTON_KEY = '/Btn'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

class LabelTest(unittest.TestCase):

    def setUp(self):
        self.importDir = ''
        self.exportDir = ''

    def test_ga(self):
        in_file = INPUT_TEMPLATE_PATH + 'ResidentialGreenandEnergyEfficientAddendum.pdf'
        data_dict = {
            'hers_rating': '57',
            'hes_score': '6'
        }
        write_green_addendum_pdf(in_file, data_dict,'./tests/ga_test.pdf')
        template_pdf = PdfReader('./tests/ga_test.pdf')
        form_fields = template_pdf.Root.AcroForm.Fields
        for field in form_fields:
            if field[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if field[ANNOT_FIELD_KEY]:
                    key = field[ANNOT_FIELD_KEY][1:-1]
                    if key in data_dict:
                        self.assertTrue(field.V,data_dict[key]) 

