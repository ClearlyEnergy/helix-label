# -*- coding: utf-8 -*-
#! /usr/bin/python
# run with python3 -m label.populate_beam_core

import datetime
import os
import re
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


#Adding Arial Unicode for checkboxes
module_path = os.path.abspath(os.path.dirname(__file__))
FONT_PATH = os.path.normpath(os.path.join(module_path, ".fonts"))
IMG_PATH = os.path.normpath(os.path.join(module_path, "images"))
CUSTOM_DTEAL = colors.Color(red=(227.0/255),green=(241.0/255),blue=(252.0/255)) ## This is the color to customize

pdfmetrics.registerFont(TTFont('InterstateLight',FONT_PATH+'/InterstateLight.ttf'))
pdfmetrics.registerFont(TTFont('InterstateBlack',FONT_PATH+'/InterstateBlack.ttf'))
#pdfmetrics.registerFont(TTFont('Arial Unicode',FONT_PATH+'/Arial Unicode.ttf'))
pdfmetrics.registerFont(TTFont("FontAwesome", FONT_PATH+"/FontAwesome.ttf"))
    
def write_core_profile_pdf(data_dict, output_pdf_path):
#    is_data_valid, msg, data_dict = validate_data_dict(data_dict)
    doc = ColorFrameSimpleDocTemplate(output_pdf_path,pagesize=letter,rightMargin=20,leftMargin=20,topMargin=20,bottomMargin=20)
    styles = getSampleStyleSheet()                 

    Story=[]
    #Standard text formats
    tf_standard = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = FONT_H, fontName = FONT_NORMAL, textColor = CUSTOM_DGRAY, leading = 14)  
    tf_standard_bold = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = FONT_H, fontName = FONT_BOLD, textColor = CUSTOM_DGRAY, leading = 14)  
    tf_standard_spaced = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = FONT_H, fontName = FONT_NORMAL, textColor = CUSTOM_DGRAY, leading = 16, spaceAfter = 12)  
    tf_small = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = FONT_S, fontName = FONT_NORMAL, textColor = CUSTOM_DGRAY, spaceBefore = 12, spaceAfter = 12)  
    tf_small_squished = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = FONT_S, fontName = FONT_NORMAL, textColor = CUSTOM_DGRAY, spaceBefore = 6, spaceAfter = 0)  
    tf_small_right = ParagraphStyle('standard', alignment = TA_RIGHT, fontSize = FONT_S, fontName = FONT_NORMAL, textColor = CUSTOM_DGRAY, spaceBefore = 6, spaceAfter = 0)  
    tf_small_bold = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = FONT_S, fontName = FONT_BOLD, textColor = CUSTOM_DGRAY, spaceBefore = 6, spaceAfter = 0)  
    
    ### P1
    # Logo
    column_10 = ColorFrame(doc.leftMargin, doc.height-0.125*doc.height, doc.width/3-12, 0.13*doc.height, showBoundary=0, roundedBackground=CUSTOM_DTEAL) 
