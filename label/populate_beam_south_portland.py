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
CUSTOM_DTEAL = colors.Color(red=(54.0/255),green=(109.0/255),blue=(238.0/255)) ## This is the color to customize

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
    y_offset += 0.02
    text_c231, text_c232 = Highlights.cost_box(data_dict)
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
#    data_dict = {'street': '77 MASSACHUSETTS AVE', 'city': 'CAMBRIGE', 'state': 'MA', 'zipcode': '02139', 'year_built': 1895, 'year_ending': 2022, 'propGrossFloorArea': 100000.0, 'systemDefinedPropertyType': 'Office', 'energy_star_score': 50, 'site_total': 3434,  'medianSiteIntensity': 50, 'percentBetterThanSiteIntensityMedian': 0.25, 'cons_mmbtu_min': 0, 'siteEnergyUseElectricityGridPurchase': 1000.0, 'siteEnergyUseElectricityGridPurchaseKwh': 100000.0, 'siteEnergyUseNaturalGas': 1000.0, 'siteEnergyUseKerosene': 0.0, 'siteEnergyUsePropane': 1000.0, 'siteEnergyUseDiesel': 0.0, 'siteEnergyUseFuelOil1': 0.0, 'siteEnergyUseFuelOil2': 0.0, 'siteEnergyUseFuelOil4': 0.0, 'siteEnergyUseFuelOil5And6': 0.0, 'siteEnergyUseWood': 0.0, 'energyCost': 10000.0, 'energyCostElectricityOnsiteSolarWind': 2110.0, 'energyCostElectricityGridPurchase': 1000.0, 'energyCostNaturalGas': 1000.0, 'energyCostKerosene': 0.0, 'energyCostPropane': 1000.0, 'energyCostDiesel': 0.0, 'energyCostFuelOil1': 0.0, 'energyCostFuelOil2': 0.0, 'energyCostFuelOil4': 0.0, 'energyCostFuelOil5And6': 0.0, 'energyCostWood': 0.0, 'cons_solar': -11000.0, 'estar_wh': True, 'yoy_percent_change_site_eui_2022': None, 'yoy_percent_change_elec_2022': -0.1, 'totalLocationBasedGHGEmissions': 150, 'onSiteRenewableSystemGeneration': 20000, 'numberOfLevelOneEvChargingStations': 3, 'numberOfLevelTwoEvChargingStations': 0, 'numberOfDcFastEvChargingStations': 0}
    
