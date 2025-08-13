#! /usr/bin/python
# run with python label/populate_bayren_electrification_checklist.py

import os
from pdfrw import PdfWriter, PdfReader, IndirectPdfDict, PdfName, PdfDict

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_TEXT_KEY = '/Tx'
ANNOT_BUTTON_KEY = '/Btn'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'


def write_elec_checklist_pdf(input_pdf_path, data_dict, output_pdf_path):
    for key in ['waterheaterfuel']:
        data_dict[key+'_'+data_dict[key]] = 'On'
    template_pdf = PdfReader(input_pdf_path)
    form_fields = template_pdf.Root.AcroForm.Fields
    for field in form_fields:
        if field[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
            if field[ANNOT_FIELD_KEY]:
                key = field[ANNOT_FIELD_KEY][1:-1]
                if key in data_dict:
                    if field.FT == ANNOT_TEXT_KEY:  # text entries
                        print(key)
                        field.V = data_dict[key]

                        rct = field.Rect
                        hight = round(float(rct[3]) - float(rct[1]), 2)
                        width = round(float(rct[2]) - float(rct[0]), 2)

                        # create Xobject
                        xobj = IndirectPdfDict(
                                    BBox=[0, 0, width, hight],
                                    FormType=1,
                                    Resources=PdfDict(ProcSet=[PdfName.PDF, PdfName.Text]),
                                    Subtype=PdfName.Form,
                                    Type=PdfName.XObject
                                    )

                        # assign a stream to it
                        xobj.stream = '''/Tx BMC
                        BT
                         /Helvetica 10.0 Tf
                         1.0 2.0 Td
                         0 g
                         (''' + data_dict[key] + ''') Tj
                        ET EMC'''

                        # put all together
                        field.AP = PdfDict(N=xobj)
                    elif field.FT == ANNOT_BUTTON_KEY:  # checkboxes
                        print(key)
                        print(data_dict[key])
                        field.update({
                            PdfName("V"): PdfName(data_dict[key]),
                            PdfName("DV"): PdfName(data_dict[key]),
                            PdfName("AS"): PdfName(data_dict[key]),
                            PdfName("DA"): PdfName('/ZapfDingbatsITC 12 Tf 0 g')
                        })
                        print(field)

#    if output_pdf_path:
    PdfWriter().write(output_pdf_path, template_pdf)
#        return True
#    else:
#        return template_pdf


### FIELD NAMES, DO NOT DELETE


# Run with:  python3 -m label.populate_bayren_electrification_checklist
if __name__ == '__main__':
    data_dict = {
        'address': '123 Main St',
        'city': 'Cambridge',
        'waterheaterfuel': 'ng',
        'ngbs_silver': 'On',
        'green_certification_date_verified': '01/01/20',
    }
    
    module_path = os.path.abspath(os.path.dirname(__file__))
    in_path = os.path.normpath(os.path.join(module_path, "./templates/"))
    out_path = os.path.normpath(os.path.join(module_path, "./tmp/"))
    in_file = in_path + '/BayREN_Electrification_Checklist.pdf'
    out_file = out_path + '/Elec_Checklist_out.pdf'
    write_elec_checklist_pdf(in_file, data_dict, out_file)
