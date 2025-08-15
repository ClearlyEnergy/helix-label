# -*- coding: utf-8 -*-
#! /usr/bin/python
# run with python3 -m label.populate_beam_west_virginia

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
from label.utils.utils import ColorFrame, ColorFrameSimpleDocTemplate, Charts, Tables, Scores, Highlights, flowable_text, flowable_triangle, validate_data_dict
import datetime

#Adding Arial Unicode for checkboxes
module_path = os.path.abspath(os.path.dirname(__file__))
FONT_PATH = os.path.normpath(os.path.join(module_path, ".fonts"))
IMG_PATH = os.path.normpath(os.path.join(module_path, "images"))
CUSTOM_DTEAL = colors.Color(red=(108.0/255),green=(179.0/255),blue=(67.0/255))

pdfmetrics.registerFont(TTFont('InterstateLight',FONT_PATH+'/InterstateLight.ttf'))
pdfmetrics.registerFont(TTFont('InterstateBlack',FONT_PATH+'/InterstateBlack.ttf'))
#pdfmetrics.registerFont(TTFont('Arial Unicode',FONT_PATH+'/Arial Unicode.ttf'))
pdfmetrics.registerFont(TTFont("FontAwesome", FONT_PATH+"/FontAwesome.ttf"))

def write_west_virginia_profile_pdf(data_dict, output_pdf_path):
    is_data_valid, msg, data_dict = validate_data_dict(data_dict)
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
    column_10 = Frame(doc.leftMargin, doc.height-0.1*doc.height, doc.width/3-12, 0.13*doc.height, showBoundary=0)    
    vthep_logo = IMG_PATH+"/eewv.png"
    im = Image(vthep_logo, 2.5*inch, 0.88*inch) #max is 1.1 inch height, #max is 2.5in wide
    Story.append(im)
    Story.append(FrameBreak)
    
    # Cost Box
    # OPTIONS ARE ESTAR_SCORE, EUI, WNEUI, GHG, EU
    column_11 = ColorFrame(doc.leftMargin, doc.height-0.23*doc.height, doc.width/3-12, 0.13*doc.height, showBoundary=0, roundedBackground=CUSTOM_DTEAL, topPadding=10)    
    text_c101, text_c102, text_c103 = Highlights.score_box(data_dict)
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
    Story.append(Paragraph("PROPERTY TYPE:", pc13))
    Story.append(Paragraph(data_dict['systemDefinedPropertyType'],pc14))
    Story.append(Paragraph("GROSS FLOOR AREA:",pc13))
    floor_area = str("{:,}".format(int(data_dict['propGrossFloorArea']))) if data_dict['propGrossFloorArea'] is not None else 'N/A'
    Story.append(Paragraph(floor_area +' Sq.Ft.',pc14))
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
    text_c201 = Highlights.usage_box(data_dict)
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
    
    # Wedge
    wedge, txt, txt2, pic, pic2, pic3 = Charts.wedge(data_dict)
    Story.append(wedge)
    Story.append(pic)
    Story.append(txt)
    Story.append(pic2)
    if pic3:
        Story.append(pic3)
    Story.append(txt2)
    Story.append(FrameBreak)
    
    # Cost
    # Options are COST, GHG, COST_INCLSQFT, ELECTRIFY
    y_offset += 0.02
    text_c231, text_c232 = Highlights.cost_box(data_dict, CUSTOM_DTEAL)
    column_231 = ColorFrame(doc.leftMargin+doc.width/3, doc.height*(1-y_offset), (1/4)*(2/3)*doc.width, 0.04*doc.height, showBoundary=0, roundedBackground=CUSTOM_DTEAL, topPadding=5, bottomPadding=5)    
    column_232 = Frame(doc.leftMargin+doc.width/3+(1/4)*(2/3)*doc.width, doc.height*(1-y_offset), (3/4)*(2/3)*doc.width, 0.04*doc.height, showBoundary=0, topPadding=10)    
    Story.append(text_c231)
    Story.append(FrameBreak)
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
    t_solar, num_line = Highlights.solar_commercial(data_dict, FONT_T, FONT_NORMAL, CUSTOM_DGRAY, CHECK_IMG, num_line)
    if t_solar:
        solar_table = Table(t_solar, colWidths = [5.1*inch])
        solar_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BACKGROUND',(0,0),(-1,-1),colors.white),
         ]))
        Story.append(solar_table)
    
    t_achieve, num_line = Highlights.general_commercial(data_dict, FONT_T, FONT_NORMAL, CUSTOM_DGRAY, CHECK_IMG, num_line, ['elec','median','eui','yoy_percent_change_elec', 'yoy_percent_change_ng', ])
    if t_achieve:
        achieve_table = Table(t_achieve, colWidths = [5.4*inch])
        achieve_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
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

    Story.append(Paragraph('Not sure where to begin? Contact Robin Blakeman (<font name="InterstateLight" color=blue><link href="mailto:robin@eewv.org">robin@eewv.org</link></font>) from <font name="InterstateLight" color=blue><link href="https://www.eewv.net/">Energy Efficient West Virginia (EEWV)</link></font> for guidance.', pc291, bulletText=UNCHECKED.encode('UTF8')))
    Story.append(Paragraph('Refer to the WV Office of Energy’s funding opportunities for <font name="InterstateLight" color=blue><link href="https://energywv.org/funding-opportunities/eecbg/">energy efficiency upgrades</link></font>, <font name="InterstateLight" color=blue><link href="https://energywv.org/funding-opportunities/solar-for-all/">solar</link></font>, <font name="InterstateLight" color=blue><link href="https://energywv.org/">and more</link></font>.', pc291, bulletText=UNCHECKED.encode('UTF8')))
    Story.append(Paragraph('Read about <font name="InterstateLight" color=blue><link href="https://neep.org/energy-rating/benchmarking-toolkit">building benchmarking</link></font> and it\'s benefits.', pc291, bulletText=UNCHECKED.encode('UTF8')))
    Story.append(Paragraph('Look into <font name="InterstateLight" color=blue><link href="https://www.energystar.gov/about/federal-tax-credits">federal tax credits</link></font> and rebates for energy-saving improvements.', pc291, bulletText=UNCHECKED.encode('UTF8')))
    Story.append(Paragraph('Check <font name="InterstateLight" color=blue><link href="https://programs.dsireusa.org/system/program/wv">WV incentives on DSIRE</link></font> for energy efficiency upgrades.', pc291, bulletText=UNCHECKED.encode('UTF8')))
                       
