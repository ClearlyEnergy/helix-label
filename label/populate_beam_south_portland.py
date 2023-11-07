# -*- coding: utf-8 -*-
#! /usr/bin/python
# run with python3 -m label.populate_madison_orlando

import os
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Flowable, Frame, FrameBreak, HRFlowable, Image, NextPageTemplate, PageBreak, PageTemplate,Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  
from label.utils.constants import *
from label.utils.utils import ColorFrame, ColorFrameSimpleDocTemplate, Charts, Tables, Scores, Highlights, flowable_text, flowable_triangle
import datetime

#Adding Arial Unicode for checkboxes
module_path = os.path.abspath(os.path.dirname(__file__))
FONT_PATH = os.path.normpath(os.path.join(module_path, ".fonts"))
IMG_PATH = os.path.normpath(os.path.join(module_path, "images"))

pdfmetrics.registerFont(TTFont('InterstateLight',FONT_PATH+'/InterstateLight.ttf'))
pdfmetrics.registerFont(TTFont('InterstateBlack',FONT_PATH+'/InterstateBlack.ttf'))
#pdfmetrics.registerFont(TTFont('Arial Unicode',FONT_PATH+'/Arial Unicode.ttf'))
pdfmetrics.registerFont(TTFont("FontAwesome", FONT_PATH+"/FontAwesome.ttf"))
    
