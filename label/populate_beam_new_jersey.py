# -*- coding: utf-8 -*-
#! /usr/bin/python
# run with python3 -m label.populate_beam_new_jersey

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
CUSTOM_DTEAL = colors.Color(red=(38.0/255),green=(86.0/255),blue=(145.0/255))

pdfmetrics.registerFont(TTFont('InterstateLight',FONT_PATH+'/InterstateLight.ttf'))
pdfmetrics.registerFont(TTFont('InterstateBlack',FONT_PATH+'/InterstateBlack.ttf'))
#pdfmetrics.registerFont(TTFont('Arial Unicode',FONT_PATH+'/Arial Unicode.ttf'))
pdfmetrics.registerFont(TTFont("FontAwesome", FONT_PATH+"/FontAwesome.ttf"))

def write_new_jersey_profile_pdf(data_dict, output_pdf_path):
#    is_data_valid, msg, data_dict = validate_data_dict(data_dict)
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
    vthep_logo = IMG_PATH+"/NJCEP.png"
    im = Image(vthep_logo, 2.5*inch, 0.79*inch)
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
    
    Story.append(Paragraph("This energy profile details the estimated annual energy costs and expected annual energy usage of this building. This profile recommends actions to achieve more efficiency and energy cost savings.", tf_standard))
    Story.append(Spacer(1,16))
    Story.append(HRFlowable(width="90%", thickness=1, lineCap='round', color=colors.white, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))
    Story.append(Paragraph("BUILDING INFORMATION", pc12))
    Story.append(Paragraph("LOCATION:", pc13))
    Story.append(Paragraph(data_dict['street'],pc14))
    Story.append(Paragraph(data_dict['city'] + ", " + data_dict["state"] + " " + data_dict["zipcode"], pc14))
    Story.append(Paragraph("YEAR BUILT:", pc13))
    Story.append(Paragraph(str(int(data_dict['year_built'])),pc14))
    Story.append(Paragraph("GROSS FLOOR AREA:",pc13))

    floor_area = '{:,.0f}'.format(int(data_dict['propGrossFloorArea'])) if data_dict['propGrossFloorArea'] is not None else 'N/A'
    Story.append(Paragraph(floor_area +' sq.ft.',pc14))
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
    text_c220 = Paragraph("Your building is benchmarked against buildings with similar uses.", tf_standard)
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
    text_c240 = Paragraph("Electricity and fuels estimates are from Energy Star Portfolio Manager", tf_standard)

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
    
    t_achieve, num_line = Highlights.general_commercial(data_dict, FONT_T, FONT_NORMAL, CUSTOM_DGRAY, CHECK_IMG, num_line, ['ghg'])
    
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
    elec_util_map = {"Atlantic City Electric": 'https://www.atlanticcityelectric.com/ways-to-save/for-your-business', "Jersey Central Power & Light": 'https://www.firstenergycorp.com/save_energy/save_energy_new_jersey/for-your-business.html', "Rockland Electric Company": 'https://www.oru.com/en/save-money/rebates-incentives-credits/new-jersey-customers/incentives-for-business-customers-nj', "Public Service Electric & Gas Co.": 'https://bizsave.pseg.com/'}
    gas_util_map = {"Public Service Electric & Gas Co.": 'https://bizsave.pseg.com/', "New Jersey Natural Gas Co.": 'https://www.savegreen.com/businesses/', "Elizabethtown Gas Co.": 'https://www.elizabethtowngas.com/business/business-service/energy-efficiency-incentives', "South Jersey Gas Co.": 'https://southjerseygas.com/save-energy-money/commercial-savings'}
                
    column_29 = Frame(doc.leftMargin+doc.width/3, doc.bottomMargin, (2/3)*doc.width, 0.17*doc.height, showBoundary=0, topPadding=0)    
    Story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color= CUSTOM_MGRAY, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='TOP', dash=None))        
    pc291 = ParagraphStyle('body_left', alignment = TA_LEFT, textColor = CUSTOM_DGRAY, fontSize = FONT_T, fontName = FONT_NORMAL,  spaceBefore = 6, spaceAfter = 0, leading=10, backColor = 'white', bulletIndent = 12, firstLineIndent = 0, leftIndent = 12, rightIndent = 0)

    Story.append(Paragraph('Find and participate in utility <font name="InterstateLight" color=blue><link href="https://cepfindaprogram.com/">energy efficiency programs</link></font> that may offer rebates, incentives, and financing for energy efficiency projects', pc291, bulletText=UNCHECKED.encode('UTF8')))
    if 'elec_util' in data_dict:
        if data_dict['elec_util'] == 'Atlantic City Electric':
            Story.append(Paragraph('For more information on electric energy efficiency programs from ACE please visit <font name="InterstateLight" color=blue><link href="'+ elec_util_map[data_dict['elec_util']] +'">here</link></font>', pc291, bulletText=UNCHECKED.encode('UTF8')))
        elif data_dict['elec_util'] == 'Jersey Central Power & Light':
            Story.append(Paragraph('For more information on electric energy efficiency programs from JCP&L please visit <font name="InterstateLight" color=blue><link href="'+ elec_util_map[data_dict['elec_util']] +'">here</link></font>', pc291, bulletText=UNCHECKED.encode('UTF8')))
        elif data_dict['elec_util'] == 'Rockland Electric Company':
            Story.append(Paragraph('For more information on electric energy efficiency programs from RECO please visit <font name="InterstateLight" color=blue><link href="'+ elec_util_map[data_dict['elec_util']] +'">here</link></font>', pc291, bulletText=UNCHECKED.encode('UTF8')))
        elif data_dict['elec_util'] == 'Public Service Electric & Gas Co.':
            Story.append(Paragraph('For more information on electric energy efficiency programs from PSEG please visit <font name="InterstateLight" color=blue><link href="'+ elec_util_map[data_dict['elec_util']] +'">here</link></font>', pc291, bulletText=UNCHECKED.encode('UTF8')))
    if 'gas_util' in data_dict:
        if data_dict['gas_util'] == "Public Service Electric & Gas Co.":
            Story.append(Paragraph('For more information on gas energy efficiency programs from PSE&G please visit <font name="InterstateLight" color=blue><link href="'+ gas_util_map[data_dict['gas_util']] +'">here</link></font>', pc291, bulletText=UNCHECKED.encode('UTF8')))
        elif data_dict['gas_util'] == "New Jersey Natural Gas Co.":
            Story.append(Paragraph('For more information on gas energy efficiency programs from NJNG please visit <font name="InterstateLight" color=blue><link href="'+ gas_util_map[data_dict['gas_util']] +'">here</link></font>', pc291, bulletText=UNCHECKED.encode('UTF8')))
        elif data_dict['gas_util'] == "Elizabethtown Gas Co.":
            Story.append(Paragraph('For more information on gas energy efficiency programs from ETG please visit <font name="InterstateLight" color=blue><link href="'+ gas_util_map[data_dict['gas_util']] +'">here</link></font>', pc291, bulletText=UNCHECKED.encode('UTF8')))
        elif data_dict['gas_util'] == "South Jersey Gas Co.":
            print(gas_util_map[data_dict['gas_util']])
            Story.append(Paragraph('For more information on gas energy efficiency programs from SJG please visit <font name="InterstateLight" color=blue><link href="'+ gas_util_map[data_dict['gas_util']] +'">here</link></font>', pc291, bulletText=UNCHECKED.encode('UTF8')))
    if ('elec_util' not in data_dict) or ('gas_util' not in data_dict):
        Story.append(Paragraph('For more information on clean energy programs in New Jersey, please visit <font name="InterstateLight" color=blue><link href="https://njcleanenergy.com/">here</link></font>', pc291, bulletText=UNCHECKED.encode('UTF8')))
    if ('elec_util' not in data_dict) and ('gas_util' not in data_dict):
        Story.append(Paragraph('For updates on NJ Clean Energy Programs, sign up for our listserv <font name="InterstateLight" color=blue><link href="https://visitor.r20.constantcontact.com/manage/optin?v=0014Ogu2wnBvl-XKzALEMAxRqHXXZqN78wNyahRWbOreRRMtzq_QzwtCSVAeJ4-mvFkT6N7t6li4b0SEm4afBVp0eglXB6n7Alv_0qga5-fWDg7u8q616oLKq7j72BhCjBqSBTMB0SxXFIZ0OgxRcIkwbL7iZ8-NnO5hV7zANu6Bgs%3D">here</link></font>', pc291, bulletText=UNCHECKED.encode('UTF8')))
    Story.append(Paragraph('Schedule a professional energy audit to identify cost-saving upgrades <font name="InterstateLight" color=blue><link href="https://urldefense.com/v3/__https:/cepfindaprogram.com/transition.html?id=10__;!!J30X0ZrnC1oQtbA!LL2ig9UvQoa3DMO6p5zsREk0kMQg3ifH8YvjF_ucmeiMfkEJWQSZbK4bPIWRYyoLvj_RZzImuEcgpSvQp4xQLxNu6rpGEmFa$">here</link></font>.', pc291, bulletText=UNCHECKED.encode('UTF8')))
    Story.append(Paragraph('If your ENERGY STAR score is 75 or higher, you may be eligible for an ENERGY STAR certification. This certification shows that your building is more efficient than 75% of similar buildings nationwide. For more information, click <font name="InterstateLight" color=blue><link href="https://urldefense.com/v3/__https:/www.energystar.gov/buildings/building-recognition/building-certification/how-apply__;!!J30X0ZrnC1oQtbA!LL2ig9UvQoa3DMO6p5zsREk0kMQg3ifH8YvjF_ucmeiMfkEJWQSZbK4bPIWRYyoLvj_RZzImuEcgpSvQp4xQLxNu6s5DMxye$">here</link></font>', pc291, bulletText=UNCHECKED.encode('UTF8')))