#    column_10 = Frame(doc.leftMargin, doc.height-0.125*doc.height, doc.width/3-12, 0.13*doc.height, showBoundary=0)    
    vthep_logo = IMG_PATH+"/core_logo.png"
    im = Image(vthep_logo, 2.0*inch, 0.56*inch)
    Story.append(im)
    Story.append(FrameBreak)
    
    # Cost Box
    column_11 = ColorFrame(doc.leftMargin, doc.height-0.23*doc.height, doc.width/3-12, 0.13*doc.height, showBoundary=0, roundedBackground=CUSTOM_DTEAL, topPadding=10)
    text_c101, text_c102, text_c103 = Highlights.score_box(data_dict, 'ESTAR_SCORE')
    
    Story.append(text_c101)
    Story.append(text_c102)
    Story.append(text_c103)
    Story.append(FrameBreak)

    # Text Column
    column_12 = ColorFrame(doc.leftMargin, doc.bottomMargin, doc.width/3-12, 0.72*doc.height, showBoundary=0, roundedBackground=CUSTOM_LGRAY, topPadding=10)
    pc12 = ParagraphStyle('column_1', alignment = TA_LEFT, fontSize = FONT_ML, fontName = FONT_BOLD, textColor = CUSTOM_DTEAL, leading = 14, spaceBefore = 16)
    pc13 = ParagraphStyle('column_1', alignment = TA_LEFT, fontSize = FONT_H, fontName = FONT_BOLD, textColor = CUSTOM_DGRAY, leading = 12, spaceBefore = 4)
    pc14 = ParagraphStyle('column_1', alignment = TA_LEFT, fontSize = FONT_T, fontName = FONT_NORMAL, textColor = CUSTOM_DGRAY, leading = 12)
    
    Story.append(Paragraph('Thank you for working with the Community Office for Resource Efficiency (CORE) to comply with the City of Aspen’s <font name="InterstateLight" color=blue><link href="https://aspen.gov/1245/Building-IQ">Building IQ Ordinance</link></font>. This scorecard outlines your building’s energy usage in comparison to other buildings like yours in Aspen, insights and trends specific to your property, along with suggested actions to enhance energy efficiency and reduce energy costs.', tf_standard))
    Story.append(Spacer(1,16))
    Story.append(HRFlowable(width="90%", thickness=1, lineCap='round', color=colors.white, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))
    Story.append(Paragraph("BUILDING INFORMATION", pc12))
    Story.append(Paragraph("LOCATION:", pc13))
    Story.append(Paragraph(data_dict['street'],pc14))
    Story.append(Paragraph(data_dict['city'] + ", " + data_dict["state"] + " " + data_dict["zipcode"], pc14))
    Story.append(Paragraph("YEAR BUILT:", pc13))
    Story.append(Paragraph(str(int(data_dict['year_built'])),pc14))
    Story.append(Paragraph("GROSS FLOOR AREA:",pc13))
    floor_area = str(int(data_dict['propGrossFloorArea'])) if data_dict['propGrossFloorArea'] is not None else 'N/A'
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
    text_c202 = Paragraph('Annual Energy Use Intensity', pc202)
    Story.append(text_c202)
    Story.append(FrameBreak)

    y_offset += 0.28
    column_22 = Frame(doc.leftMargin+doc.width/3, doc.height*(1-y_offset), (2/3)*doc.width, (y_offset-0.04)*doc.height, showBoundary=0, topPadding=10)    
    Story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color= CUSTOM_MGRAY, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='TOP', dash=None))
    text_c220 = Paragraph("The energy use intensity (EUI) refers to the amount of energy used per square foot annually", tf_standard)
    Story.append(text_c220)
    
    # Wedge
    wedge, txt, txt2, pic, pic2, pic3 = Charts.wedge(data_dict, True)
    Story.append(wedge)
    Story.append(pic)
    Story.append(txt)
    Story.append(pic2)
    if pic3:
        Story.append(pic3)
    Story.append(txt2)
    Story.append(FrameBreak)
    
    # Cost
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
    t_cert, num_line = Highlights.cert_commercial(data_dict, FONT_T, FONT_NORMAL, CUSTOM_DGRAY, CHECK_IMG, num_line)             
    if t_cert:
        ratings_table = Table(t_cert, colWidths = [2.7*inch, 2.7*inch])
        ratings_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('BACKGROUND',(0,0),(-1,-1),colors.white),
         ]))
        Story.append(ratings_table)   
        
    t_solar, num_line = Highlights.solar_commercial(data_dict, FONT_T, FONT_NORMAL, CUSTOM_DGRAY, CHECK_IMG, num_line)
    if t_solar:
        solar_table = Table(t_solar, colWidths = [5.1*inch])
        solar_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BACKGROUND',(0,0),(-1,-1),colors.white),
         ]))
        Story.append(solar_table)
    
    t_achieve, num_line = Highlights.general_commercial(data_dict, FONT_T, FONT_NORMAL, CUSTOM_DGRAY, CHECK_IMG, num_line)
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
    column_281 = ColorFrame(doc.leftMargin+doc.width/3, doc.bottomMargin+0.17*doc.height+10, (1/3)*(2/3)*doc.width, 0.04*doc.height, showBoundary=0, roundedBackground=CUSTOM_DTEAL, bottomPadding=10)    
    text_c281 = Paragraph('Take Action with CORE!', pc261)
    Story.append(text_c281)
    Story.append(FrameBreak)
    
    pc262 = ParagraphStyle('column_2', alignment = TA_LEFT, fontSize = FONT_T, fontName = FONT_BOLD, textColor = CUSTOM_DTEAL, spaceBefore = -12, spaceAfter = -12)
    
    column_282 = Frame(doc.leftMargin+doc.width/3+(1/3)*(2/3)*doc.width, doc.bottomMargin+0.17*doc.height, (2/3)*(2/3)*doc.width, 0.06*doc.height, showBoundary=0, topPadding=10)    
    text_c282 = Paragraph('The following actions can help you save money on your energy costs for years to come', pc262)
    Story.append(text_c282)
    Story.append(FrameBreak)
    
    # Take Action Details    
    column_29 = Frame(doc.leftMargin+doc.width/3, doc.bottomMargin, (2/3)*doc.width, 0.17*doc.height, showBoundary=0, topPadding=0)    
    Story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color= CUSTOM_MGRAY, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='TOP', dash=None))        
    pc291 = ParagraphStyle('body_left', alignment = TA_LEFT, textColor = CUSTOM_DGRAY, fontSize = FONT_T, fontName = FONT_NORMAL,  spaceBefore = 6, spaceAfter = 0, leading=10, backColor = 'white', bulletIndent = 12, firstLineIndent = 0, leftIndent = 12, rightIndent = 0)

    Story.append(Paragraph('Discover energy savings and improvements at any stage of your building project through our free <font name="InterstateLight" color=blue><link href="https://www.aspencore.org/energy-concierge">Energy Concierge</link></font> service.', pc291, bulletText=UNCHECKED.encode('UTF8')))
    Story.append(Paragraph('Apply for <font name="InterstateLight" color=blue><link href="https://www.aspencore.org/savings-finder">CORE rebates and grants</link></font>. Rebates of up to $15,000 are available per commercial or multifamily building project.', pc291, bulletText=UNCHECKED.encode('UTF8')))
    Story.append(Paragraph('You may qualify for larger rebates through CORE’s <font name="InterstateLight" color=blue><link href="https://www.aspencore.org/cpp">Community Priority Participant program</link></font>, as well as utility, state, and federal programs. These grants can help cover a portion of the overall project cost for up to $200,0000.', pc291, bulletText=UNCHECKED.encode('UTF8')))
    Story.append(Paragraph('Learn about Building Performance Standards by joining the City of Aspen’s <font name="InterstateLight" color=blue><link href="https://aspen.gov/1245/Building-IQ">BPS Stakeholder Committee</link></font>.', pc291, bulletText=UNCHECKED.encode('UTF8')))