### BUILD PAGE
    page_1_frames = [column_10, column_11, column_12, column_211, column_212, column_22, column_231, column_232, column_24, column_251, column_252, column_253, column_261, column_27, column_281, column_282, column_29]
    templates =[]
    templates.append(PageTemplate(frames=page_1_frames,id='firstPage'))
    doc.addPageTemplates(templates)
    style = styles["Normal"]

    #populate story with paragraphs    
    doc.build(Story)

# Run with:  python3 -m label.populate_west_virginia_profile
if __name__ == '__main__':
    has_cost = True
    if has_cost:
                data_dict = {
            'street': '150 Lively Street', 'city': 'Fayetteville', 'state': 'WV', 'zipcode': '25840', 
            'year_built': 1988, 'year_ending': 2024, 'propGrossFloorArea': 2100.0, 'systemDefinedPropertyType': 'Vehicle Repair Services', 'energy_star_score': None, 'site_total': 245.586,  'medianSiteIntensity': 64.8, 
            'percentBetterThanSiteIntensityMedian': None, 'cons_mmbtu_min': 0,
            'siteEnergyUseElectricityGridPurchase': 188130.0, 'siteEnergyUseElectricityGridPurchaseKwh': 55138.0, 'siteEnergyUseNaturalGas': 57456.0, 'siteEnergyUseKerosene': None, 'siteEnergyUsePropane': None,
            'siteEnergyUseDiesel': 0.0, 'siteEnergyUseFuelOil1': 0.0, 'siteEnergyUseFuelOil2': 0.0, 'siteEnergyUseFuelOil4': 0.0, 'siteEnergyUseFuelOil5And6': 0.0, 'siteEnergyUseWood': 0.0, 'siteEnergyUseDistrictSteam': 0.0,
            'siteIntensity': 116.9, 
            'energyCost': 3348.91,  'percent_electric': 20.0,
            'energyCostElectricityOnsiteSolarWind': None,
            'energyCostElectricityGridPurchase': 2259.61, 'energyCostNaturalGas': 1089.30, 'energyCostKerosene': None, 'energyCostPropane': None,
            'energyCostDiesel': 0.0, 'energyCostFuelOil1': 0.0, 'energyCostFuelOil2': 0.0, 'energyCostFuelOil4': 0.0, 'energyCostFuelOil5And6': 0.0, 'energyCostWood': 0.0, 'energyCostDistrictSteam': 0.0,
            'cons_solar': 0.0,
            'estar_wh': False,
            'yoy_percent_change_site_eui': None, 'yoy_percent_change_elec': None,
            'totalLocationBasedGHGEmissions': None,
            'onSiteRenewableSystemGeneration': 0.0, 'numberOfLevelOneEvChargingStations': 0, 'numberOfLevelTwoEvChargingStations': 0, 'numberOfDcFastEvChargingStations': 0,
        }

