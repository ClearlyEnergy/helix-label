# -*- coding: utf-8 -*-
#! /usr/bin/python
# run with python3 -m label.populate_madison_orlando

import csv
import os
import time
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.lib.validators import Auto
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Flowable, Frame, FrameBreak, HRFlowable, Image, NextPageTemplate, PageBreak, PageTemplate,Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  
from label.utils.utils import ColorFrame, ColorFrameSimpleDocTemplate, Highlights
import datetime

#Adding Arial Unicode for checkboxes
module_path = os.path.abspath(os.path.dirname(__file__))
FONT_PATH = os.path.normpath(os.path.join(module_path, ".fonts"))
IMG_PATH = os.path.normpath(os.path.join(module_path, "images"))

pdfmetrics.registerFont(TTFont('InterstateLight',FONT_PATH+'/InterstateLight.ttf'))
pdfmetrics.registerFont(TTFont('InterstateBlack',FONT_PATH+'/InterstateBlack.ttf'))
#pdfmetrics.registerFont(TTFont('Arial Unicode',FONT_PATH+'/Arial Unicode.ttf'))
pdfmetrics.registerFont(TTFont("FontAwesome", FONT_PATH+"/FontAwesome.ttf"))

CUSTOM_LGRAY = colors.Color(red=(242.0/255),green=(246.0/255),blue=(248.0/255))
CUSTOM_DGRAY = colors.Color(red=(109.0/255),green=(111.0/255),blue=(106.0/255))
CUSTOM_MGRAY = colors.Color(red=(111.0/255),green=(111.0/255),blue=(106.0/255))
CUSTOM_LGREEN = colors.Color(red=(209.0/255),green=(229.0/255),blue=(202.0/255))
CUSTOM_DGREEN = colors.Color(red=(65.0/255),green=(173.0/255),blue=(73.0/255))
CUSTOM_MGREEN = colors.Color(red=(74.0/255),green=(151.0/255),blue=(93.0/255))
CUSTOM_ELECGREEN = colors.Color(red=(113.0/255),green=(168.0/255),blue=(80.0/255))
CUSTOM_LORANGE = colors.Color(red=(242.0/255),green=(151.0/255),blue=(152.0/255))
CUSTOM_ORANGE = colors.Color(red=(217.0/255),green=(92.0/255),blue=(35.0/255))
CUSTOM_YELLOW = colors.Color(red=(255.0/255),green=(221.0/255),blue=(0.0/255))
CUSTOM_LTEAL = colors.Color(red=(53.0/255),green=(196.0/255),blue=(229.0/255))
CUSTOM_DTEAL = colors.Color(red=(0.0/255),green=(0.0/255),blue=(128.0/255)) ## This is the color to customize
FUELS = ['ElectricityGridPurchase', 'NaturalGas', 'FuelOil', 'Propane',  'Wood']
#FUELICONS = [u"",u"\uf06d",u"\uf043",u"\uf043",u"\uf1bb",u"\uf185"]
FUELICONS = [u"\uf0e7",u"\uf06d",u"\uf043",u"\uf043",u"\uf1bb",u"\uf185"]
FUELIMAGES = [Image(IMG_PATH+"/HomeEnergyProfile_icons-03.png",0.4*inch,0.4*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-09.png",0.4*inch,0.4*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-10.png",0.4*inch,0.4*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-11.png",0.4*inch,0.4*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-02.png",0.4*inch,0.4*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-02.png",0.4*inch,0.4*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-04.png",0.4*inch,0.4*inch)]
FUELIMAGESSMALL = [Image(IMG_PATH+"/HomeEnergyProfile_icons-03.png",0.3*inch,0.3*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-09.png",0.3*inch,0.3*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-10.png",0.3*inch,0.3*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-11.png",0.3*inch,0.3*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-02.png",0.3*inch,0.3*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-02.png",0.3*inch,0.3*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-04.png",0.3*inch,0.3*inch)]
FUELLABEL = ['Electric', 'Natural Gas', 'Heating Oil', 'Propane', 'Wood']
FUELUNIT = ['kwh', 'ccf', 'gal', 'gal', 'ton']
FUELCOLOR = [CUSTOM_ELECGREEN, CUSTOM_ORANGE, CUSTOM_DTEAL, CUSTOM_LTEAL, CUSTOM_MGREEN]


