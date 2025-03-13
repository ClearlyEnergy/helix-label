# -*- coding: utf-8 -*-
#! /usr/bin/python
# run with python3 -m label.populate_remotely_ipc

import os
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Frame, FrameBreak, HRFlowable, Image, PageTemplate,Paragraph, Spacer
from label.utils.constants import *
from label.utils.utils import ColorFrame, ColorFrameSimpleDocTemplate
import datetime

#Adding Arial Unicode for checkboxes
module_path = os.path.abspath(os.path.dirname(__file__))
FONT_PATH = os.path.normpath(os.path.join(module_path, ".fonts"))
IMG_PATH = os.path.normpath(os.path.join(module_path, "images"))
CUSTOM_DTEAL = colors.Color(red=(243.0/255),green=(243.0/255),blue=(243.0/255))

pdfmetrics.registerFont(TTFont('InterstateLight', FONT_PATH+'/InterstateLight.ttf'))
pdfmetrics.registerFont(TTFont('InterstateBlack', FONT_PATH+'/InterstateBlack.ttf'))
pdfmetrics.registerFont(TTFont("FontAwesome", FONT_PATH+"/FontAwesome.ttf"))

def write_remotely_ipc_pdf(data_dict, output_pdf_path):
    """
    Create a PDF file of data submitted for IPC programs
    
    :param dict data_dict: The data required to construct the IPC PDF. See the main function
    in this file for example of input dictionary.
    :param str output_pdf_path: A local file path where the resultant file will be written.    
    """
    doc = ColorFrameSimpleDocTemplate(output_pdf_path,pagesize=letter,rightMargin=20,leftMargin=20,topMargin=20,bottomMargin=20)

    Story=[]
    #Standard text formats
    title_font = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = FONT_XL, fontName = FONT_NORMAL, textColor = CUSTOM_DGRAY, leading = 20, spaceBefore = 20, spaceAfter = 20)
    tf_standard = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = FONT_H, fontName = FONT_NORMAL, textColor = CUSTOM_DGRAY, leading = 14, spaceBefore = 4, spaceAfter = 4)
    tf_small = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = FONT_S, fontName = FONT_NORMAL, textColor = CUSTOM_DGRAY, spaceBefore = 4, spaceAfter = 4, bulletIndent = 12, leftIndent = 12)  

    ### P1
    # Logo
    column_10 = Frame(doc.leftMargin, doc.height-0.1*doc.height, doc.width/3-12, 0.13*doc.height, showBoundary=0)    
    vthep_logo = IMG_PATH + "/IPC-Logo.png"
    im = Image(vthep_logo, 2.5*inch, 0.675*inch) #max is 1.1 inch height
    Story.append(im)
    Story.append(FrameBreak)
    
    # Text Column
    column_12 = ColorFrame(doc.leftMargin, doc.bottomMargin, doc.width/3-20, 0.87*doc.height, showBoundary=0, roundedBackground=CUSTOM_LGRAY, topPadding=10)
    pc12 = ParagraphStyle('column_1', alignment = TA_LEFT, fontSize = FONT_ML, fontName = FONT_BOLD, textColor = CUSTOM_DTEAL, leading = 14, spaceBefore = 4)
    pc13 = ParagraphStyle('column_1', alignment = TA_LEFT, fontSize = FONT_H, fontName = FONT_BOLD, textColor = CUSTOM_DGRAY, leading = 12, spaceBefore = 4)
    pc14 = ParagraphStyle('column_1', alignment = TA_LEFT, fontSize = FONT_T, fontName = FONT_NORMAL, textColor = CUSTOM_DGRAY, leading = 12)
    
    program_display_name = data_dict['program_display_name']
    Story.append(Paragraph(f"This report summarizes inspection findings for an <font name='InterstateBlack'>{program_display_name}</font> inspection.", tf_standard))
    Story.append(Spacer(1,16))
    Story.append(HRFlowable(width="90%", thickness=1, lineCap='round', color=colors.white, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))
    Story.append(Paragraph("BUILDING INFORMATION", pc12))
    Story.append(Paragraph("LOCATION:", pc13))
    Story.append(Paragraph(data_dict['street'],pc14))
    Story.append(Paragraph(data_dict['city'] + ", " + data_dict["state"] + " " + data_dict["zipcode"], pc14))
    Story.append(Paragraph("YEAR BUILT:", pc13))
    Story.append(Paragraph(str(int(data_dict['year_built'])),pc14))
    Story.append(Spacer(1,16))
    Story.append(HRFlowable(width="90%", thickness=1, lineCap='round', color=colors.white, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))
    Story.append(Paragraph("REPORT INFORMATION", pc12))
    Story.append(Paragraph("CREATION DATE:", pc13))
    Story.append(Paragraph(datetime.datetime.now().strftime("%m/%d/%Y"),pc14))
    Story.append(Spacer(1,16))
    Story.append(HRFlowable(width="90%", thickness=1, lineCap='round', color=colors.white, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))
    remotely_logo = os.path.join(IMG_PATH, "PoweredByRemotely.png")
    Story.append(Spacer(1,16))
    im = Image(remotely_logo, 2.0*inch, 0.675*inch, kind='proportional')
    Story.append(im)
    Story.append(FrameBreak)
    
    # Column 2 (Question Groups)
    column_20 = Frame(doc.leftMargin+doc.width/3, doc.bottomMargin, (2/3)*doc.width, doc.height, showBoundary=0, topPadding=10)    
    Story.append(Paragraph(f"{program_display_name}: Report", title_font))
    pc201 = ParagraphStyle('column_2', alignment = TA_LEFT, fontSize = FONT_L, fontName = FONT_BOLD, textColor = CUSTOM_DGRAY, spaceAfter=6)
    question_answers = data_dict.get('question_answers', [])
    if not isinstance(question_answers, list):
        raise ValueError('question_answers must be a list')

    question_answers_by_group = { qa['question_group']: [] for qa in question_answers }
    for qa in question_answers:
        question_answers_by_group[qa['question_group']].append(qa)

    for (question_group, qas) in question_answers_by_group.items():
        Story.append(Paragraph(question_group, pc201))
        for qa in qas:
            Story.append(Paragraph(qa['question'], tf_standard))
            answer = qa.get('answer', 'No answer provided')
            date_answer = get_date_string(answer)

            if qa.get('data_type', None) == 'photo':
                images = qa.get('answer', [])
                if isinstance(images, list):
                    for fp in images:
                        im = Image(fp, width=2*inch,height=1*inch,kind='proportional')
                        Story.append(im)
            elif date_answer:
                Story.append(Paragraph(date_answer, tf_small))
            elif isinstance(answer, (str, int, float)):
                Story.append(Paragraph(str(answer), tf_small))
            elif isinstance(answer, list):
                options = qa.get('options', answer)
                for a in options:
                    bullet = CHECK.encode('UTF8') if a in answer else '   '
                    Story.append(Paragraph(a, tf_small, bulletText=bullet))

        Story.append(Spacer(1,16))

    # BUILD PAGE
    page_1_frames = [column_10, column_12, column_20]
    templates =[]
    templates.append(PageTemplate(frames=page_1_frames,id='firstPage'))
    doc.addPageTemplates(templates)

    #populate story with paragraphs
    doc.build(Story)