#    data_dict = {'property_name': 'My Property', 'street': '220 VIRGINIA AVE', 'city': 'South Portland', 'state': 'ME', 'zipcode': '04106', 'year_built': 1991, 'year_ending': '2022', 'systemDefinedPropertyType': 'Laboratory', 'propGrossFloorArea': 212000.0, 'energy_star_score': None, 'site_total': 17844.3429, 'medianSiteIntensity': None, 'percentBetterThanSiteIntensityMedian': -41.3, 'yoy_percent_change_site_eui_2022': None, 'yoy_percent_change_elec_2022': None, 'numberOfLevelOneEvChargingStations': 0, 'numberOfLevelTwoEvChargingStations': 0, 'numberOfDcFastEvChargingStations': 0, 'onSiteRenewableSystemGeneration': 0, 'siteEnergyUseElectricityGridPurchase': 3563328.8, 'siteEnergyUseElectricityGridPurchaseKwh': 1044351.8, 'siteEnergyUseNaturalGas': 4281014.1, 'siteEnergyUseKerosene': 0, 'siteEnergyUsePropane': 0, 'siteEnergyUseDiesel': 0, 'siteEnergyUseFuelOil1': 0, 'siteEnergyUseFuelOil2': 0, 'siteEnergyUseFuelOil4': 0, 'siteEnergyUseFuelOil5And6': 0, 'siteEnergyUseWood': 0, 'energyCost': 272755.54, 'energyCostElectricityOnsiteSolarWind': 0, 'energyCostElectricityGridPurchase': 211913.96, 'energyCostNaturalGas': 60841.58, 'energyCostKerosene': 0, 'energyCostPropane': 0, 'energyCostDiesel': 0, 'energyCostFuelOil1': 0, 'energyCostFuelOil2': 0, 'energyCostFuelOil4': 0, 'energyCostFuelOil5And6': 0, 'energyCostWood': 0, 'totalLocationBasedGHGEmissions': 485.1, 'siteEnergyUseFuelOil': 0, 'energyCostFuelOil': 0, 'energyRateElectricityGridPurchase': 0.059470784733645685, 'energyRateNaturalGas': 0.014211955059900411}
#    data_dict = {'street': 'N/A', 'city': 'South Portland', 'state': 'ME', 'zipcode': '04106', 'year_built': 1970, 'year_ending': '2022', 'systemDefinedPropertyType': 'Parking', 'propGrossFloorArea': 174000.0, 'energy_star_score': None, 'site_total': 30.9121, 'medianSiteIntensity': None, 'percentBetterThanSiteIntensityMedian': None, 'yoy_percent_change_site_eui_2022': None, 'yoy_percent_change_elec_2022': None, 'numberOfLevelOneEvChargingStations': 0, 'numberOfLevelTwoEvChargingStations': 0, 'numberOfDcFastEvChargingStations': 0, 'onSiteRenewableSystemGeneration': 0, 'siteEnergyUseElectricityGridPurchase': 30912.1, 'siteEnergyUseElectricityGridPurchaseKwh': 9059.8, 'siteEnergyUseNaturalGas': 0, 'siteEnergyUseKerosene': 0, 'siteEnergyUsePropane': 0, 'siteEnergyUseDiesel': 0, 'siteEnergyUseFuelOil1': 0, 'siteEnergyUseFuelOil2': 0, 'siteEnergyUseFuelOil4': 0, 'siteEnergyUseFuelOil5And6': 0, 'siteEnergyUseWood': 0, 'energyCost': 1183.56, 'energyCostElectricityOnsiteSolarWind': 0, 'energyCostElectricityGridPurchase': 1183.56, 'energyCostNaturalGas': 0, 'energyCostKerosene': 0, 'energyCostPropane': 0, 'energyCostDiesel': 0, 'energyCostFuelOil1': 0, 'energyCostFuelOil2': 0, 'energyCostFuelOil4': 0, 'energyCostFuelOil5And6': 0, 'energyCostWood': 0, 'totalLocationBasedGHGEmissions': 2.2}
#    data_dict = {'street': '1338 BROADWAY', 'city': 'South Portland', 'state': 'ME', 'zipcode': '04106', 'year_built': 1940, 'year_ending': 2023, 'systemDefinedPropertyType': 'K-12 School', 'Who is your electricity supplier?': 'N/A', 'propGrossFloorArea': 24636.0, 'energy_star_score': 69.0, 'site_total': 1780.6341, 'siteIntensity': 72.3, 'medianSiteIntensity': 89.1, 'percentBetterThanSiteIntensityMedian': -18.9, 'yoy_percent_change_site_eui_2022': None, 'yoy_percent_change_elec_2022': None, 'numberOfLevelOneEvChargingStations': 0, 'numberOfLevelTwoEvChargingStations': 0, 'numberOfDcFastEvChargingStations': 0, 'onSiteRenewableSystemGeneration': 0, 'siteEnergyUseElectricityGridPurchase': 147831.2, 'siteEnergyUseElectricityGridPurchaseKwh': 43326.8, 'siteEnergyUseNaturalGas': 1632802.9, 'siteEnergyUseKerosene': 0, 'siteEnergyUsePropane': 0, 'siteEnergyUseDiesel': 0, 'siteEnergyUseFuelOil1': 0, 'siteEnergyUseFuelOil2': 0, 'siteEnergyUseFuelOil4': 0, 'siteEnergyUseFuelOil5And6': 0, 'siteEnergyUseWood': 0, 'energyCost': 33797.19, 'energyCostElectricityOnsiteSolarWind': 0, 'energyCostElectricityGridPurchase': 10096.94, 'energyCostNaturalGas': 23700.25, 'energyCostKerosene': 0, 'energyCostPropane': 0, 'energyCostDiesel': 0, 'energyCostFuelOil1': 0, 'energyCostFuelOil2': 0, 'energyCostFuelOil4': 0, 'energyCostFuelOil5And6': 0, 'energyCostWood': 0, 'totalLocationBasedGHGEmissions': 97.4}
#    data_dict = {'street': 'PO BOX 10001', 'city': 'DALLAS', 'state': 'N/A', 'zipcode': '04106', 'year_built': 1983, 'year_ending': datetime.date(2022, 12, 31), 'systemDefinedPropertyType': 'Retail Store', 'Who is your electricity supplier?': 'N/A', 'propGrossFloorArea': None, 'energy_star_score': 93.0, 'site_total': 3171.1687, 'siteIntensity': None, 'medianSiteIntensity': None, 'percentBetterThanSiteIntensityMedian': -48.5, 'yoy_percent_change_site_eui_2022': None, 'yoy_percent_change_elec_2022': None, 'numberOfLevelOneEvChargingStations': 0, 'numberOfLevelTwoEvChargingStations': 0, 'numberOfDcFastEvChargingStations': 0, 'onSiteRenewableSystemGeneration': 0, 'siteEnergyUseElectricityGridPurchase': 1564354.3, 'siteEnergyUseElectricityGridPurchaseKwh': 458486.0, 'siteEnergyUseNaturalGas': 1606814.4, 'siteEnergyUseKerosene': 0, 'siteEnergyUsePropane': 0, 'siteEnergyUseDiesel': 0, 'siteEnergyUseFuelOil1': 0, 'siteEnergyUseFuelOil2': 0, 'siteEnergyUseFuelOil4': 0, 'siteEnergyUseFuelOil5And6': 0, 'siteEnergyUseWood': 0, 'energyCost': 0, 'energyCostElectricityOnsiteSolarWind': 0, 'energyCostElectricityGridPurchase': 0, 'energyCostNaturalGas': 0, 'energyCostKerosene': 0, 'energyCostPropane': 0, 'energyCostDiesel': 0, 'energyCostFuelOil1': 0, 'energyCostFuelOil2': 0, 'energyCostFuelOil4': 0, 'energyCostFuelOil5And6': 0, 'energyCostWood': 0, 'totalLocationBasedGHGEmissions': 196.2}
#    data_dict = {'street': '181 WORCESTER RD, SUITE 200', 'city': 'South Portland', 'state': 'ME', 'zipcode': '04106', 'year_built': 1900, 'year_ending': 2023, 'systemDefinedPropertyType': 'Multifamily Housing', 'Who is your electricity supplier?': 'N/A', 'propGrossFloorArea': 20000.0, 'energy_star_score': 100.0, 'site_total': 6.209, 'siteIntensity': 1.1, 'medianSiteIntensity': 75.1, 'percentBetterThanSiteIntensityMedian': -98.6, 'yoy_percent_change_site_eui_2022': None, 'yoy_percent_change_elec_2022': None, 'numberOfLevelOneEvChargingStations': 0, 'numberOfLevelTwoEvChargingStations': 0, 'numberOfDcFastEvChargingStations': 0, 'onSiteRenewableSystemGeneration': 0, 'siteEnergyUseElectricityGridPurchase': 6209.0, 'siteEnergyUseElectricityGridPurchaseKwh': 1819.7, 'siteEnergyUseNaturalGas': 0, 'siteEnergyUseKerosene': 0, 'siteEnergyUsePropane': 15097.2, 'siteEnergyUseDiesel': 0, 'siteEnergyUseFuelOil1': 0, 'siteEnergyUseFuelOil2': 0, 'siteEnergyUseFuelOil4': 0, 'siteEnergyUseFuelOil5And6': 0, 'siteEnergyUseWood': 0, 'energyCost': 0, 'energyCostElectricityOnsiteSolarWind': 0, 'energyCostElectricityGridPurchase': 0, 'energyCostNaturalGas': 0, 'energyCostKerosene': 0, 'energyCostPropane': 0, 'energyCostDiesel': 0, 'energyCostFuelOil1': 0, 'energyCostFuelOil2': 0, 'energyCostFuelOil4': 0, 'energyCostFuelOil5And6': 0, 'energyCostWood': 0, 'totalLocationBasedGHGEmissions': 1.4}
    data_dict = {'street': '150 Black Point Rd', 'city': 'South Portland', 'state': 'ME', 'zipcode': '04106', 'year_built': 1950, 'year_ending': 2023, 'systemDefinedPropertyType': 'N/A', 'Who is your electricity supplier?': 'N/A', 'propGrossFloorArea': None, 'energy_star_score': None, 'site_total': 1456.3383, 'siteIntensity': None, 'medianSiteIntensity': None, 'percentBetterThanSiteIntensityMedian': None, 'yoy_percent_change_site_eui_2022': None, 'yoy_percent_change_elec_2022': None, 'numberOfLevelOneEvChargingStations': 0, 'numberOfLevelTwoEvChargingStations': 0, 'numberOfDcFastEvChargingStations': 0, 'onSiteRenewableSystemGeneration': 0, 'siteEnergyUseElectricityGridPurchase': 168362.9, 'siteEnergyUseElectricityGridPurchaseKwh': 49344.3, 'siteEnergyUseNaturalGas': 1176954.4, 'siteEnergyUseKerosene': 0, 'siteEnergyUsePropane': 0, 'siteEnergyUseDiesel': 0, 'siteEnergyUseFuelOil1': 0, 'siteEnergyUseFuelOil2': 111021.0, 'siteEnergyUseFuelOil4': 0, 'siteEnergyUseFuelOil5And6': 0, 'siteEnergyUseWood': 0, 'energyCost': 29889.39, 'energyCostElectricityOnsiteSolarWind': 0, 'energyCostElectricityGridPurchase': 9072.82, 'energyCostNaturalGas': 18169.2, 'energyCostKerosene': 0, 'energyCostPropane': 0, 'energyCostDiesel': 0, 'energyCostFuelOil1': 0, 'energyCostFuelOil2': 2647.37, 'energyCostFuelOil4': 0, 'energyCostFuelOil5And6': 0, 'energyCostWood': 0, 'totalLocationBasedGHGEmissions': 82.9}