#        data_dict = {
#            'street': '1 MAIN ST', 'city': 'NITRO', 'state': 'WV', 'zipcode': '25143', 
#            'year_built': 1935, 'year_ending': 2024, 'propGrossFloorArea': 50000.0, 'systemDefinedPropertyType': 'Office', 'energy_star_score': 99, 'site_total': 3434,  'medianSiteIntensity': 2500, 'percentBetterThanSiteIntensityMedian': 5.4, 'cons_mmbtu_min': 0,
#            'siteEnergyUseElectricityGridPurchase': 1000.0, 'siteEnergyUseElectricityGridPurchaseKwh': 100000.0, 'siteEnergyUseNaturalGas': 1000.0, 'siteEnergyUseKerosene': 0.0, 'siteEnergyUsePropane': 1000.0,
#            'siteEnergyUseDiesel': 0.0, 'siteEnergyUseFuelOil1': 0.0, 'siteEnergyUseFuelOil2': 0.0, 'siteEnergyUseFuelOil4': 0.0, 'siteEnergyUseFuelOil5And6': 0.0, 'siteEnergyUseWood': 0.0, 'siteEnergyUseDistrictSteam': 0.0,
#            'siteIntensity': 100.0,
#            'energyCost': 10000.0, 'percent_electric': 20.0,
#            'energyCostElectricityOnsiteSolarWind': 0.0,
#            'energyCostElectricityGridPurchase': 1000.0, 'energyCostNaturalGas': 1000.0, 'energyCostKerosene': 0.0, 'energyCostPropane': 1000.0,
#            'energyCostDiesel': 0.0, 'energyCostFuelOil1': 0.0, 'energyCostFuelOil2': 0.0, 'energyCostFuelOil4': 0.0, 'energyCostFuelOil5And6': 0.0, 'energyCostWood': 0.0, 'energyCostDistrictSteam': 0.0,
#            'cons_solar': 0.0,
#            'estar_wh': True,
#            'yoy_percent_change_site_eui': 0.0, 'yoy_percent_change_elec': -0.1,
#            'totalLocationBasedGHGEmissions': 150,
#            'onSiteRenewableSystemGeneration': 0.0, 'numberOfLevelOneEvChargingStations': 0, 'numberOfLevelTwoEvChargingStations': 0, 'numberOfDcFastEvChargingStations': 0,
#        }
#no costs data example
    else:
        data_dict = {
            'street': '1 MAIN ST', 'city': 'NITRO', 'state': 'WV', 'zipcode': '25143', 
            'year_built': 1935, 'year_ending': 2024, 'propGrossFloorArea': 50000.0, 'systemDefinedPropertyType': 'Office', 'energy_star_score': 99, 'site_total': 3434,  'medianSiteIntensity': 2500, 'percentBetterThanSiteIntensityMedian': 5.4, 'cons_mmbtu_min': 0,
            'siteEnergyUseElectricityGridPurchase': 10000.0, 'siteEnergyUseElectricityGridPurchaseKwh': 10000.0, 'siteEnergyUseNaturalGas': 5000.0, 'siteEnergyUseKerosene': None, 'siteEnergyUsePropane': None,
            'siteEnergyUseDiesel': 0.0, 'siteEnergyUseFuelOil1': 0.0, 'siteEnergyUseFuelOil2': 0.0, 'siteEnergyUseFuelOil4': 0.0, 'siteEnergyUseFuelOil5And6': 0.0, 'siteEnergyUseWood': 0.0, 'siteEnergyUseDistrictSteam': 0.0,
            'siteIntensity': 100.0, 
            'energyCost': None,  'percent_electric': 20.0,
            'energyCostElectricityOnsiteSolarWind': None,
            'energyCostElectricityGridPurchase': None, 'energyCostNaturalGas': None, 'energyCostKerosene': None, 'energyCostPropane': None,
            'energyCostDiesel': 0.0, 'energyCostFuelOil1': 0.0, 'energyCostFuelOil2': 0.0, 'energyCostFuelOil4': 0.0, 'energyCostFuelOil5And6': 0.0, 'energyCostWood': 0.0, 'energyCostDistrictSteam': 0.0,
            'cons_solar': 0.0,
            'estar_wh': True,
            'yoy_percent_change_site_eui': 0.0, 'yoy_percent_change_elec': -0.1,
            'totalLocationBasedGHGEmissions': 150,
            'onSiteRenewableSystemGeneration': 0.0, 'numberOfLevelOneEvChargingStations': 0, 'numberOfLevelTwoEvChargingStations': 0, 'numberOfDcFastEvChargingStations': 0,
        }


    out_file = 'West_Virginia_Profile.pdf'
    write_west_virginia_profile_pdf(data_dict, out_file)