class flowable_triangle(Flowable):
    def __init__(self, imgdata, offset_x, offset_y, height, width, text, side='right'):
        Flowable.__init__(self)
        self.img = ImageReader(imgdata)
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.height = height
        self.width = width
        self.text = text
        self.side = side

    def draw(self):
        self.canv.drawImage(self.img, self.offset_x*inch, self.offset_y*inch, height = self.height*inch, width=self.width*inch)
        self.canv.setFont("InterstateBlack", 7)
        self.canv.setFillColor(colors.gray)
        t = self.canv.beginText()
#        t.setFont("FontAwesome", 30)
        if self.side == 'right':
            t.setTextOrigin((self.offset_x)*inch, (self.offset_y-0.1)*inch)
        elif self.side == 'left':
            t.setTextOrigin((self.offset_x-0.4)*inch, (self.offset_y-0.1)*inch)
        elif self.side == 'low':
            t.setTextOrigin((self.offset_x)*inch, (self.offset_y-0.3)*inch)
        elif self.side == 'high':
            t.setTextOrigin((self.offset_x)*inch, (self.offset_y+0.1)*inch)
        t.textLines(self.text)
        self.canv.drawText(t)
#        self.canv.drawString(self.offset_x*inch, (self.offset_y-0.1)*inch, self.text)

class flowable_text(Flowable):
    def __init__(self, offset_x, offset_y, text, font_size):
        Flowable.__init__(self)
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.text = text
        self.font_size = font_size
        
    def draw(self):
        self.canv.setFont("InterstateBlack", self.font_size)
        self.canv.setFillColor(colors.gray)
        self.canv.drawString(self.offset_x*inch, (self.offset_y-0.1)*inch, self.text)        
    
def pie_chart(data_dict):
    drawing = Drawing(width=1.0*inch, height=1.0*inch)
    data = []
    labels = []
    order = []

    for num, fuel in enumerate(FUELS):
        if data_dict['energyCost'+fuel] > 0:
            data.append(int(data_dict['energyCost'+fuel]))
#            txt += FUELLABEL[num]
            labels.append(FUELICONS[num])
            order.append(num)
    pie = Pie()
    pie.sideLabels = False
    pie.x = 5
    pie.y = 10
    pie.width = 1.0*inch
    pie.height = 1.0*inch
    pie.data = data
#    pie.labels = labels
    pie.slices.strokeColor = colors.white
    pie.slices.strokeWidth = 0.01
    pie.simpleLabels = 0
    for i in range(len(data)):
        pie.slices[i].labelRadius = 0.5
        pie.slices[i].fillColor = FUELCOLOR[order[i]]
        pie.slices[i].fontName = 'FontAwesome'
        pie.slices[i].fontSize = 16
    drawing.add(pie)
    return drawing
    
def map_scores(property_type):
    espm_score_mapping = {}
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'utils/energy_star_score.csv')
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            espm_score_mapping[row['Category']] = row
    return espm_score_mapping[property_type]

