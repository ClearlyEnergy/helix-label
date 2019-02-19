#! /usr/bin/python
# run with python label/populate_residential_green_addendum.py

import os
from pdfrw import PdfWriter, PdfReader, IndirectPdfDict, PdfName, PdfDict

INVOICE_TEMPLATE_PATH = './templates/ResidentialGreenandEnergyEfficientAddendum.pdf'
INVOICE_OUTPUT_PATH = './GA_out.pdf'


ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_TEXT_KEY = '/Tx'
ANNOT_BUTTON_KEY = '/Btn'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

def write_green_addendum_pdf(input_pdf_path, data_dict, output_pdf_path):
    template_pdf = PdfReader(input_pdf_path)
    form_fields = template_pdf.Root.AcroForm.Fields
    for field in form_fields:
        if field[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
            if field[ANNOT_FIELD_KEY]:
                key = field[ANNOT_FIELD_KEY][1:-1]
                if key in data_dict:
                    if field.FT == ANNOT_TEXT_KEY: #text entries
                        field.V = data_dict[key]

                        rct = field.Rect
                        hight = round(float(rct[3]) - float(rct[1]),2)
                        width = round(float(rct[2]) - float(rct[0]),2)

                        #create Xobject
                        xobj = IndirectPdfDict(
                                    BBox = [0, 0, width, hight],
                                    FormType = 1,
                                    Resources = PdfDict(ProcSet = [PdfName.PDF, PdfName.Text]),
                                    Subtype = PdfName.Form,
                                    Type = PdfName.XObject
                                    )

                        #assign a stream to it
                        xobj.stream = '''/Tx BMC
                        BT
                         /Helvetica 10.0 Tf
                         1.0 2.0 Td
                         0 g
                         (''' + data_dict[key] + ''') Tj
                        ET EMC'''

                        #put all together
                        field.AP = PdfDict(N = xobj)
                    elif field.FT == ANNOT_BUTTON_KEY: #checkboxes
                        field.update({
                            PdfName("V"): PdfName(data_dict[key]),
                            PdfName("DV"): PdfName(data_dict[key]),
                            PdfName("AS"): PdfName(data_dict[key])
                        })

#    if output_pdf_path:
    PdfWriter().write(output_pdf_path, template_pdf)
#        return True
#    else:
#        return template_pdf
            

# sample data dictionary
data_dict = {
    'street': '296 Highland Ave',
    'street_2': '296 Highland Ave',
    'street_3': '296 Highland Ave',
    'city': 'Cambridge',
    'state': 'MA',
    'zip': '02139',
    'ngbs_silver': 'On', 
    'leed_platinum': 'On',
    'green_certification_date_verified': '01/01/20',
    'verification_attached': 'On',
    'green_certification_organization_url': 'ngbs.org',
    'hers_rating': '57',
    'hers_confirmed_rating': 'On',
    'hes_score': '6',
    'hes_official': 'On',
    'score_date_verified': '01/01/20',
    'score_version': 'v2.1',
}


#indoor_air_plus, water_sense, energy_star, zerh, 
# ngbs_bronze, ngbs_silver, ngbs_gold, ngbs_emerald
#living_building_certified
# petal_certification
# phi_low_energy
# energy_phit, passive_house
# phius_2015
# leed_certified, leed_silver, leed_gold, leed_platinum
# green_certification_date_verified
# verification_reviewed_on_site, verification_attached
# green_certification_version
# green_certification_organization_url

# hers_rating, hers_sampling_rating, hers_projected_rating, hers_confirmed_rating, hers_estimated_savings, hers_rate
# hes_score, hes_official, hes_unofficial, hes_estimated_savings, hes_rate
# score_date_verified, score_version, score_


# energy_improvement_description, cost_of_energy_improvement

#resnet_url, hes_url, other_score_url_check, other_score_url
# score_reviewed_on_site, score_attached

#solar_leased, solar_owned, solar_loan_ucc, solar_ppa
# solar_size, solar_production, solar_production_type, solar_age
# solar_fixed_mount, solar_tracking_mount
# same with _2


if __name__ == '__main__':
    write_green_addendum_pdf(INVOICE_TEMPLATE_PATH, INVOICE_OUTPUT_PATH, data_dict)