# -*- coding: utf-8 -*-
#! /usr/bin/python
# run with python3 -m label.populate_remotely_ipc

import os
from reportlab.lib.enums import TA_RIGHT, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Frame, FrameBreak, HRFlowable, Image, PageTemplate,Paragraph, Spacer
from label.utils.constants import *
from label.utils.utils import ColorFrame, ColorFrameSimpleDocTemplate, validate_data_dict
import datetime

#Adding Arial Unicode for checkboxes
module_path = os.path.abspath(os.path.dirname(__file__))
FONT_PATH = os.path.normpath(os.path.join(module_path, ".fonts"))
IMG_PATH = os.path.normpath(os.path.join(module_path, "images"))
CUSTOM_DTEAL = colors.Color(red=(243.0/255),green=(243.0/255),blue=(243.0/255))

pdfmetrics.registerFont(TTFont('InterstateLight',FONT_PATH+'/InterstateLight.ttf'))
pdfmetrics.registerFont(TTFont('InterstateBlack',FONT_PATH+'/InterstateBlack.ttf'))
#pdfmetrics.registerFont(TTFont('Arial Unicode',FONT_PATH+'/Arial Unicode.ttf'))
pdfmetrics.registerFont(TTFont("FontAwesome", FONT_PATH+"/FontAwesome.ttf"))

def write_remotely_ipc_pdf(data_dict, output_pdf_path):
    """ 
    Create a PDF file of data submitted for IPC programs
    TODO: describe data_dict
    """
    doc = ColorFrameSimpleDocTemplate(output_pdf_path,pagesize=letter,rightMargin=20,leftMargin=20,topMargin=20,bottomMargin=20)
    styles = getSampleStyleSheet()                 

    Story=[]
    #Standard text formats
    tf_standard = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = FONT_H, fontName = FONT_NORMAL, textColor = CUSTOM_DGRAY, leading = 14, spaceBefore = 4, spaceAfter = 4)  
    tf_standard_bold = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = FONT_H, fontName = FONT_BOLD, textColor = CUSTOM_DGRAY, leading = 14)  
    tf_small = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = FONT_S, fontName = FONT_NORMAL, textColor = CUSTOM_DGRAY, spaceBefore = 4, spaceAfter = 4, bulletIndent = 12, leftIndent = 12)  
    tf_small_squished = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = FONT_S, fontName = FONT_NORMAL, textColor = CUSTOM_DGRAY, spaceBefore = 6, spaceAfter = 0)  
    tf_small_right = ParagraphStyle('standard', alignment = TA_RIGHT, fontSize = FONT_S, fontName = FONT_NORMAL, textColor = CUSTOM_DGRAY, spaceBefore = 6, spaceAfter = 0)  
    tf_small_bold = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = FONT_S, fontName = FONT_BOLD, textColor = CUSTOM_DGRAY, spaceBefore = 6, spaceAfter = 0)  
    
    ### P1
    # Logo
    column_10 = Frame(doc.leftMargin, doc.height-0.1*doc.height, doc.width/3-12, 0.13*doc.height, showBoundary=0)    
    vthep_logo = IMG_PATH + "/IPC-logo.png"
    im = Image(vthep_logo, 2.5*inch, 0.675*inch) #max is 1.1 inch height
    Story.append(im)
    Story.append(FrameBreak)
    
    # Text Column
    column_12 = ColorFrame(doc.leftMargin, doc.bottomMargin, doc.width/3-12, 0.87*doc.height, showBoundary=0, roundedBackground=CUSTOM_LGRAY, topPadding=10)
    pc12 = ParagraphStyle('column_1', alignment = TA_LEFT, fontSize = FONT_ML, fontName = FONT_BOLD, textColor = CUSTOM_DTEAL, leading = 14, spaceBefore = 16)
    pc13 = ParagraphStyle('column_1', alignment = TA_LEFT, fontSize = FONT_H, fontName = FONT_BOLD, textColor = CUSTOM_DGRAY, leading = 12, spaceBefore = 4)
    pc14 = ParagraphStyle('column_1', alignment = TA_LEFT, fontSize = FONT_T, fontName = FONT_NORMAL, textColor = CUSTOM_DGRAY, leading = 12)
    
    Story.append(Paragraph("This report summarizes inspection findings for the IPC SMARTE program", tf_standard))
    Story.append(Spacer(1,16))
    Story.append(HRFlowable(width="90%", thickness=1, lineCap='round', color=colors.white, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))
    Story.append(Paragraph("BUILDING INFORMATION", pc12))
    Story.append(Paragraph("LOCATION:", pc13))
    Story.append(Paragraph(data_dict['street'],pc14))
    Story.append(Paragraph(data_dict['city'] + ", " + data_dict["state"] + " " + data_dict["zipcode"], pc14))
    Story.append(Paragraph("YEAR BUILT:", pc13))
    Story.append(Paragraph(str(int(data_dict['year_built'])),pc14))
    # Story.append(Paragraph("PROPERTY TYPE:", pc13))
    # Story.append(Paragraph(data_dict['systemDefinedPropertyType'],pc14))
    Story.append(Spacer(1,16))
    Story.append(HRFlowable(width="90%", thickness=1, lineCap='round', color=colors.white, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))
    Story.append(Paragraph("REPORT INFORMATION", pc12))
    Story.append(Paragraph("CREATION DATE:", pc13))
    Story.append(Paragraph(datetime.datetime.now().strftime("%m/%d/%Y"),pc14))
    Story.append(Spacer(1,16))
    Story.append(HRFlowable(width="90%", thickness=1, lineCap='round', color=colors.white, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))
    Story.append(Paragraph("Brought to you by Remotely", tf_small))
    Story.append(FrameBreak)
    
    # Column 2 (Question Groups)
    column_20 = Frame(doc.leftMargin+doc.width/3, doc.bottomMargin, (2/3)*doc.width, doc.height, showBoundary=0, topPadding=10)    
    pc201 = ParagraphStyle('column_2', alignment = TA_LEFT, fontSize = FONT_L, fontName = FONT_BOLD, textColor = CUSTOM_DGRAY, spaceAfter=6)
    pc202 = ParagraphStyle('body_left', alignment = TA_LEFT, textColor = CUSTOM_DGRAY, fontSize = FONT_T, fontName = FONT_NORMAL,  spaceBefore = 6, spaceAfter = 0, leading=10, backColor = 'white', bulletIndent = 12, firstLineIndent = 0, leftIndent = 12, rightIndent = 0)
    question_answers = data_dict['question_answers']
    if not isinstance(question_answers, list):
        raise ValueError('question_answers must be a list')
    
    REQUIRED_KEYS = ['question_group', 'question', 'answer']
    for qa in question_answers:
        if not all(k in qa for k in REQUIRED_KEYS):
            raise ValueError('question_answer dictionary must contain question_group')
        
    question_answers_by_group = { qa['question_group']: [] for qa in question_answers }

    for qa in question_answers:
        question_answers_by_group[qa['question_group']].append(qa)
        
    for (question_group, qas) in question_answers_by_group.items():
        Story.append(Paragraph(question_group, pc201))
        for qa in qas:
            Story.append(Paragraph(qa['question'], tf_standard))
            answer = qa['answer']

            date_answer = get_date_string(answer)
            if date_answer:
                Story.append(Paragraph(date_answer, tf_small))
            elif isinstance(answer, str):
                Story.append(Paragraph(answer, tf_small))
            elif isinstance(answer, list):
                options = qa['options'] if qa['options'] else answer
                for a in options:
                    bullet = CHECK.encode('UTF8') if a in answer else '   '
                    # Factor out code that formats scalar quantities
                    Story.append(Paragraph(a, tf_small, bulletText=bullet))
                    
        Story.append(Spacer(1,16))