def write_south_portland_profile_pdf(data_dict, output_pdf_path):
    doc = ColorFrameSimpleDocTemplate(output_pdf_path,pagesize=letter,rightMargin=20,leftMargin=20,topMargin=20,bottomMargin=20)
    styles = getSampleStyleSheet()                 

    Story=[]
    #Standard text formats
    tf_standard = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = FONT_H, fontName = FONT_NORMAL, textColor = CUSTOM_DGRAY, leading = 14)  
    tf_standard_bold = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = FONT_H, fontName = FONT_BOLD, textColor = CUSTOM_DGRAY, leading = 14)  
    tf_small = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = FONT_S, fontName = FONT_NORMAL, textColor = CUSTOM_DGRAY, spaceBefore = 12, spaceAfter = 12)  
    tf_small_squished = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = FONT_S, fontName = FONT_NORMAL, textColor = CUSTOM_DGRAY, spaceBefore = 6, spaceAfter = 0)  
    tf_small_right = ParagraphStyle('standard', alignment = TA_RIGHT, fontSize = FONT_S, fontName = FONT_NORMAL, textColor = CUSTOM_DGRAY, spaceBefore = 6, spaceAfter = 0)  
    tf_small_bold = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = FONT_S, fontName = FONT_BOLD, textColor = CUSTOM_DGRAY, spaceBefore = 6, spaceAfter = 0)  
    
    ### P1
    # Logo
    column_10 = Frame(doc.leftMargin, doc.height-0.125*doc.height, doc.width/3-12, 0.13*doc.height, showBoundary=0)    
    vthep_logo = IMG_PATH+"/south_portland.jpg"
    im = Image(vthep_logo, 2.0*inch, 0.654*inch)
    Story.append(im)
    Story.append(FrameBreak)
    
    # Cost Box
    column_11 = ColorFrame(doc.leftMargin, doc.height-0.23*doc.height, doc.width/3-12, 0.13*doc.height, showBoundary=0, roundedBackground=CUSTOM_DTEAL, topPadding=10)
    text_c101, text_c102, text_c103 = Highlights.score_box(data_dict, 'ESTAR_SCORE', colors, FONT_S, FONT_H, FONT_XXL, FONT_BOLD, TA_CENTER)
    
    Story.append(text_c101)
    Story.append(text_c102)
    Story.append(text_c103)
    Story.append(FrameBreak)

    # Text Column
    column_12 = ColorFrame(doc.leftMargin, doc.bottomMargin, doc.width/3-12, 0.72*doc.height, showBoundary=0, roundedBackground=CUSTOM_LGRAY, topPadding=10)
    pc12 = ParagraphStyle('column_1', alignment = TA_LEFT, fontSize = FONT_ML, fontName = FONT_BOLD, textColor = CUSTOM_DTEAL, leading = 14, spaceBefore = 16)
    pc13 = ParagraphStyle('column_1', alignment = TA_LEFT, fontSize = FONT_H, fontName = FONT_BOLD, textColor = CUSTOM_DGRAY, leading = 12, spaceBefore = 4)
    pc14 = ParagraphStyle('column_1', alignment = TA_LEFT, fontSize = FONT_T, fontName = FONT_NORMAL, textColor = CUSTOM_DGRAY, leading = 12)
    
    Story.append(Paragraph("This energy profile details the estimated annual energy costs and expected annual energy usage of this building. It also highlights energy upgrades and improvements made to increase the building’s efficiency. The profile includes further recommendations that can help to achieve more efficiency and energy costs savings.", tf_standard))
    Story.append(Spacer(1,16))
    Story.append(HRFlowable(width="90%", thickness=1, lineCap='round', color=colors.white, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))
    Story.append(Paragraph("BUILDING INFORMATION", pc12))
    Story.append(Paragraph("LOCATION:", pc13))
    Story.append(Paragraph(data_dict['street'],pc14))
    Story.append(Paragraph(data_dict['city'] + ", " + data_dict["state"] + " " + data_dict["zipcode"], pc14))
    Story.append(Paragraph("YEAR BUILT:", pc13))
    Story.append(Paragraph(str(int(data_dict['year_built'])),pc14))
    Story.append(Paragraph("GROSS FLOOR AREA:",pc13))
    Story.append(Paragraph(str(int(data_dict['propGrossFloorArea']))+' Sq.Ft.',pc14))
    Story.append(Spacer(1,16))
    Story.append(HRFlowable(width="90%", thickness=1, lineCap='round', color=colors.white, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))
    Story.append(Paragraph("REPORT INFORMATION", pc12))
    Story.append(Paragraph("PROFILE CREATION DATE:", pc13))
    Story.append(Paragraph(datetime.datetime.now().strftime("%m/%d/%Y"),pc14))
    Story.append(Paragraph("REPORTING YEAR:", pc13))
    Story.append(Paragraph(str(data_dict['year_ending']),pc14))
    Story.append(Spacer(1,16))
    Story.append(HRFlowable(width="90%", thickness=1, lineCap='round', color=colors.white, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))
    Story.append(Paragraph("Brought to you by the Building Energy Analysis Manager", tf_small))
    Story.append(Image(IMG_PATH+"/beamlogo.png", 1.5*inch, 0.5475*inch))
    Story.append(FrameBreak)
    
    # Column 2
    y_offset = 0.04
    # Expected Usage Total
    column_211 = ColorFrame(doc.leftMargin+doc.width/3, doc.height*(1-y_offset), (1/4)*(2/3)*doc.width, 0.04*doc.height, showBoundary=0, roundedBackground=CUSTOM_DTEAL, topPadding=5, bottomPadding = 5)    
    pc201 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = FONT_LL, fontName = FONT_BOLD, textColor = colors.white)
    text_c201 = Paragraph(str(int(data_dict['site_total']))+"<font size=10> MMBtu </font>", pc201)
    Story.append(text_c201)
    Story.append(FrameBreak)
    
    column_212 = Frame(doc.leftMargin+doc.width/3+(1/4)*(2/3)*doc.width, doc.height*(1-y_offset), (3/4)*(2/3)*doc.width, 0.04*doc.height, showBoundary=0, topPadding=10)    
    pc202 = ParagraphStyle('column_2', alignment = TA_LEFT, fontSize = FONT_L, fontName = FONT_BOLD, textColor = CUSTOM_DTEAL)
    text_c202 = Paragraph('Annual Energy Usage', pc202)
    Story.append(text_c202)
    Story.append(FrameBreak)

    y_offset += 0.28
    column_22 = Frame(doc.leftMargin+doc.width/3, doc.height*(1-y_offset), (2/3)*doc.width, (y_offset-0.04)*doc.height, showBoundary=0, topPadding=10)    
    Story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color= CUSTOM_MGRAY, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='TOP', dash=None))
    text_c220 = Paragraph("The building energy use with 0 being a net zero building", tf_standard)
    Story.append(text_c220)
    
    # Wedge - start at 0.62 end at 4.82
    espm_score_mapping = Scores.map_scores(data_dict['systemDefinedPropertyType'])
    if data_dict['energy_star_score']:
        site_max = float(espm_score_mapping['1']) * data_dict['site_total'] / float(espm_score_mapping[str(int(data_dict['energy_star_score']))])
    else:
        site_max = float(espm_score_mapping['1']) * data_dict['site_total'] / float(espm_score_mapping['50'])
            
    median_site_use = data_dict['propGrossFloorArea'] * data_dict['medianSiteIntensity'] / 1000.0
    wedge_img = IMG_PATH+"/wedge.png"
    wedge = Image(wedge_img, 5.0*inch, 2.25*inch)
    Story.append(wedge)
    triangle = IMG_PATH+"/triangle.png"
    offset_x = 0.53+data_dict['site_total']/site_max*(4.75-0.53)
    pic = flowable_triangle(triangle,offset_x, 1.78, 0.2, 0.288,'')
    Story.append(pic)
    txt = flowable_text(min(offset_x-0.5,2), 2.2, "This building's usage: " + str(int(data_dict['site_total'])),9)
    Story.append(txt)
    triangle2 = IMG_PATH+"/triangle2.png"
    offset_x = 0.62 + 40.0/site_max*(4.82-0.62)
    pic = flowable_triangle(triangle2,offset_x, 0.44,0.08, 0.138,"Net zero \n building","left")
    Story.append(pic)
    triangle = IMG_PATH+"/triangle2.png"
    offset_x = 0.62 + median_site_use/site_max*(4.82-0.62)
    if offset_x < 4.3:
        pic = flowable_triangle(triangle2,offset_x, 0.44,0.08, 0.138,"Median building","right")
        Story.append(pic)
    triangle2 = IMG_PATH+"/triangle2.png"
    offset_x = 0.62 + 105.0/site_max*(4.82-0.62)
    txt = flowable_text(4.82, 0.44, str(int(site_max)),7)
    Story.append(txt)
    Story.append(FrameBreak)
    
    # Cost
    y_offset += 0.02
    column_231 = ColorFrame(doc.leftMargin+doc.width/3, doc.height*(1-y_offset), (1/4)*(2/3)*doc.width, 0.04*doc.height, showBoundary=0, roundedBackground=CUSTOM_DTEAL, topPadding=5, bottomPadding=5)    
    pc231 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = FONT_LL, fontName = FONT_BOLD, textColor = colors.white)
    text_c231 = Paragraph('${:,.0f}'.format(data_dict['energyCost']), pc231)
    Story.append(text_c231)
    Story.append(FrameBreak)
    column_232 = Frame(doc.leftMargin+doc.width/3+(1/4)*(2/3)*doc.width, doc.height*(1-y_offset), (3/4)*(2/3)*doc.width, 0.04*doc.height, showBoundary=0, topPadding=10)    
    text_c232 = Paragraph('Annual Energy Cost', pc202)
    Story.append(text_c232)
    Story.append(FrameBreak)
    
    # Pie Chart
    y_offset +=0.09
    column_24 = Frame(doc.leftMargin+doc.width/3, doc.height*(1-y_offset), (2/3)*doc.width, 0.09*doc.height, showBoundary=0, topPadding=10)    
    Story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color= CUSTOM_MGRAY, spaceBefore=0, spaceAfter=0, hAlign='CENTER', vAlign='TOP', dash=None))
    text_c240 = Paragraph("Estimate includes electricity and fuels from ENERGY STAR Portfolio Manager", tf_standard)

    Story.append(text_c240)
    Story.append(FrameBreak)
    y_offset +=0.16
    column_251 = Frame(doc.leftMargin+doc.width/3, doc.height*(1-y_offset), (1/5)*(2/3)*doc.width, 0.20*doc.height, showBoundary=0, topPadding=0)    
    Story.append(FrameBreak)
    column_252 = Frame(doc.leftMargin+doc.width/3+(1/5)*(2/3)*doc.width, doc.height*(1-y_offset), (1/2)*(2/3)*doc.width, 0.20*doc.height, showBoundary=0, topPadding=0)    
    
    # Cost Table
    cost_subTable = Tables.cost_table(data_dict)
     
    Story.append(cost_subTable)
    Story.append(FrameBreak)
    pie = Charts.pie_chart(data_dict, FUELS, FUELICONS, FUELCOLOR)
    column_253 = Frame(doc.leftMargin+doc.width/3+(7/15)*doc.width, doc.height*(1-y_offset), (3/10)*(2/3)*doc.width, 0.20*doc.height, showBoundary=0, topPadding=10)        
    Story.append(pie)
    Story.append(FrameBreak)    
    
    # Energy Highlights Header
    y_offset += 0.03
    column_261 = ColorFrame(doc.leftMargin+doc.width/3, doc.height*(1-y_offset)+10, (1/4)*(2/3)*doc.width, 0.04*doc.height, showBoundary=0, roundedBackground=CUSTOM_DTEAL, topPadding=10)    
    pc261 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = FONT_T, fontName = FONT_BOLD, textColor = colors.white)
    text_c261 = Paragraph('Insights & Trends', pc261)
    Story.append(text_c261)
    Story.append(FrameBreak)

    # Energy Highlights Details
    y_offset += 0.17
    column_27 = Frame(doc.leftMargin+doc.width/3, doc.height*(1-y_offset), (2/3)*doc.width, 0.17*doc.height, showBoundary=0, topPadding=0)    
    Story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color= CUSTOM_MGRAY, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='TOP', dash=None))
    
    ## HIGHLIGHTS: CERTIFICATIONS, SOLAR & EV, GENERAL
    num_line = 0
    t_cert, num_line = Highlights.cert_commercial(data_dict, FONT_T, FONT_NORMAL, CUSTOM_DGRAY, CHECK_IMG, num_line)             
    if t_cert:
        ratings_table = Table(t_cert, colWidths = [2.7*inch, 2.7*inch])
        ratings_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('BACKGROUND',(0,0),(-1,-1),colors.white),
         ]))
        Story.append(ratings_table)   
            
    t_achieve, num_line = Highlights.general_commercial(data_dict, FONT_T, FONT_NORMAL, CUSTOM_DGRAY, CHECK_IMG, num_line)
    if t_achieve:
        ratings_table = Table(t_achieve, colWidths = [5.4*inch])
        ratings_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('BACKGROUND',(0,0),(-1,-1),colors.white),
         ]))
        Story.append(ratings_table)

    t_achieve, num_line = Highlights.solar_commercial(data_dict, FONT_T, FONT_NORMAL, CUSTOM_DGRAY, CHECK_IMG, num_line)
    if t_achieve:
        achieve_table = Table(t_achieve, colWidths = [5.1*inch])
        achieve_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BACKGROUND',(0,0),(-1,-1),colors.white),
         ]))
        Story.append(achieve_table)
     
    Story.append(FrameBreak)

    # Take Action Header
    y_offset += 0.0
    column_281 = ColorFrame(doc.leftMargin+doc.width/3, doc.bottomMargin+0.17*doc.height+10, (1/4)*(2/3)*doc.width, 0.04*doc.height, showBoundary=0, roundedBackground=CUSTOM_DTEAL, bottomPadding=10)    
    text_c281 = Paragraph('Take Action!', pc261)
    Story.append(text_c281)
    Story.append(FrameBreak)
    
    pc262 = ParagraphStyle('column_2', alignment = TA_LEFT, fontSize = FONT_T, fontName = FONT_BOLD, textColor = CUSTOM_DTEAL, spaceBefore = -12, spaceAfter = -12)
    
    column_282 = Frame(doc.leftMargin+doc.width/3+(1/4)*(2/3)*doc.width, doc.bottomMargin+0.17*doc.height, (3/4)*(2/3)*doc.width, 0.06*doc.height, showBoundary=0, topPadding=10)    
    text_c282 = Paragraph('The following actions can help you save money on your energy costs for years to come', pc262)
    Story.append(text_c282)
    Story.append(FrameBreak)
    
    # Take Action Details    
    column_29 = Frame(doc.leftMargin+doc.width/3, doc.bottomMargin, (2/3)*doc.width, 0.17*doc.height, showBoundary=0, topPadding=0)    
    Story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color= CUSTOM_MGRAY, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='TOP', dash=None))        
    pc291 = ParagraphStyle('body_left', alignment = TA_LEFT, textColor = CUSTOM_DGRAY, fontSize = FONT_T, fontName = FONT_NORMAL,  spaceBefore = 6, spaceAfter = 0, leading=10, backColor = 'white', bulletIndent = 12, firstLineIndent = 0, leftIndent = 12, rightIndent = 0)

    Story.append(Paragraph("Schedule a professional energy audit to identify cost-saving upgrades.", pc291, bulletText=UNCHECKED.encode('UTF8')))
    Story.append(Paragraph("Perform regular building envelope maintenance.", pc291, bulletText=UNCHECKED.encode('UTF8')))
    Story.append(Paragraph("Regularly update and maintain key heating and cooling systems.", pc291, bulletText=UNCHECKED.encode('UTF8')))
    Story.append(Paragraph('Look into energy efficiency incentives and rebates available to commercial properties through <font name="InterstateLight" color=blue><link href="https://www.efficiencymaine.com/">Efficiency Maine</link></font>.', pc291, bulletText=UNCHECKED.encode('UTF8')))
    Story.append(Paragraph('Identify other state and federal incentives through the <font name="InterstateLight" color=blue><link href="https://www.dsireusa.org/">Database of State Incentives for Renewables & Efficiency (DSIRE)</link></font>.', pc291, bulletText=UNCHECKED.encode('UTF8')))    
                        