#    data_dict = {'street': '240 Ocean Street', 'city': 'South Portland', 'state': 'ME', 'zipcode': '04106', 'year_built': 1940, 'year_ending': 2023, 'systemDefinedPropertyType': 'K-12 School', 'Who is your electricity supplier?': 'N/A', 'propGrossFloorArea': 93090.0, 'energy_star_score': None, 'site_total': 0, 'siteIntensity': None, 'medianSiteIntensity': 48.5, 'percentBetterThanSiteIntensityMedian': None, 'yoy_percent_change_site_eui_2022': None, 'yoy_percent_change_elec_2022': None, 'numberOfLevelOneEvChargingStations': 0, 'numberOfLevelTwoEvChargingStations': 0, 'numberOfDcFastEvChargingStations': 0, 'onSiteRenewableSystemGeneration': 0, 'siteEnergyUseElectricityGridPurchase': 0, 'siteEnergyUseElectricityGridPurchaseKwh': 0, 'siteEnergyUseNaturalGas': 0, 'siteEnergyUseKerosene': 0, 'siteEnergyUsePropane': 0, 'siteEnergyUseDiesel': 0, 'siteEnergyUseFuelOil1': 0, 'siteEnergyUseFuelOil2': 0, 'siteEnergyUseFuelOil4': 0, 'siteEnergyUseFuelOil5And6': 0, 'siteEnergyUseWood': 0, 'energyCost': 0, 'energyCostElectricityOnsiteSolarWind': 0, 'energyCostElectricityGridPurchase': 0, 'energyCostNaturalGas': 0, 'energyCostKerosene': 0, 'energyCostPropane': 0, 'energyCostDiesel': 0, 'energyCostFuelOil1': 0, 'energyCostFuelOil2': 0, 'energyCostFuelOil4': 0, 'energyCostFuelOil5And6': 0, 'energyCostWood': 0, 'totalLocationBasedGHGEmissions': 0, 'percentElectricity': 0}

    out_file = 'South_Portland_BEAM_Profile.pdf'
    write_south_portland_profile_pdf(data_dict, out_file)


