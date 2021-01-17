# -*- coding: utf-8 -*-
#! /usr/bin/python
# run with python label/populate_vermont_energy_profile.py

import datetime
import os
import sys
import time
from label.utils.utils import ColorFrame, ColorFrameSimpleDocTemplate
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm, mm
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer,Table,TableStyle, BaseDocTemplate, Frame, PageTemplate, FrameBreak, NextPageTemplate, PageBreak
from reportlab.rl_config import defaultPageSize


sys.path.insert(0,'./utils')

PAGE_HEIGHT=defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()

module_path = os.path.abspath(os.path.dirname(__file__))
FONT_PATH = os.path.normpath(os.path.join(module_path, ".fonts"))
IMG_PATH = os.path.normpath(os.path.join(module_path, "images"))

def write_energy_first_mortgage_pdf(data_dict, out_file):
    ''' creates the pdf using frames '''
    address_line_1 = data_dict['address_line_1']
    address_line_2 = '' if data_dict['address_line_2'] is None else data_dict['address_line_2']
    city=data_dict['city']
    state = data_dict['state']
    postal_code= data_dict['postal_code']
#    address = '<font  name=Times-Roman size=9 color=#4e4e52>{}{}, {}, {}, {}</font>'.format(address_line_1,address_line_2,city,state,postal_code)
#    address_p = Paragraph(address,styles['Normal'])
    now = datetime.datetime.now()
    year = '{:02d}'.format(now.year)
    
    Story = []
    document = ColorFrameSimpleDocTemplate(out_file,pagesize=letter,rightMargin=20,leftMargin=20,topMargin=20,bottomMargin=20)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='line-height',leading=13))
    cell_center = ParagraphStyle('cell_center', alignment = TA_CENTER)
    cell_left = ParagraphStyle('cell_center', alignment = TA_LEFT)
    
    header_frame = Frame(document.leftMargin,document.height-0.10*document.height,document.width,0.10*document.height, showBoundary=1)
    hp1 = Paragraph('''<font name=Helvetica size=18>EnergyFirst Mortgage Program Summary Form</font>''',styles['Heading1'])
    Story.append(hp1)
    hp2 = Paragraph("<font name=helvetica size=9><i>This Form summarizes the scope of work and cost for the energy improvements for the subject property and serves as the agreement between all parties to enable the EnergyFirst Mortgage to proceed.</i></font>",styles['line-height'])          
    Story.append(hp2)
    Story.append(FrameBreak)

    customer_tableStyle = TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID',(0,0),(-1,-1),0.5,colors.gray),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ])

    customer_frame = Frame(document.leftMargin,document.height-0.25*document.height,document.width,0.15*document.height, showBoundary=1)
    customer_header_p = Paragraph("<font name=Helvetica-Bold size=11>Customer</font>",styles['Heading2'])
    Story.append(customer_header_p)
    customer_table = Table([['Name',data_dict['customer_name']],['Property Address (street, city, zip, state)',''],['Mailing Address (street, city, zip, state)','']], colWidths = [2.5*inch, 5.0*inch], hAlign = 'LEFT')
    customer_table.setStyle(customer_tableStyle)
    Story.append(customer_table)
    customer_subtable = Table([['Phone #',data_dict['customer_phone'],'Email',data_dict['customer_email']]], colWidths = [1.75*inch, 2.0*inch, 1.75*inch, 2.0*inch], hAlign = 'LEFT')
    customer_subtable.setStyle(customer_tableStyle)
    Story.append(customer_subtable)
    Story.append(FrameBreak)
    
    contractor_frame = Frame(document.leftMargin,document.height-0.37*document.height,document.width,0.12*document.height, showBoundary=1)
    contractor_header_p = Paragraph("<font name=Helvetica-Bold size=11>Contractor</font>",styles['Heading2'])
    Story.append(contractor_header_p)
    contractor_table = Table([['Name',data_dict['contractor_name']],['Company Name',data_dict['contractor_company']],['Phone #',data_dict['contractor_phone']]], colWidths = [2.5*inch, 5.0*inch], hAlign = 'LEFT')
    contractor_table.setStyle(customer_tableStyle)
    Story.append(contractor_table)
    Story.append(FrameBreak)
    
    originator_frame = Frame(document.leftMargin,document.height-0.47*document.height,document.width,0.10*document.height, showBoundary=1)
    originator_header_p = Paragraph("<font name=Helvetica-Bold size=11>VSECU Originator</font>",styles['Heading2'])
    Story.append(originator_header_p)
    originator_table = Table([['Name',data_dict['originator_name']],['Phone #',data_dict['originator_phone']]], colWidths = [2.5*inch, 5.0*inch], hAlign = 'LEFT')
    originator_table.setStyle(customer_tableStyle)
    Story.append(originator_table)
    Story.append(FrameBreak)
    
    coach_frame = Frame(document.leftMargin,document.height-0.57*document.height,document.width,0.10*document.height, showBoundary=1)
    coach_header_p = Paragraph("<font name=Helvetica-Bold size=11>Energy Coach (Energy Futures Group)</font>",styles['Heading2'])
    Story.append(coach_header_p)
    coach_table = Table([['Name',data_dict['coach_name']],['Phone #',data_dict['coach_phone']]], colWidths = [2.5*inch, 5.0*inch], hAlign = 'LEFT')
    coach_table.setStyle(customer_tableStyle)
    Story.append(coach_table)
    Story.append(FrameBreak)

    work_frame = Frame(document.leftMargin,document.height-0.94*document.height,document.width,0.37*document.height, showBoundary=1)
    work_header_p = Paragraph("<font name=Helvetica-Bold size=12>Scope of Work</font>",styles['Heading2'])
    Story.append(work_header_p)
    work_text = Paragraph("<font name=helvetica size=9><i>Energy improvement and energy barrier remediation measures agreed to by the contractor and borrower(s) that will total at least 10% of the mortgage amount.</i></font>",styles['line-height'])          
    Story.append(work_text)
    work_table = Table([['#','Measure Description','Cost']], colWidths = [0.5*inch, 5.0*inch, 2.0*inch], hAlign = 'LEFT')
    work_table.setStyle(customer_tableStyle)
    Story.append(work_table)
    #iterate through measures
    item_num = 1
    cost_sum = 0
    for name, value in data_dict['measures'].items():
        c3 = Paragraph("${:,}".format(int(value)), cell_left)
        work_subtable = Table([[item_num, name, c3]], colWidths = [0.5*inch, 5.0*inch, 2.0*inch], hAlign = 'LEFT')
        work_subtable.setStyle(customer_tableStyle)
        Story.append(work_subtable)
        item_num += 1
        cost_sum += value
    c3 = Paragraph("${:,}".format(int(cost_sum)), cell_left)
    work_subtable = Table([['', 'Total', c3]], colWidths = [0.5*inch, 5.0*inch, 2.0*inch], hAlign = 'LEFT')
    work_subtable.setStyle(customer_tableStyle)
    Story.append(work_subtable)
    c3 = Paragraph("${:,}".format(int(data_dict['mortgage'])), cell_left)
    work_subtable = Table([['', 'Total Mortgage Loan Amount', c3]], colWidths = [0.5*inch, 5.0*inch, 2.0*inch], hAlign = 'LEFT')
    work_tableStyle = TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ])
    work_subtable.setStyle(work_tableStyle)
    Story.append(work_subtable)
    c3 = Paragraph("{:,.1f}%".format(100.0 * cost_sum / data_dict['mortgage']), cell_left)
    work_subtable = Table([['', 'Energy Improvement Package Cost as a Percent of Total Loan Amount:', c3]], colWidths = [0.5*inch, 5.0*inch, 2.0*inch], hAlign = 'LEFT')
    work_subtable.setStyle(work_tableStyle)
    Story.append(work_subtable)
    Story.append(FrameBreak)
    
    #  FOOTER FRAME
    footer_version = Paragraph('''<font size=8 color=#736d5e>v.12/4/2020</font>''',styles['Normal'])
    footer_address_p = Paragraph('''<font size=8 color=#736d5e>EnergyFirst Mortgage Program Summary Form</font>''',styles['Normal'])
    footer_data = [[footer_version,'','','',footer_address_p]]
    footer_table = Table(footer_data)
    footer_table_style = TableStyle([('RIGHTPADDING',(4,0),(4,0),0),
                                    ('LEFTPADDING',(0,0),(0,0),0),
                                    ('SPAN',(0,0),(3,0)),
                                    ('ALIGN',(0,0),(0,0),'LEFT'),
                                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                                    ('ALIGN',(-1,-1),(-1,-1),'RIGHT'),
                                    ('RIGHTPADDING',(-1,-1),(-1,-1),0),
                                   
                                    ])
    footer_table.setStyle(footer_table_style)
    footer_frame = Frame(document.leftMargin,document.height-0.999*document.height,document.width,0.06*document.height, showBoundary=1)
    Story.append(footer_table)
    
    #### SETTING UP FRAMES FOR PAGE 2
    Story.append(NextPageTemplate('secondPage'))
    Story.append(FrameBreak)
    energy_savings_frame = Frame(document.leftMargin,document.height-0.16*document.height,document.width,0.16*document.height, showBoundary=0)
    savings_header_p = Paragraph("<font name=Helvetica-Bold size=11>Energy Savings Information</font>",styles['Heading2'])
    Story.append(savings_header_p)
    
    h12 = Paragraph('<font name=Helvetica-Bold><strong>Existing Home</strong></font>',styles['Normal'])
    h13 = Paragraph('<font name=Helvetica-Bold><strong>Upgraded Home</strong></font>',styles['Normal'])
    h14 = Paragraph('<font name=Helvetica-Bold><strong>Improvement</strong></font>',styles['Normal'])
    h21 = Paragraph('<font name=Helvetica-Bold><strong>Annual Energy Cost</strong></font>',styles['Normal'])
    h31 = Paragraph('<font name=Helvetica-Bold><strong>US DOE Home Energy Score (1-10)</strong></font>',styles['Normal'])
    c22 = Paragraph('$'+str(int(data_dict['cost_pre'])), cell_center)
    c23 = Paragraph('$'+str(int(data_dict['cost_post'])), cell_center)
    c24 = Paragraph('$'+str(int(data_dict['cost_pre'] - data_dict['cost_post'])), cell_center)
    
    savings_table = Table([['',h12,h13,h14], [h21, c22, c23,c24], [h31, data_dict['hes_pre'],data_dict['hes_post'],data_dict['hes_post']-data_dict['hes_pre']]], colWidths = [2.0*inch, 1.8*inch, 1.8*inch, 1.8*inch])
    savings_tableStyle = TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('GRID',(0,0),(-1,-1),0.5,colors.gray),
    ])
    savings_table.setStyle(savings_tableStyle)       
    Story.append(savings_table)
    
    Story.append(FrameBreak)

    approval_frame = Frame(document.leftMargin,document.height-0.34*document.height,document.width,0.20*document.height, showBoundary=0)
    approval_header_p = Paragraph("<font name=Helvetica-Bold size=11>Customer Approval</font>",styles['Heading2'])
    Story.append(approval_header_p)
    approval_text1 = '''<font name=Helvetica size=8>I certify that I meet the eligibility requirements of this loan program, that all information submitted as part of this form is correct to the best of my knowledge and that I accept the Terms & Conditions. I agree to allow VSECU to share project information with Energy Future Group.</font>'''
    approval_text1_p = Paragraph(approval_text1, styles['line-height'])
    Story.append(approval_text1_p)
    Story.append(Spacer(1, 24))
    
    signature_table = Table([['Customer Signature','','Date']], colWidths = [3.0*inch, 1.0*inch,3.0*inch])
    signature_tableStyle = TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('LINEABOVE',(0,0),(0,-1),1, colors.gray),
        ('LINEABOVE',(2,0),(-1,-1),1, colors.gray),
    ])
    signature_table.setStyle(signature_tableStyle)       
    Story.append(signature_table)
    Story.append(Spacer(1,24))
    Story.append(signature_table)
    Story.append(FrameBreak)

    agreement_frame = Frame(document.leftMargin,document.height-0.48*document.height,document.width,0.14*document.height, showBoundary=0)
    agreement_header_p = Paragraph("<font name=Helvetica-Bold size=11>Contractor Agreement</font>",styles['Heading2'])
    Story.append(agreement_header_p)
    agreement_text1 = '''<font name=Helvetica size=8>I certify that I have provided an accurate scope of work and price quote that meets the EnergyFirst Mortgage Program requirements. I agree to report project information to VSECU and Energy Futures Group.</font>'''
    agreement_text1_p = Paragraph(agreement_text1, styles['line-height'])
    Story.append(agreement_text1_p)
    Story.append(Spacer(1, 20))
    
    signature_table = Table([['Contractor Signature','','Date']], colWidths = [3.0*inch, 1.0*inch,3.0*inch])
    signature_tableStyle = TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('LINEABOVE',(0,0),(0,-1),1, colors.gray),
        ('LINEABOVE',(2,0),(-1,-1),1, colors.gray),
    ])
    signature_table.setStyle(signature_tableStyle)       
    Story.append(signature_table)
    
    Story.append(FrameBreak)
       
    page2_terms = ColorFrame(document.leftMargin,document.height-0.88*document.height,document.width,0.4*document.height, showBoundary=0)
    terms_header_p = Paragraph("<font name=Helvetica-Bold size=11>Terms & Conditions</font>",styles['Heading2'])
    Story.append(terms_header_p)
    terms_text1 = '''<font name=Helvetica size=8><strong>Eligibility:</strong> Project must be installed at a Vermont residential home, owned and occupied by the borrower, containing one to four family housing units; property taxes must be paid and up to date, and the home must not be an asset in a pending bankruptcy, legal, or divorce proceeding. Lenders may limit eligibility subject to limitations or guidelines established by HUD and/or other underwriting criteria. Improvements must be permanently attached to participating property and aim to reduce the net energy requirements of the participating property. Scope of work must be developed, and work must be overseen by a BPI-certified Efficiency Excellence Network contractor. Eligible items covered by the EnergyFirst Mortgage include the cost of labor, installation, equipment, materials, efficiency-related health and safety repairs, taxes, shipping, any permit or loan application fees, and applicable audit, assessment and inspection charges.</font>'''
    terms_text1_p = Paragraph(terms_text1, styles['line-height'])
    Story.append(terms_text1_p)
    terms_text2 = '''<font name=Helvetica size=8><strong>Loan limits:</strong> Minimum of 10% of total mortgage amount.</font>'''
    terms_text2_p = Paragraph(terms_text2, styles['line-height'])
    Story.append(terms_text2_p)
    terms_text3 = '''<font name=Helvetica size=8><strong>Disclaimer of warranties and limitation of liability:</strong> Neither VSECU nor Energy Futures Group (EFG) warrant the performance of installed equipment expressly or implicitly for fitness for a particular purpose or for any specific level of energy savings, nor do they warrant that the equipment or its installation complies with any specifications, laws, regulations, codes, or standards. Neither VSECU nor EFG will be liable for any incidental or consequential damages of any kind in connection with the installation, implementation, or use of the improvements.</font>'''
    terms_text3_p = Paragraph(terms_text3, styles['line-height'])
    Story.append(terms_text3_p)
    terms_text4 = '''<font name=Helvetica size=8><strong>Endorsement:</strong> VSECU and EFG do not endorse any particular manufacturer’s product or system design in providing this financing opportunity. </font>'''
    terms_text4_p = Paragraph(terms_text4, styles['line-height'])
    Story.append(terms_text4_p)
    terms_text5 = '''<font name=Helvetica size=8><strong>Terms:</strong> This form is for {} loan applications. Loan offer is subject to available funding, and interest rates and other terms are subject to change without prior notice. Depending on credit score, some applicants may qualify for lower rates on other loan products.</font>'''.format(year)
    terms_text5_p = Paragraph(terms_text5, styles['line-height'])
    Story.append(terms_text5_p)
    terms_text6 = '''<font name=Helvetica size=8><strong>Information Release:</strong> The enrollee hereby authorizes VSECU and EFG to release information for the purpose of assisting real estate appraisers and realtors in the development of accurate home appraisals. Requests by enrollees to withhold such release will be honored, providing such notification is received prior to completion of HERS documentation.</font>'''
    terms_text6_p = Paragraph(terms_text6, styles['line-height'])
    Story.append(terms_text6_p)
    terms_header_p2 = Paragraph("<font name=Helvetica-Bold size=11>Other Comments</font>",styles['Heading2'])
    Story.append(terms_header_p2)
    #add line    
    Story.append(FrameBreak)
        
    page2_internal_frame = ColorFrame(document.leftMargin,document.height-0.94*document.height,document.width,0.06*document.height, showBoundary=0,background='#f2f1ef')
    f1_header1 = "<font name=Helvetica-Bold size=11>For Internal Use</font>"
    f1_header1_p = Paragraph(f1_header1,styles['Heading2'])
    Story.append(f1_header1_p)
    Story.append(FrameBreak)
    
    page2_footer_frame = Frame(document.leftMargin,document.height-0.999*document.height,document.width,0.06*document.height, showBoundary=0)
    # Story.append(Spacer(1,8))
    Story.append(footer_table)
    
    page_1_frames = [header_frame, customer_frame, contractor_frame, originator_frame, coach_frame, work_frame, footer_frame]
    page_2_frames = [energy_savings_frame, approval_frame, agreement_frame, page2_terms, page2_internal_frame, page2_footer_frame]
    templates =[]
    templates.append(PageTemplate(frames=page_1_frames,id='firstPage'))
    templates.append(PageTemplate(frames=page_2_frames,id='secondPage'))
    document.addPageTemplates(templates)

    style = styles["Normal"]

      #populate story with paragraphs    
    document.build(Story)

# Run with:  python3 -m label.populate_energy_first_mortgage
if __name__ == '__main__':
    data_dict ={'address_line_1': '34 Somerset Rd', 'address_line_2': None, 'city': 'Montpelier', 'state': 'VT', 'postal_code': '05602', 
    'hes_pre': 5, 'hes_post': 10, 'cost_pre': 3000, 'cost_post': 1000, 
    'coach_name': 'Richard Faesy', 'coach_phone': '444-444-4444', 
    'originator_name': 'Joe Banker', 'originator_phone': '555-555-5555',
    'contractor_name': 'Gabrielle Contractor', 'contractor_company': 'Contractor Co.', 'contractor_phone': '123-456-7890', 
    'customer_name': 'Handy Andy', 'customer_phone': '111-111-1111', 'customer_email': 'handy@andy.com', 
    'measures': {'Solar Photovoltaic': 25000, 'Garage Insulation': 2345}, 'mortgage': 100000} 
    out_file = 'EFMLabel.pdf'
    write_energy_first_mortgage_pdf(data_dict, out_file) 
  