### BUILD PAGE
    page_1_frames = [column_10, column_11, column_12, column_211, column_212, column_22, column_231, column_232, column_24, column_251, column_252, column_253, column_261, column_27, column_281, column_282, column_29]
    templates =[]
    templates.append(PageTemplate(frames=page_1_frames,id='firstPage'))
    doc.addPageTemplates(templates)
    style = styles["Normal"]

    #populate story with paragraphs    
    doc.build(Story)

# Run with:  python3 -m label.populate_beam_south_portland
if __name__ == '__main__':
    data_dict = {
        'street': '77 MASSACHUSETTS AVE', 'city': 'CAMBRIGE', 'state': 'MA', 'zipcode': '02139', 
        'year_built': 1895, 'year_ending': 2022, 'propGrossFloorArea': 100000.0, 'systemDefinedPropertyType': 'Enclosed Mall', 'energy_star_score': None, 'site_total': 3434,  'medianSiteIntensity': 50, 'percentBetterThanSiteIntensityMedian': 0.25, 'cons_mmbtu_min': 0,
        'siteEnergyUseElectricityGridPurchase': 1000.0, 'siteEnergyUseElectricityGridPurchaseKwh': 100000.0, 'siteEnergyUseNaturalGas': 1000.0, 'siteEnergyUseKerosene': 0.0, 'siteEnergyUsePropane': 1000.0,
        'siteEnergyUseDiesel': 0.0, 'siteEnergyUseFuelOil1': 0.0, 'siteEnergyUseFuelOil2': 0.0, 'siteEnergyUseFuelOil4': 0.0, 'siteEnergyUseFuelOil5And6': 0.0, 'siteEnergyUseWood': 0.0,
        'energyCost': 10000.0, 
        'energyCostElectricityOnsiteSolarWind': 2110.0,
        'energyCostElectricityGridPurchase': 1000.0, 'energyCostNaturalGas': 1000.0, 'energyCostKerosene': 0.0, 'energyCostPropane': 1000.0,
        'energyCostDiesel': 0.0, 'energyCostFuelOil1': 0.0, 'energyCostFuelOil2': 0.0, 'energyCostFuelOil4': 0.0, 'energyCostFuelOil5And6': 0.0, 'energyCostWood': 0.0,
        'cons_solar': -11000.0,
        'estar_wh': True,
        'yoy_percent_change_site_eui_2022': None, 'yoy_percent_change_elec_2022': -0.1,
        'totalLocationBasedGHGEmissions': 150,
        'onSiteRenewableSystemGeneration': 20000, 'numberOfLevelOneEvChargingStations': 3, 'numberOfLevelTwoEvChargingStations': 0, 'numberOfDcFastEvChargingStations': 0,
    }
    out_file = 'South_Portland_BEAM_Profile.pdf'
    write_south_portland_profile_pdf(data_dict, out_file)