### BUILD PAGE
    page_1_frames = [column_10, column_12, column_20]
    templates =[]
    templates.append(PageTemplate(frames=page_1_frames,id='firstPage'))
    doc.addPageTemplates(templates)
    style = styles["Normal"]

    #populate story with paragraphs    
    doc.build(Story)
    
def get_date_string(answer):
    """ Get a string from an answer if the answer is an ISO date string """
    try:
        return datetime.datetime.fromisoformat(answer).date().strftime("%m/%d/%Y")
    except (ValueError, TypeError):
        return None

# Run with:  python3 -m label.populate_remotely_ipc
if __name__ == '__main__':
    question_answers = [
        {
            # This results in a text input
            "question_group": "Assessment Info",
            "question": "What is the name of the inspector?",
            "answer": "Marc Maron"
        },
        {
            # This results in a date input
            "question_group": "Assessment Info",
            "question": "What is the date of the inspection?",
            # Date MUST be ISO8601 or function assumes plain text.
            "answer": "2025-01-27T13:56:12Z"
        },
        {
            # This results in a radio (single-select) input
            "question_group": "Other Hot Water Heaters",
            "question": "Does the natural gas, on-demand, tankless water heater have an energy factor of 0.94 or greater?",
            "options": ["Yes", "No"],
            "answer": "Yes"
        },
        {
            # This results in a checkbox (multi-select) input
            "question_group": "Other Hot Water Heaters",
            "question": "What type of other hot water heater was installed?",
            "options": ["Natural Gas Condensing or Storage", "Natural Gas Tankless", "Propane Tankless"],
            "answer": ["Natural Gas Tankless", "Propane Tankless"]
        }
    ]
    data_dict = {
        'street': '77 MASSACHUSETTS AVE', 
        'city': 'CAMBRIGE', 
        'state': 'MA', 
        'zipcode': '02139', 
        'year_built': 1895,
        'program_name': 'SMARTEPV',
        'question_answers': question_answers
    }
    out_file = 'Remotely_IPC_Inspection_Report.pdf'
    write_remotely_ipc_pdf(data_dict, out_file)