def write_lexington_profile_pdf(data_dict, output_pdf_path):
    doc = ColorFrameSimpleDocTemplate(output_pdf_path,pagesize=letter,rightMargin=20,leftMargin=20,topMargin=20,bottomMargin=20)
    styles = getSampleStyleSheet()                 
    font_xxl =30
    font_xl = 24
    font_ll = 16
    font_l = 14
    font_ml = 12
    font_h = 10
    font_t = 9
    font_s = 8
    font_normal = 'InterstateLight'
    font_bold = 'InterstateBlack'
    checked = u"\u2713"
    unchecked = u"\u2752"
    check_img = IMG_PATH+"/HomeEnergyProfile_icons-13.png"
    leq = u"\u2264"
    geq = u"\u2265"
    registered = u"\u00AE"
    space = u"\u0009"
    page2 = False
    
    colors_lgreen = ''

    Story=[]
    #Standard text formats
    tf_standard = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = font_h, fontName = font_normal, textColor = CUSTOM_DGRAY, leading = 14)  
    tf_standard_bold = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = font_h, fontName = font_bold, textColor = CUSTOM_DGRAY, leading = 14)  
    tf_small = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = font_s, fontName = font_normal, textColor = CUSTOM_DGRAY, spaceBefore = 12, spaceAfter = 12)  
    tf_small_squished = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = font_s, fontName = font_normal, textColor = CUSTOM_DGRAY, spaceBefore = 6, spaceAfter = 0)  
    tf_small_right = ParagraphStyle('standard', alignment = TA_RIGHT, fontSize = font_s, fontName = font_normal, textColor = CUSTOM_DGRAY, spaceBefore = 6, spaceAfter = 0)  
    tf_small_bold = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = font_s, fontName = font_bold, textColor = CUSTOM_DGRAY, spaceBefore = 6, spaceAfter = 0)  
    
    ### P1
    # Logo
    column_10 = Frame(doc.leftMargin, doc.height-0.1*doc.height, doc.width/3-12, 0.13*doc.height, showBoundary=0)    
    vthep_logo = IMG_PATH+"/lexington.png"
    im = Image(vthep_logo, 1.122*inch, 1.1*inch)
    Story.append(im)
    Story.append(FrameBreak)
    
    # Cost Box
    column_11 = ColorFrame(doc.leftMargin, doc.height-0.23*doc.height, doc.width/3-12, 0.13*doc.height, showBoundary=0, roundedBackground=CUSTOM_DTEAL, topPadding=10)    
    pc101 = ParagraphStyle('column_1', alignment = TA_CENTER, fontSize = font_h, fontName = font_bold, textColor=colors.white, leading=14)
    pc102 = ParagraphStyle('column_1', alignment = TA_CENTER, fontSize = font_xxl, fontName = font_bold, textColor = colors.white)
    pc103 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = font_s, fontName = font_bold, textColor = colors.white, spaceBefore=26)
    text_c101 = Paragraph("ENERGY STAR SCORE", pc101)
    text_c102 = Paragraph(str(int(data_dict['energy_star_score']))+'/100', pc102)
    text_c103 = Paragraph('50=median, 75=high performer', pc103)
    Story.append(text_c101)
    Story.append(text_c102)
    Story.append(text_c103)
    Story.append(FrameBreak)

    # Text Column
    column_12 = ColorFrame(doc.leftMargin, doc.bottomMargin, doc.width/3-12, 0.72*doc.height, showBoundary=0, roundedBackground=CUSTOM_LGRAY, topPadding=10)
    pc12 = ParagraphStyle('column_1', alignment = TA_LEFT, fontSize = font_ml, fontName = font_bold, textColor = CUSTOM_DTEAL, leading = 14, spaceBefore = 16)
    pc13 = ParagraphStyle('column_1', alignment = TA_LEFT, fontSize = font_h, fontName = font_bold, textColor = CUSTOM_DGRAY, leading = 12, spaceBefore = 4)
    pc14 = ParagraphStyle('column_1', alignment = TA_LEFT, fontSize = font_t, fontName = font_normal, textColor = CUSTOM_DGRAY, leading = 12)
    
    Story.append(Paragraph("Thank you for your compliance with Lexington’s Building Energy Use Disclosure (BEU-D) bylaw. This Building Energy Profile details your building’s energy use compared to the other buildings in Lexington that fall under the bylaw’s reporting requirement. It also highlights actions you can take to achieve more efficiency and energy cost savings.", tf_standard))
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
    pc201 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = font_ll, fontName = font_bold, textColor = colors.white)
    text_c201 = Paragraph(str(int(data_dict['site_total']))+"<font size=10> MMBtu </font>", pc201)
    Story.append(text_c201)
    Story.append(FrameBreak)
    
    column_212 = Frame(doc.leftMargin+doc.width/3+(1/4)*(2/3)*doc.width, doc.height*(1-y_offset), (3/4)*(2/3)*doc.width, 0.04*doc.height, showBoundary=0, topPadding=10)    
    pc202 = ParagraphStyle('column_2', alignment = TA_LEFT, fontSize = font_l, fontName = font_bold, textColor = CUSTOM_DTEAL)
    text_c202 = Paragraph('Annual Energy Usage', pc202)
    Story.append(text_c202)
    Story.append(FrameBreak)

    y_offset += 0.28
    column_22 = Frame(doc.leftMargin+doc.width/3, doc.height*(1-y_offset), (2/3)*doc.width, (y_offset-0.04)*doc.height, showBoundary=0, topPadding=10)    
    Story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color= CUSTOM_MGRAY, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='TOP', dash=None))
    text_c220 = Paragraph("The building energy use with 0 being a net zero building", tf_standard)
    Story.append(text_c220)
    
    # Wedge - start at 0.62 end at 4.82
    espm_score_mapping = {}
    with open('label/utils/energy_star_score.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            espm_score_mapping[row['Category']] = row
    espm_score_mapping = map_scores(data_dict['systemDefinedPropertyType'])
    site_max = float(espm_score_mapping['1']) * data_dict['site_total'] / float(espm_score_mapping[str(int(data_dict['energy_star_score']))])
            
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
    pc231 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = font_ll, fontName = font_bold, textColor = colors.white)
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
    
    pc251 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_t, textColor = CUSTOM_DGRAY, fontName = font_bold,  spaceBefore = 0)
    pc252 = ParagraphStyle('body_left', alignment = TA_RIGHT, fontSize = font_t, textColor = CUSTOM_DGRAY, fontName = font_bold,  spaceBefore = -12)
    pc253 = ParagraphStyle('body_left', alignment = TA_RIGHT, fontSize = font_t, textColor = CUSTOM_DGRAY, fontName = font_normal,  spaceBefore = 0)
    tct = []
    
    data_dict['siteEnergyUseFuelOil'] = data_dict['siteEnergyUseDiesel'] + data_dict['siteEnergyUseFuelOil1'] + data_dict['siteEnergyUseFuelOil2'] + data_dict['siteEnergyUseFuelOil4'] + data_dict['siteEnergyUseFuelOil5And6']
    data_dict['siteEnergyUsePropane'] += data_dict['siteEnergyUseKerosene']
    data_dict['energyCostFuelOil'] = data_dict['energyCostDiesel'] + data_dict['energyCostFuelOil1'] + data_dict['energyCostFuelOil2'] + data_dict['energyCostFuelOil4'] + data_dict['energyCostFuelOil5And6']
    data_dict['energyCostPropane'] += data_dict['energyCostKerosene']

    num_fuel = 0
    for num, fuel in enumerate(FUELS):
        if data_dict['energyCost'+fuel] != 0:
            data_dict['energyRate'+fuel] = data_dict['energyCost'+fuel]/data_dict['siteEnergyUse'+fuel]
            num_fuel+=1
    if data_dict['onSiteRenewableSystemGeneration'] != 0:
        num_fuel+=1
            
    for num, fuel in enumerate(FUELS):
        if data_dict['energyCost'+fuel] != 0:
            pc251.textColor = FUELCOLOR[num]
            if num_fuel > 3:
                tct.append([FUELIMAGESSMALL[num],  [Paragraph(FUELLABEL[num], pc251),Paragraph('$'+"{:,}".format(int(data_dict['energyCost'+fuel])), pc252), Paragraph("{:,}".format(int(data_dict['siteEnergyUse'+fuel])) + ' ' + FUELUNIT[num] + ' at {0:.2f}'.format(data_dict['energyRate'+fuel]) + ' $/'+FUELUNIT[num], pc253),], ''])
            else:
                tct.append([FUELIMAGES[num],  [Paragraph(FUELLABEL[num], pc251),Paragraph('$'+"{:,}".format(int(data_dict['energyCost'+fuel])), pc252), Paragraph("{:,}".format(int(data_dict['siteEnergyUse'+fuel])) + ' ' + FUELUNIT[num], pc253), Paragraph('{0:.2f}'.format(data_dict['energyRate'+fuel]) + ' $/'+FUELUNIT[num], pc253)], ''])

    if data_dict['onSiteRenewableSystemGeneration'] != 0:
        pc251.textColor = FUELCOLOR[-1]
        if num_fuel > 3:
            tct.append([FUELIMAGESSMALL[-1],[Paragraph("<font name='FontAwesome'>"+FUELICONS[-1]+"</font> Solar", pc251), Paragraph('$'+"{:,}".format(int(-1.0*data_dict['energyCostElectricityOnsiteSolarWind'])), pc252), Paragraph("{:,}".format(int(data_dict['onSiteRenewableSystemGeneration'])) + ' kwh', pc253)],''])
        else:
            tct.append([FUELIMAGES[-1],[Paragraph("<font name='FontAwesome'>"+FUELICONS[-1]+"</font> Solar", pc251), Paragraph('$'+"{:,}".format(int(-1.0*data_dict['energyCostElectricityOnsiteSolarWind'])), pc252), Paragraph("{:,}".format(int(data_dict['onSiteRenewableSystemGeneration'])) + ' kwh', pc253)],''])
        
    cost_subTable = Table(tct, colWidths = [0.5*inch, 1.83*inch, 0.2*inch, 2.0*inch])
    cost_subTableStyle = TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ])

    row_ind = 0
    for num, fuel in enumerate(FUELS):
        if data_dict['energyCost'+fuel]!= 0:
            cost_subTableStyle.add('BACKGROUND',(2,row_ind),(-1,-num_fuel+row_ind),FUELCOLOR[num])
            if num_fuel != 1:
                cost_subTableStyle.add('LINEBELOW', (0, row_ind), (-2, -num_fuel+row_ind), 1, CUSTOM_MGRAY),
            row_ind += 1
    if data_dict['onSiteRenewableSystemGeneration'] != 0:
        cost_subTableStyle.add('BACKGROUND',(2,num_fuel-1),(-1,-1),FUELCOLOR[-1])
        cost_subTableStyle.add('LINEABOVE', (0, row_ind),(-1, -num_fuel+row_ind),1, CUSTOM_MGRAY)
        
    cost_subTable.setStyle(cost_subTableStyle)    
     
    Story.append(cost_subTable)
    Story.append(FrameBreak)
    pie = pie_chart(data_dict)
    column_253 = Frame(doc.leftMargin+doc.width/3+(7/15)*doc.width, doc.height*(1-y_offset), (3/10)*(2/3)*doc.width, 0.20*doc.height, showBoundary=0, topPadding=10)        
    Story.append(pie)
    Story.append(FrameBreak)    
    
    
    # Energy Highlights Header
    y_offset += 0.03
    column_261 = ColorFrame(doc.leftMargin+doc.width/3, doc.height*(1-y_offset)+10, (1/4)*(2/3)*doc.width, 0.04*doc.height, showBoundary=0, roundedBackground=CUSTOM_DTEAL, topPadding=10)    
    pc261 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = font_t, fontName = font_bold, textColor = colors.white)
    text_c261 = Paragraph('Insights & Trends', pc261)
    Story.append(text_c261)
    Story.append(FrameBreak)

    
    # Energy Highlights Details
    y_offset += 0.17
    column_27 = Frame(doc.leftMargin+doc.width/3, doc.height*(1-y_offset), (2/3)*doc.width, 0.17*doc.height, showBoundary=0, topPadding=0)    
    Story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color= CUSTOM_MGRAY, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='TOP', dash=None))
    
    ## HIGHLIGHTS: CERTIFICATIONS, SOLAR & EV, GENERAL
    num_line = 0
    t_cert, num_line = Highlights.cert_commercial(data_dict, font_t, font_normal, CUSTOM_DGRAY, check_img, TA_LEFT, num_line)             
    if t_cert:
        ratings_table = Table(t_cert, colWidths = [2.7*inch, 2.7*inch])
        ratings_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('BACKGROUND',(0,0),(-1,-1),colors.white),
         ]))
        Story.append(ratings_table)   
        
    t_achieve, num_line = Highlights.solar_commercial(data_dict, font_t, font_normal, CUSTOM_DGRAY, check_img, TA_LEFT, num_line)
    if t_achieve:
        achieve_table = Table(t_achieve, colWidths = [5.1*inch])
        achieve_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BACKGROUND',(0,0),(-1,-1),colors.white),
         ]))
        Story.append(achieve_table)
    
    t_achieve, num_line = Highlights.general_commercial(data_dict, font_t, font_normal, CUSTOM_DGRAY, check_img, TA_LEFT, num_line)
    if t_achieve and num_line < 5:
        ratings_table = Table(t_achieve, colWidths = [5.4*inch])
        ratings_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('BACKGROUND',(0,0),(-1,-1),colors.white),
         ]))
        Story.append(ratings_table)      
    Story.append(FrameBreak)
    
        
    # Take Action Header
    y_offset += 0.0
    column_281 = ColorFrame(doc.leftMargin+doc.width/3, doc.bottomMargin+0.19*doc.height+10, (1/4)*(2/3)*doc.width, 0.04*doc.height, showBoundary=0, roundedBackground=CUSTOM_DTEAL, bottomPadding=10)    
    text_c281 = Paragraph('Take Action!', pc261)
    Story.append(text_c281)
    Story.append(FrameBreak)

    pc262 = ParagraphStyle('column_2', alignment = TA_LEFT, fontSize = font_t, fontName = font_bold, textColor = CUSTOM_DTEAL, spaceBefore = -12, spaceAfter = -12)
    
    column_282 = Frame(doc.leftMargin+doc.width/3+(1/4)*(2/3)*doc.width, doc.bottomMargin+0.19*doc.height, (3/4)*(2/3)*doc.width, 0.06*doc.height, showBoundary=0, topPadding=10)    
    text_c282 = Paragraph('The following actions can help you save money on your energy costs for years to come', pc262)
    Story.append(text_c282)
    Story.append(FrameBreak)
    
    # Take Action Details    
    column_29 = Frame(doc.leftMargin+doc.width/3, doc.bottomMargin, (2/3)*doc.width, 0.19*doc.height, showBoundary=0, topPadding=0)    
    Story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color= CUSTOM_MGRAY, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='TOP', dash=None))        
    pc291 = ParagraphStyle('body_left', alignment = TA_LEFT, textColor = CUSTOM_DGRAY, fontSize = font_t, fontName = font_normal,  spaceBefore = 6, spaceAfter = 0, leading=10, backColor = 'white', bulletIndent = 12, firstLineIndent = 0, leftIndent = 12, rightIndent = 0)

    Story.append(Paragraph('Schedule a Mass Save <font name="InterstateLight" color=blue><link href="https://www.masssave.com/en/business/programs-and-services/building-energy-assessments">Building Energy Assessment</link></font> to identify cost-saving upgrades.', pc291, bulletText=unchecked.encode('UTF8')))
    Story.append(Paragraph('Use Mass Save <font name="InterstateLight" color=blue><link href="https://www.masssave.com/business/rebates-and-incentives">rebates and incentives</link></font> for building insulation, HVAC systems, lighting controls, water heating, and more.', pc291, bulletText=unchecked.encode('UTF8')))
    Story.append(Paragraph('Take advantage of <font name="InterstateLight" color=blue><link href="https://www.whitehouse.gov/cleanenergy/clean-energy-tax-provisions/">federal tax credits or direct pay rebates</link></font> for energy upgrades.', pc291, bulletText=unchecked.encode('UTF8')))
    Story.append(Paragraph('Consult <font name="InterstateLight" color=blue><link href="https://www.dsireusa.org/">DSIRE</link></font> for all available incentives for renewables and energy efficiency.', pc291, bulletText=unchecked.encode('UTF8')))    
    Story.append(Paragraph('Take advantage of Mass Save <font name="InterstateLight" color=blue><link href="https://www.masssave.com/en/business/programs-and-services/building-energy-assessments">programs and technical support</link></font> to help save energy.', pc291, bulletText=unchecked.encode('UTF8')))
    Story.append(Paragraph('Install solar panels on the roof or over parking lots.', pc291, bulletText=unchecked.encode('UTF8')))
    Story.append(Paragraph('Finance energy improvements with the <font name="InterstateLight" color=blue><link href="https://www.massdevelopment.com/what-we-offer/key-initiatives/pace">Property Assessed Clean Energy (PACE)</link></font> Massachusetts program.', pc291, bulletText=unchecked.encode('UTF8')))
                        