### P2
    Story.append(NextPageTemplate('secondPage'))
    Story.append(FrameBreak)

    column_20 = ColorFrame(doc.leftMargin, doc.bottomMargin, doc.width/3-12, doc.height, showBoundary=0, roundedBackground=CUSTOM_LGRAY, topPadding=10)
    Story.append(Paragraph("CORE partners with the City of Aspen to support you in benchmarking your building’s energy use and finding solutions to reducing greenhouse gas emissions in our community. The simple act of benchmarking can decrease energy use by 2 – 3% per year. Going a step further, you can use your benchmarking data to inform additional measures you can take to reduce your energy consumption. Based on your current benchmarking data, we recommend taking these steps to further reduce your energy use.", tf_standard))
    Story.append(Spacer(1,16))
    Story.append(Paragraph('If this is your second year receiving a scorecard from CORE, and you completed any of CORE’s recommendations, let us know: <font name="InterstateLight" color=blue><link href="mailto:Energy@AspenCORE.org">Energy@AspenCORE.org</link></font>.', tf_standard))
    Story.append(Spacer(1,16))
    Story.append(Paragraph("More questions? We’re here to help. Give us a call at: 1-970-925-9775, x1002.", tf_standard))

    Story.append(FrameBreak)    

    column_21 = Frame(doc.leftMargin + (1/3)*doc.width, doc.bottomMargin, (2/3)*doc.width, doc.height, showBoundary=0, topPadding=0)    
    Story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color= CUSTOM_MGRAY, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='TOP', dash=None))
    Story.append(Spacer(1,12))
    Story.append(Paragraph('Recommendations',tf_standard_bold))
    for cat in ['Lighting', 'Heating and Cooling', 'Building Envelope', 'Electrification', 'Water Heating']:
        cat_name = 'recommendation_' + re.sub(r'(?<=[a-z])(?=[A-Z])|[^a-zA-Z]', ' ', cat).strip().replace(' ', '_').lower()
        Story.append(Paragraph('<font name="InterstateBlack">'+cat+':</font> ' + data_dict[cat_name], tf_standard_spaced))
    Story.append(FrameBreak)