def get_date_string(answer):
    """ Get a string from an answer if the answer is an ISO8601 date string """
    try:
        return datetime.datetime.fromisoformat(answer).date().strftime("%m/%d/%Y")
    except (ValueError, TypeError):
        return None

# Run with:  python3 -m label.populate_remotely_ipc
if __name__ == '__main__':
    question_answers = [
        {
            # This results in a checkbox (multi-select) input
            "question_group": "Installations",
            "question": "Select all systems which have been installed for this home.",
            "options": ["Air Sealing", "Air source heat pump", "Central air conditioning", "Ductless mini split heat pump", "Ducts", "Ground water source heat pump", "Heat pump hot water heater", "Heating system", "High efficiency insulation", "Indirect hot water heater", "Other hot water heaters", "Smart meters", "Window retrofits"],
            "answer": ["Other hot water heaters", "Window retrofits"]
        },
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
            "question_group": "Assessment Info",
            "question": "What is the name of the customer?",
            "answer": "Sam Harris"
        },
        {
            "question_group": "Assessment Info",
            "question": "Is the inverter consistent with the manufacturer specifications?",
            "options": ["Yes", "No"],
            "answer": ["Yes"]
        },
        {
            "question_group": "Window Retrofits (1/2)",
            "question": "What is the make of the installed windows?",
            "answer": 'ClearlyEnergy Windows'
        },
        {
            "question_group": "Window Retrofits (1/2)",
            "question": "What is the model name of the installed windows?",
            "answer": 'Clear & Efficienct'
        },
        {
            "question_group": "Window Retrofits (1/2)",
            "question": "What is the area of the window in square feet?",
            "answer": 8.8
        },
        {
            "question_group": "Window Retrofits (1/2)",
            "question": "How many windows of this size, type, and orientation are in this home?",
            "answer": 4
        },
        {
            "question_group": "Window Retrofits (1/2)",
            "question": "Input comments about the installed window.",
            "answer": 
                """
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam vestibulum velit quam, vitae scelerisque velit semper a. Pellentesque porta orci ac justo posuere, in elementum nisl condimentum. Nam finibus semper laoreet. Ut volutpat tellus ut lorem commodo, non fringilla urna consectetur. Aenean mollis sit amet lorem et pellentesque. Curabitur sed leo condimentum, finibus ex eu, sagittis ipsum. Aenean sodales, mi nec mattis feugiat, diam leo maximus ligula, quis condimentum diam felis non purus. Fusce facilisis dolor enim, vel fermentum ligula venenatis vitae. Aliquam viverra sit amet nibh vel dapibus. Proin ornare diam at est lobortis, vel pellentesque nisl porta. Morbi posuere sit amet arcu sit amet tristique. Vestibulum faucibus aliquam ante eget rhoncus. In a consequat diam. Ut sit amet ultricies lectus. Aenean porta ac magna nec posuere. Cras scelerisque felis sit amet porta euismod.
                """
        },
        {
            "question_group": "Window Retrofits (2/2)",
            "question": "What is the make of the installed windows?",
            "answer": 'ClearlyEnergy Windows'
        },
        {
            "question_group": "Window Retrofits (2/2)",
            "question": "What is the model name of the installed windows?",
            "answer": 'MagicGlass'
        },
        {
            "question_group": "Window Retrofits (2/2)",
            "question": "What is the area of the window in square feet?",
            "answer": 20
        },
        {
            "question_group": "Window Retrofits (2/2)",
            "question": "How many windows of this size, type, and orientation are in this home?",
            "answer": 2
        },
        {
            "question_group": "Other Hot Water Heaters",
            "question": "Does the natural gas, on-demand, tankless water heater have an energy factor of 0.94 or greater?",
            "options": ["Yes", "No"],
            "answer": ["Yes"]
        },
        {
            # This results in a checkbox (multi-select) input
            "question_group": "Other Hot Water Heaters",
            "question": "What type of other hot water heater was installed?",
            "options": ["Natural Gas Condensing or Storage", "Natural Gas Tankless", "Propane Tankless"],
            "answer": ["Natural Gas Tankless", "Propane Tankless"]
        },
        {
            "question_group": "PV Arrays",
            "question": "Are the conduit ends weather resistant or does the junction box have strain relief connectors?",
            "options": ["Yes", "No"],
            "answer": ["Yes"]
        },
        {
            # This results in a set of images.
            "question_group": "PV Arrays",
            "question": "Take a photo of the conduit ends or junction box connectors.",
            "answer":[os.path.join(IMG_PATH, 'IPC-Logo.png'), os.path.join(IMG_PATH, 'IPC-Logo.png')],
            "data_type": "photo"
        },
        {
            "question_group": "PV Arrays",
            "question": "Is there any visible damage to modules, junction boxes, or wires present?",
            "options": ["Yes", "No"],
            "answer": ["No"]
        }
    ]
    data_dict = {
        'program_display_name': 'IPC SMARTE',
        'ce_api_id': '0123456789',
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
    