### BUILD PAGE
    page_1_frames = [column_10, column_11, column_12, column_211, column_212, column_22, column_231, column_232, column_24, column_251, column_252, column_253, column_261, column_27, column_281, column_282, column_29]
    templates =[]
    templates.append(PageTemplate(frames=page_1_frames,id='firstPage'))
    doc.addPageTemplates(templates)
    style = styles["Normal"]

    #populate story with paragraphs    
    doc.build(Story)

# Run with:  python3 -m label.populate_beam_lexington
if __name__ == '__main__':
    data_dict = {
        'street': '77 MASSACHUSETTS AVE', 'city': 'CAMBRIGE', 'state': 'MA', 'zipcode': '02139', 
        'year_built': 1895, 'year_ending': 2022, 'propGrossFloorArea': 100000.0, 'systemDefinedPropertyType': 'Hotel', 'energy_star_score': 99, 'site_total': 3434,  'medianSiteIntensity': 2500, 'percentBetterThanSiteIntensityMedian': 0.25, 'cons_mmbtu_min': 0,
        'siteEnergyUseElectricityGridPurchase': 1000.0, 'siteEnergyUseElectricityGridPurchaseKwh': 100000.0, 'siteEnergyUseNaturalGas': 1000.0, 'siteEnergyUseKerosene': 0.0, 'siteEnergyUsePropane': 1000.0,
        'siteEnergyUseDiesel': 0.0, 'siteEnergyUseFuelOil1': 0.0, 'siteEnergyUseFuelOil2': 0.0, 'siteEnergyUseFuelOil4': 0.0, 'siteEnergyUseFuelOil5And6': 0.0, 'siteEnergyUseWood': 0.0,
        'energyCost': 10000.0, 
        'energyCostElectricityOnsiteSolarWind': 2110.0,
        'energyCostElectricityGridPurchase': 1000.0, 'energyCostNaturalGas': 1000.0, 'energyCostKerosene': 0.0, 'energyCostPropane': 1000.0,
        'energyCostDiesel': 0.0, 'energyCostFuelOil1': 0.0, 'energyCostFuelOil2': 0.0, 'energyCostFuelOil4': 0.0, 'energyCostFuelOil5And6': 0.0, 'energyCostWood': 0.0,
        'cons_solar': -11000.0,
        'estar_wh': True,
        'yoy_percent_change_site_eui_2022': 0.0, 'yoy_percent_change_elec_2022': -0.1,
        'onSiteRenewableSystemGeneration': 20000, 'numberOfLevelOneEvChargingStations': 3, 'numberOfLevelTwoEvChargingStations': 0, 'numberOfDcFastEvChargingStations': 0,
    }
    out_file = 'Lexington_BEAM_Profile.pdf'
    write_lexington_profile_pdf(data_dict, out_file)