### BUILD PAGE
    page_1_frames = [column_10, column_11, column_12, column_211, column_212, column_22, column_231, column_232, column_24, column_251, column_252, column_253, column_261, column_27, column_281, column_282, column_29]
    page_2_frames = [column_20, column_21]

    templates =[]
    templates.append(PageTemplate(frames=page_1_frames,id='firstPage'))
    templates.append(PageTemplate(frames=page_2_frames,id='secondPage'))

    doc.addPageTemplates(templates)
    style = styles["Normal"]

    #populate story with paragraphs    
    doc.build(Story)

# Run with:  python3 -m label.populate_beam_core
if __name__ == '__main__':
 #   data_dict = {'street': '77 MASSACHUSETTS AVE', 'city': 'CAMBRIGE', 'state': 'MA', 'zipcode': '02139', 'year_built': 1895, 'year_ending': 2022, 'propGrossFloorArea': 10000.0, 'systemDefinedPropertyType': 'Office', 'energy_star_score': 50, 'site_total': 3434,  'siteIntensity': 73.60, 'medianSiteIntensity': 176.40, 'percentBetterThanSiteIntensityMedian': 0.25, 'cons_mmbtu_min': 0, 'siteEnergyUseElectricityGridPurchase': 1000.0, 'siteEnergyUseElectricityGridPurchaseKwh': 100000.0, 'siteEnergyUseNaturalGas': 1000.0, 'siteEnergyUseKerosene': 0.0, 'siteEnergyUsePropane': 1000.0, 'siteEnergyUseDiesel': 0.0, 'siteEnergyUseFuelOil1': 0.0, 'siteEnergyUseFuelOil2': 0.0, 'siteEnergyUseFuelOil4': 0.0, 'siteEnergyUseFuelOil5And6': 0.0, 'siteEnergyUseWood': 0.0, 'energyCost': 10000.0, 'energyCostElectricityOnsiteSolarWind': 2110.0, 'energyCostElectricityGridPurchase': 1000.0, 'energyCostNaturalGas': 1000.0, 'energyCostKerosene': 0.0, 'energyCostPropane': 1000.0, 'energyCostDiesel': 0.0, 'energyCostFuelOil1': 0.0, 'energyCostFuelOil2': 0.0, 'energyCostFuelOil4': 0.0, 'energyCostFuelOil5And6': 0.0, 'energyCostWood': 0.0, 'cons_solar': -11000.0, 'estar_wh': True, 'yoy_percent_change_site_eui': None, 'yoy_percent_change_elec': -0.1, 'totalLocationBasedGHGEmissions': 150, 'onSiteRenewableSystemGeneration': 20000, 'numberOfLevelOneEvChargingStations': 3, 'numberOfLevelTwoEvChargingStations': 0, 'numberOfDcFastEvChargingStations': 0}
    data_dict = {
    "Who is your electricity supplier?": "N/A",
    "city": "Aspen",
    "energyCost": 3060040.48,
    "energyCostDiesel": 0,
    "energyCostDistrictChilledWater": 0,
    "energyCostDistrictHotWater": 0,
    "energyCostDistrictSteam": 0,
    "energyCostElectricityGridPurchase": 263454.42,
    "energyCostElectricityOnsiteSolarWind": 0,
    "energyCostFuelOil1": 0,
    "energyCostFuelOil2": 0,
    "energyCostFuelOil4": 0,
    "energyCostFuelOil5And6": 0,
    "energyCostKerosene": 0,
    "energyCostNaturalGas": 42550.06,
    "energyCostPropane": 0,
    "energyCostWood": 0,
    "energy_star_score": 100.0,
    "medianSiteIntensity": 176.4,
    "numberOfDcFastEvChargingStations": 0,
    "numberOfLevelOneEvChargingStations": 0,
    "numberOfLevelTwoEvChargingStations": 0,
    "onSiteRenewableSystemGeneration": 0,
    "percentBetterThanSiteIntensityMedian": -61.5,
    "percentElectricity": 2.0,
    "propGrossFloorArea": 104000.0,
    "siteEnergyUseDiesel": 0,
    "siteEnergyUseDistrictChilledWater": 0,
    "siteEnergyUseDistrictHotWater": 0,
    "siteEnergyUseDistrictSteam": 0,
    "siteEnergyUseElectricityGridPurchase": 139786.2,
    "siteEnergyUseElectricityGridPurchaseKwh": 40969.0,
    "siteEnergyUseFuelOil1": 0,
    "siteEnergyUseFuelOil2": 0,
    "siteEnergyUseFuelOil4": 0,
    "siteEnergyUseFuelOil5And6": 0,
    "siteEnergyUseKerosene": 0,
    "siteEnergyUseNaturalGas": 6914465.4,
    "siteEnergyUsePropane": 0,
    "siteEnergyUseWood": 0,
    "siteIntensity": 67.8,
    "site_total": 7054.2516,
    "state": "CO",
    "street": "1 Center Street",
    "systemDefinedPropertyType": "Hotel",
    "totalLocationBasedGHGEmissions": 377.4,
    "year_built": 2021,
    "year_ending": 2023,
    "yoy_change_score": 10.0,
    "yoy_percent_change_elec": 10.0,
    "yoy_percent_change_site_eui": 10.0,
    "zipcode": "81611",
    "recommendation_lighting": "Lighting is one of the easiest and most cost-effective upgrades you can make for your business. LEDs have a wide color temperature range, long lifespan (saving on maintenance costs), better quality lighting, and are more affordable than ever. Add proper control systems (daylighting, timers, occupancy sensors, etc.) to maximize the efficiency of your lighting improvement project.",
    "recommendation_heating_and_cooling": "Recommission the building regularly (for example, balance air distribution, verify sensor operation, tune up boilers, etc.) to ensure the building equipment is operating at its maximum efficiency. Replace manual thermostats with Wi-Fi enabled or wireless thermostats, and turn down heating and cooling systems when the building is unoccupied.", 
    "recommendation_building_envelope": "Repair broken windows and weatherstrip or caulk windows and doors where drafts can be felt or there are visible signs of deterioration. Repair and tighten broken and misaligned exterior doors. Install insulating double-pleated blinds on all windows and shut them at night.",
    "recommendation_electrification": "Considering the lifespan of your current heating systems, we recommend you start planning to electrify your building. This includes electrifying heating and cooling systems, and appliances. Electrification offers a lot of benefits, including improved energy efficiency, reduced greenhouse gas emissions, and enhanced occupant comfort and health. And, since technology will only continue to evolve, moving towards electrification now can future-proof your investment and reduce your long-term operating costs.",
    "recommendation_water_heating": "Repair any damaged or missing insulation on pipes and tanks. Look for rust or leaks around the base of the water heater. Repair leaky faucets and install high efficiency shower heads."
}    

    out_file = 'CORE_BEAM_Profile.pdf'
    write_core_profile_pdf(data_dict, out_file)