#Spell out units in the Annual Energy Usage section (people won't understand MMBTU)

### BUILD PAGE
    page_1_frames = [column_10, column_11, column_12, column_211, column_212, column_22, column_231, column_232, column_24, column_251, column_252, column_253, column_261, column_27, column_281, column_282, column_29]
    templates =[]
    templates.append(PageTemplate(frames=page_1_frames,id='firstPage'))
    doc.addPageTemplates(templates)
    style = styles["Normal"]

    #populate story with paragraphs    
    doc.build(Story)

# Run with:  python3 -m label.populate_beam_new_jersey
if __name__ == '__main__':
    data_dict = {
        "Who is your electricity supplier?": "N/A",
        "city": "JERSEY CITY",
        "energyCost": 318753.47,
        "energyCostDiesel": 0,
        "energyCostDistrictChilledWater": 0,
        "energyCostDistrictHotWater": 0,
        "energyCostDistrictSteam": 0,
        "energyCostElectricityGridPurchase": 265659.13,
        "energyCostElectricityOnsiteSolarWind": 0,
        "energyCostFuelOil1": 0,
        "energyCostFuelOil2": 0,
        "energyCostFuelOil4": 0,
        "energyCostFuelOil5And6": 0,
        "energyCostKerosene": 0,
        "energyCostNaturalGas": 66310.05,
        "energyCostPropane": 0,
        "energyCostWood": 0,
        "energy_star_score": 71.00,
        "medianSiteIntensity": 176.4,
        "numberOfDcFastEvChargingStations": 0,
        "numberOfLevelOneEvChargingStations": 0,
        "numberOfLevelTwoEvChargingStations": 0,
        "onSiteRenewableSystemGeneration": 0,
        "percentBetterThanSiteIntensityMedian": -61.5,
        "percentElectricity": 2.0,
        "propGrossFloorArea": 149326.00,
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
        "state": "NJ",
        "street": "1 BRUCE WAY",
        "systemDefinedPropertyType": "Office",
        "totalLocationBasedGHGEmissions": 555.3,
        "year_built": 1987,
        "year_ending": 2023,
        "yoy_change_score": 10.0,
        "yoy_percent_change_elec": 15.2,
        "yoy_percent_change_ng": None,
        "yoy_percent_change_site_eui": 15.3,
        "zipcode": "89501",
        "elec_util": "Public Service Electric & Gas Co.",
        "gas_util": "South Jersey Gas Co."
    }
#        "gas_util": "Public Service Electric & Gas Co."

    out_file = 'NJ_BEAM_Profile.pdf'
    write_new_jersey_profile_pdf(data_dict, out_file)
