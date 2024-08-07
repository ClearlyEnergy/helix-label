# -*- coding: utf-8 -*-
#! /usr/bin/python
# run with python3 -m label.populate_vermont_energy_profile

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
from label.utils.utils import ColorFrame, ColorFrameSimpleDocTemplate
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
CUSTOM_DTEAL = colors.Color(red=(0.0/255),green=(77.0/255),blue=(113.0/255))
FUELS = ['elec', 'ng', 'ho', 'propane', 'wood_pellet', 'wood_cord']
#FUELICONS = [u"",u"\uf06d",u"\uf043",u"\uf043",u"\uf1bb",u"\uf1bb",u"\uf185"]
FUELICONS = [u"\uf0e7",u"\uf06d",u"\uf043",u"\uf043",u"\uf1bb",u"\uf1bb",u"\uf185"]
FUELIMAGES = [Image(IMG_PATH+"/HomeEnergyProfile_icons-03.png",0.4*inch,0.4*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-09.png",0.4*inch,0.4*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-10.png",0.4*inch,0.4*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-11.png",0.4*inch,0.4*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-02.png",0.4*inch,0.4*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-02.png",0.4*inch,0.4*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-04.png",0.4*inch,0.4*inch)]
FUELIMAGESSMALL = [Image(IMG_PATH+"/HomeEnergyProfile_icons-03.png",0.3*inch,0.3*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-09.png",0.3*inch,0.3*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-10.png",0.3*inch,0.3*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-11.png",0.3*inch,0.3*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-02.png",0.3*inch,0.3*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-02.png",0.3*inch,0.3*inch), Image(IMG_PATH+"/HomeEnergyProfile_icons-04.png",0.3*inch,0.3*inch)]
FUELLABEL = ['Electric', 'Natural Gas', 'Heating Oil', 'Propane', 'Wood-Pellet', 'Wood-Cord']
FUELUNIT = ['kwh', 'ccf', 'gal', 'gal', 'ton', 'cord']
FUELCOLOR = [CUSTOM_ELECGREEN, CUSTOM_ORANGE, CUSTOM_DTEAL, CUSTOM_LTEAL, CUSTOM_MGREEN, CUSTOM_MGREEN, CUSTOM_YELLOW]


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
    
#def add_legend(draw_obj, chart, data):
#    legend = Legend()
#    legend.alignment = 'right'
#    legend.x = 10
#    legend.y = 70
#    legend.colorNamePairs = Auto(obj=chart)
#    draw_obj.add(legend)

def pie_chart(data_dict):
    drawing = Drawing(width=1.0*inch, height=1.0*inch)
    data = []
    labels = []
    order = []

    for num, fuel in enumerate(FUELS):
        if data_dict[fuel+'_score'] > 0:
            data.append(int(data_dict[fuel+'_score']))
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

def write_vermont_energy_profile_pdf(data_dict, output_pdf_path):
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
    vthep_logo = IMG_PATH+"/HomeEnergyProfile_icons-01.png"
    im = Image(vthep_logo, 2.4*inch, 1.0*inch)
    Story.append(im)
    Story.append(FrameBreak)
    
    total_score = 0.0
    for fuel in ['ng','elec','ho','propane','wood_cord','wood_pellet']:
        total_score += data_dict[fuel+'_score']

    # Cost Box
    column_11 = ColorFrame(doc.leftMargin, doc.height-0.23*doc.height, doc.width/3-12, 0.13*doc.height, showBoundary=0, roundedBackground=CUSTOM_DTEAL, topPadding=10)    
    pc101 = ParagraphStyle('column_1', alignment = TA_CENTER, fontSize = font_h, fontName = font_bold, textColor=colors.white, leading=14)
    pc102 = ParagraphStyle('column_1', alignment = TA_CENTER, fontSize = font_xxl, fontName = font_bold, textColor = colors.white)
    pc103 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = font_s, fontName = font_bold, textColor = colors.white, spaceBefore=26)
    text_c101 = Paragraph("THIS HOME'S EXPECTED ANNUAL ENERGY COST*", pc101)
    text_c102 = Paragraph('$'+str(int(total_score)), pc102)
    text_c103 = Paragraph(data_dict['rating'], pc103)
    Story.append(text_c101)
    Story.append(text_c102)
    Story.append(text_c103)
    Story.append(FrameBreak)

    # Text Column
    column_12 = ColorFrame(doc.leftMargin, doc.bottomMargin, doc.width/3-12, 0.72*doc.height, showBoundary=0, roundedBackground=CUSTOM_LGRAY, topPadding=10)
    pc12 = ParagraphStyle('column_1', alignment = TA_LEFT, fontSize = font_ml, fontName = font_bold, textColor = CUSTOM_DTEAL, leading = 14, spaceBefore = 16)
    pc13 = ParagraphStyle('column_1', alignment = TA_LEFT, fontSize = font_h, fontName = font_bold, textColor = CUSTOM_DGRAY, leading = 12, spaceBefore = 4)
    pc14 = ParagraphStyle('column_1', alignment = TA_LEFT, fontSize = font_t, fontName = font_normal, textColor = CUSTOM_DGRAY, leading = 12)
    text_c11 = Paragraph("This profile details the estimated annual energy costs of this home and documents energy upgrades. Energy usage and costs are estimates only based on standardized assumptions for variable factors such as weather, occupancy, lights and appliance usage.", tf_standard)
    text_c12 = Paragraph("HOME INFORMATION", pc12)
    text_c13 = Paragraph("LOCATION:", pc13)
    text_c14 = Paragraph(data_dict['street'],pc14)
    text_c15 = Paragraph(data_dict['city'] + ", " + data_dict["state"] + " " + data_dict["zipcode"], pc14)
    text_c16 = Paragraph("YEAR BUILT:", pc13)
    text_c17 = Paragraph(str(int(data_dict['yearbuilt'])),pc14)
    text_c18 = Paragraph("CONDITIONED FLOOR AREA:",pc13)
    text_c19 = Paragraph(str(int(data_dict['finishedsqft']))+' Finished Square Feet',pc14)
    text_c110 = Paragraph("REPORT INFORMATION", pc12)
    text_c111 = Paragraph("PROFILE CREATION DATE:", pc13)
    text_c112 = Paragraph(datetime.datetime.now().strftime("%m/%d/%Y"),pc14)
    text_c114c = None
    if data_dict['third_party']:
        text_c113 = Paragraph("PROFILE GENERATED FOR:", pc13)
        text_c114 = Paragraph(data_dict['third_party'],pc14)
        if data_dict['author_company']:
            text_c114c = Paragraph('Profile created by: ' + data_dict['author_company'],pc14)
        else:
            text_c114c = Paragraph('Profile created by: ' + data_dict['author_name'],pc14)
    else:
        text_c113 = Paragraph("PROFILE GENERATED BY:", pc13)
        if data_dict['author_company']:
            text_c114 = Paragraph(data_dict['author_company'],pc14)
        else:
            text_c114 = Paragraph(data_dict['author_name'],pc14)

    if 'hers_score' in data_dict and data_dict['hers_score']:
        text_c114b = Paragraph('Source: RESNET HERS Rating', pc14)
    elif 'hes_score' in data_dict and data_dict['hes_score']:
        text_c114b = Paragraph('Source: Dept. of Energy Home Energy Score', pc14)
    else:
        text_c114b = None
    
    text_c115 = Paragraph("Brought to you by a collaboration of Vermont Residential Energy Labeling Stakeholders, HELIX and ClearlyEnergy", tf_small)
    text_c116 = Paragraph("*Annual energy costs include heating, cooling and electricity", tf_small)
    
    Story.append(text_c11)

    Story.append(Spacer(1,16))
    Story.append(HRFlowable(width="90%", thickness=1, lineCap='round', color=colors.white, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))
    Story.append(text_c12)
    Story.append(text_c13)
    Story.append(text_c14)
    Story.append(text_c15)
    Story.append(text_c16)
    Story.append(text_c17)
    Story.append(text_c18)
    Story.append(text_c19)
    Story.append(Spacer(1,16))
    Story.append(HRFlowable(width="90%", thickness=1, lineCap='round', color=colors.white, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))
    Story.append(text_c110)
    Story.append(text_c111)
    Story.append(text_c112)
    Story.append(text_c113)
    Story.append(text_c114)
    if text_c114b:
        Story.append(text_c114b)
    if text_c114c:
        Story.append(text_c114c)
    Story.append(Spacer(1,16))
    Story.append(HRFlowable(width="90%", thickness=1, lineCap='round', color=colors.white, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))
    Story.append(text_c115)
    Story.append(text_c116)
    Story.append(FrameBreak)
    # Column 2
    y_offset = 0.04
    # Expected Usage
    column_211 = ColorFrame(doc.leftMargin+doc.width/3, doc.height*(1-y_offset), (1/4)*(2/3)*doc.width, 0.04*doc.height, showBoundary=0, roundedBackground=CUSTOM_DTEAL, topPadding=5, bottomPadding = 5)    
    pc201 = ParagraphStyle('column_2', alignment = TA_CENTER, fontSize = font_ll, fontName = font_bold, textColor = colors.white)
    text_c201 = Paragraph(str(int(data_dict['cons_mmbtu']))+"<font size=10> MMBtu </font>", pc201)
    Story.append(text_c201)
    Story.append(FrameBreak)
    
    column_212 = Frame(doc.leftMargin+doc.width/3+(1/4)*(2/3)*doc.width, doc.height*(1-y_offset), (3/4)*(2/3)*doc.width, 0.04*doc.height, showBoundary=0, topPadding=10)    
    pc202 = ParagraphStyle('column_2', alignment = TA_LEFT, fontSize = font_l, fontName = font_bold, textColor = CUSTOM_DTEAL)
    text_c202 = Paragraph('Expected Annual Energy Usage', pc202)
    Story.append(text_c202)
    Story.append(FrameBreak)

    y_offset += 0.28
    column_22 = Frame(doc.leftMargin+doc.width/3, doc.height*(1-y_offset), (2/3)*doc.width, (y_offset-0.04)*doc.height, showBoundary=0, topPadding=10)    
    Story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color= CUSTOM_MGRAY, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='TOP', dash=None))
    text_c220 = Paragraph("The annual home energy use with 0 being a net zero home. The \"Highest Energy Use\" is determined from the home size and age assuming inefficient features", tf_standard)
    Story.append(text_c220)
    
    # Wedge - start at 0.62 end at 4.82
    wedge_img = IMG_PATH+"/wedge.png"
    wedge = Image(wedge_img, 5.0*inch, 2.25*inch)
    Story.append(wedge)
    triangle = IMG_PATH+"/triangle.png"
    offset_x = 0.53+data_dict['cons_mmbtu']/data_dict['cons_mmbtu_max']*(4.75-0.53)
    pic = flowable_triangle(triangle,offset_x, 1.78, 0.2, 0.288,'')
    Story.append(pic)
    txt = flowable_text(min(offset_x-0.5,4), 2.2, "This home's usage: " + str(int(data_dict['cons_mmbtu'])),9)
    Story.append(txt)
    triangle2 = IMG_PATH+"/triangle2.png"
    offset_x = 0.62 + 40.0/data_dict['cons_mmbtu_max']*(4.82-0.62)
    pic = flowable_triangle(triangle2,offset_x, 0.44,0.08, 0.138,"High Performance \n Home","left")
    Story.append(pic)
    triangle = IMG_PATH+"/triangle2.png"
    offset_x = 0.62 + data_dict['cons_mmbtu_avg']/data_dict['cons_mmbtu_max']*(4.82-0.62)
    if offset_x < 4.3:
        pic = flowable_triangle(triangle2,offset_x, 0.44,0.08, 0.138,"Avg. home \n built in " + str(int(data_dict['yearbuilt'])),"right")
        Story.append(pic)
    triangle2 = IMG_PATH+"/triangle2.png"
    offset_x = 0.62 + 105.0/data_dict['cons_mmbtu_max']*(4.82-0.62)
#    if offset_x < 4.2:
#        if (data_dict['cons_mmbtu_avg'] - 105.0)/data_dict['cons_mmbtu_max'] > 0.15 and (105.0 - 40.0)/data_dict['cons_mmbtu_max'] > 0.15:
#            pic = flowable_triangle(triangle2,offset_x, 0.44,0.08, 0.138,'Avg. home built to \n 2020 Energy Code', 'left')
#        else:
#            pic = flowable_triangle(triangle2,offset_x, 0.44,0.08, 0.138,'Avg. home built to 2020 Energy Code','high')
#        Story.append(pic)
    txt = flowable_text(4.82, 0.44, str(int(data_dict['cons_mmbtu_max'])),7)
    Story.append(txt)
    
    
    # Expected Cost
    y_offset += 0.02
    column_231 = ColorFrame(doc.leftMargin+doc.width/3, doc.height*(1-y_offset), (1/4)*(2/3)*doc.width, 0.04*doc.height, showBoundary=0, roundedBackground=CUSTOM_DTEAL, topPadding=5, bottomPadding=5)    
    text_c231 = Paragraph('$'+str(int(total_score)), pc201)
    Story.append(text_c231)
    Story.append(FrameBreak)
    
    column_232 = Frame(doc.leftMargin+doc.width/3+(1/4)*(2/3)*doc.width, doc.height*(1-y_offset), (3/4)*(2/3)*doc.width, 0.04*doc.height, showBoundary=0, topPadding=10)    
    text_c232 = Paragraph('Expected Annual Energy Costs', pc202)
    Story.append(text_c232)
    Story.append(FrameBreak)
    
    # Pie Chart
    y_offset +=0.09
    column_24 = Frame(doc.leftMargin+doc.width/3, doc.height*(1-y_offset), (2/3)*doc.width, 0.09*doc.height, showBoundary=0, topPadding=10)    
    Story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color= CUSTOM_MGRAY, spaceBefore=0, spaceAfter=0, hAlign='CENTER', vAlign='TOP', dash=None))
    if data_dict['bill']:
        if data_dict['certified_bill'] and 'hers_score' in data_dict and data_dict['hers_score']:
            text_c240 = Paragraph("The breakdown of fuel usage is calculated from a third-party certification of costs of " + data_dict['bill'], tf_standard)
        elif data_dict['certified_bill'] and 'hes_score' in data_dict and data_dict['hes_score']:
            text_c240 = Paragraph("The breakdown of fuel usage is calculated from a third-party certification of costs of " + data_dict['bill'], tf_standard)        
        else:
            text_c240 = Paragraph("Annual fuel usage and costs are calculated from homeowner provided bill data of " + data_dict['bill'] + ", adjusted for weather, settings and occupancy.", tf_standard)
    else:
        text_c240 = Paragraph("Estimate includes electricity and fuels used to heat your home for a year.", tf_standard)

    Story.append(text_c240)
    Story.append(FrameBreak)
    y_offset +=0.19
    column_251 = Frame(doc.leftMargin+doc.width/3, doc.height*(1-y_offset), (1/5)*(2/3)*doc.width, 0.20*doc.height, showBoundary=0, topPadding=0)    
    Story.append(FrameBreak)
    column_252 = Frame(doc.leftMargin+doc.width/3+(1/5)*(2/3)*doc.width, doc.height*(1-y_offset), (1/2)*(2/3)*doc.width, 0.20*doc.height, showBoundary=0, topPadding=0)    
    
    pc251 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_t, textColor = CUSTOM_DGRAY, fontName = font_bold,  spaceBefore = 0)
    pc252 = ParagraphStyle('body_left', alignment = TA_RIGHT, fontSize = font_t, textColor = CUSTOM_DGRAY, fontName = font_bold,  spaceBefore = -12)
    pc253 = ParagraphStyle('body_left', alignment = TA_RIGHT, fontSize = font_t, textColor = CUSTOM_DGRAY, fontName = font_normal,  spaceBefore = 0)
    tct1 = Paragraph("<font name='InterstateBlack'>The breakdown of energy usage is an estimate </font><font name='Helvetica'>based on the energy sources used in this home</font>", pc251) 
    tct = []
    if data_dict['has_solar']:
        if data_dict['solar_ownership'] == 'owned':
            data_dict['elec_score'] = data_dict['solar_score'] + data_dict['elec_score']
        else:
            data_dict['cons_elec'] = data_dict['cons_elec'] + data_dict['cons_solar']            
    
    num_fuel = 0
    for num, fuel in enumerate(FUELS):
        if data_dict[fuel+'_score'] != 0:
            num_fuel+=1
    if data_dict['has_solar'] and data_dict['solar_score'] != 0 and data_dict['solar_ownership'] == 'owned':
        num_fuel+=1
            
    for num, fuel in enumerate(FUELS):
        if data_dict[fuel+'_score'] != 0:
            pc251.textColor = FUELCOLOR[num]
            if num_fuel > 3:
                tct.append([FUELIMAGESSMALL[num],  [Paragraph(FUELLABEL[num], pc251),Paragraph('$'+"{:,}".format(int(data_dict[fuel+'_score'])), pc252), Paragraph("{:,}".format(int(data_dict['cons_'+fuel])) + ' ' + FUELUNIT[num] + ' at {0:.2f}'.format(float(data_dict['rate_'+fuel])) + ' $/'+FUELUNIT[num], pc253),], ''])
            else:
                tct.append([FUELIMAGES[num],  [Paragraph(FUELLABEL[num], pc251), Paragraph('$'+"{:,}".format(int(data_dict[fuel+'_score'])), pc252), Paragraph("{:,}".format(int(data_dict['cons_'+fuel])) + ' ' + FUELUNIT[num], pc253), Paragraph('{0:.2f}'.format(float(data_dict['rate_'+fuel])) + ' $/'+FUELUNIT[num], pc253)], ''])

    if data_dict['has_solar'] and data_dict['solar_score'] != 0 and data_dict['solar_ownership'] == 'owned':
        pc251.textColor = FUELCOLOR[-1]
        if num_fuel > 3:
            tct.append([FUELIMAGESSMALL[-1],[Paragraph("<font name='FontAwesome'>"+FUELICONS[-1]+"</font> Solar", pc251), Paragraph('$'+"{:,}".format(int(-1.0*data_dict['solar_score'])), pc252), Paragraph("{:,}".format(int(data_dict['cons_solar'])) + ' kwh', pc253)],''])
        else:
            tct.append([FUELIMAGES[-1],[Paragraph("<font name='FontAwesome'>"+FUELICONS[-1]+"</font> Solar", pc251), Paragraph('$'+"{:,}".format(int(-1.0*data_dict['solar_score'])), pc252), Paragraph("{:,}".format(int(data_dict['cons_solar'])) + ' kwh', pc253)],''])
        
    cost_subTable = Table(tct, colWidths = [0.5*inch, 1.83*inch, 0.2*inch, 2.0*inch])
    cost_subTableStyle = TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ])

    row_ind = 0
    for num, fuel in enumerate(FUELS):
        if data_dict[fuel+'_score']!= 0:
            cost_subTableStyle.add('BACKGROUND',(2,row_ind),(-1,-num_fuel+row_ind),FUELCOLOR[num])
            if num_fuel != 1:
                cost_subTableStyle.add('LINEBELOW', (0, row_ind), (-2, -num_fuel+row_ind), 1, CUSTOM_MGRAY),
            row_ind += 1
    if data_dict['has_solar'] and data_dict['solar_score'] != 0 and data_dict['solar_ownership'] == 'owned':
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
    text_c261 = Paragraph('Energy Highlights', pc261)
    Story.append(text_c261)
    Story.append(FrameBreak)
    
    column_262 = Frame(doc.leftMargin+doc.width/3+(1/4)*(2/3)*doc.width, doc.height*(1-y_offset), (3/4)*(2/3)*doc.width, 0.06*doc.height, showBoundary=0, topPadding=10)    
    pc262 = ParagraphStyle('column_2', alignment = TA_LEFT, fontSize = font_t, fontName = font_bold, textColor = CUSTOM_DTEAL, spaceBefore = -12, spaceAfter = -12)
    text_c262 = Paragraph('Completed actions, home energy certifications and improvement measures', pc262)
    Story.append(text_c262)
    Story.append(FrameBreak)
    
    # Energy Highlights Details
    y_offset += 0.17
    column_27 = Frame(doc.leftMargin+doc.width/3, doc.height*(1-y_offset), (2/3)*doc.width, 0.17*doc.height, showBoundary=0, topPadding=0)    
    Story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color= CUSTOM_MGRAY, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='TOP', dash=None))
    
    pc272 = ParagraphStyle('body_left', alignment = TA_LEFT, textColor = CUSTOM_DGRAY, fontSize = font_t, fontName = font_normal,  spaceBefore = -1, spaceAfter = 0, leading=10, backColor = 'white', bulletIndent = 12, firstLineIndent = 0, leftIndent = 12, rightIndent = 6)
    pc273 = ParagraphStyle('body_left', alignment = TA_LEFT, textColor = CUSTOM_DGRAY, fontSize = font_t, fontName = font_normal)
    
    ## CERTIFICATIONS
    num_line = 0
    t_cert = []
    if 'evt' in data_dict and data_dict['evt']:
        t_cert.append([Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> '''+data_dict['evt'], pc272)])
    if 'hers_score' in data_dict and data_dict['hers_score']:
        t_cert.append([Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> HERS Index Score: ''' + str(data_dict['hers_score']), pc272)])
    if 'hes_score' in data_dict and data_dict['hes_score']:
        t_cert.append([Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> Home Energy Score: ''' + str(data_dict['hes_score']) + '/10', pc272)])
    if 'phius' in data_dict and data_dict['phius']:
        t_cert.append([Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> Certified Passive House''', pc272)])
    if 'zerh' in data_dict and data_dict['zerh']:
        t_cert.append([Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> DOE Zero Energy Ready Home''', pc272)])
    if 'ngbs' in data_dict and data_dict['ngbs']:
        t_cert.append([Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> NGBS New Construction '''+data_dict['ngbs'], pc272)])
    if 'leed' in data_dict and data_dict['leed']:
        t_cert.append([Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> LEED for Homes '''+data_dict['leed'], pc272)])
    if 'estar_wh' in data_dict and data_dict['estar_wh']:
        t_cert.append([Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> EPA ENERGYSTAR® Home''', pc272)])
    if 'iap' in data_dict and data_dict['iap']:
        t_cert.append([Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> Indoor airPLUS''', pc272)])
        
    if len(t_cert) > 4:
        t_cert = [t_cert[0:2],t_cert[2:4], t_cert[4:]]    
        num_line += 3
    elif len(t_cert) > 2:
        t_cert = [t_cert[0:2], t_cert[2:]]
        num_line += 2
    elif len(t_cert) == 2:
        t_cert = [t_cert]
        num_line +=1 
    elif len(t_cert) == 1:
        t_cert.append(Paragraph("", pc272))
        t_cert = [t_cert]
        num_line += 1
    else:
        t_cert = None
             
    if t_cert:
        ratings_table = Table(t_cert, colWidths = [2.7*inch, 2.7*inch])
        ratings_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('BACKGROUND',(0,0),(-1,-1),colors.white),
         ]))
        Story.append(ratings_table)   
        
    ## SOLAR & WEATHERIZATION
    t_achieve = []
    if data_dict['has_solar'] and num_line < 4:
        if data_dict['solar_ownership'] == 'owned':
            t_achieve.append([Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> '''+"This home has " + str(data_dict['capacity']) + 'KW of owned solar photovoltaic on site', pc273)])
        elif data_dict['solar_ownership'] == 'third':
            t_achieve.append([Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> '''+"Home has " + str(data_dict['capacity']) + 'KW of leased solar photovoltaic estimated to generate ' + str(int(data_dict['cons_solar'])) + 'kWh/yr', pc273)]) 
        else:
            t_achieve.append([Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> '''+"This home has " + str(data_dict['capacity']) + 'KW of solar photovoltaic on site', pc273)])
        num_line +=1 
    if data_dict['water_solar'] and num_line < 4:
        t_achieve.append([Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> '''+"This home has solar hot water", pc273)])
        num_line +=1                 
    if data_dict['has_storage'] and num_line < 4:
        t_achieve.append([Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> '''+"This home has electric battery storage on site", pc273)])
        num_line +=1
    if data_dict['evcharger'] and num_line < 4:
        t_achieve.append([Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> '''+"This home has an electric vehicle charger", pc273)])
        num_line +=1         
    if 'weatherization' in data_dict and data_dict['weatherization'] and num_line < 4:
        num_line += 1
        if data_dict['weatherization'] == 'program':
            t_achieve.append([Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> Program-sponsored weatherization upgrades''', pc273)])
        elif data_dict['weatherization'] == 'contractor':
            t_achieve.append([Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> Professional weatherization upgrades''', pc273)])
        elif data_dict['weatherization'] == 'diy':
            t_achieve.append([Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> DIY weatherization upgrades''', pc273)])
    if t_achieve:
        achieve_table = Table(t_achieve, colWidths = [5.1*inch])
        achieve_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BACKGROUND',(0,0),(-1,-1),colors.white),
         ]))
        Story.append(achieve_table)

    ## ENERGY STAR APPLIANCES
    estarr = []
    num_estar = (data_dict['heater_estar'] + data_dict['water_estar'] + data_dict['ac_estar'] + data_dict['lighting_estar'] + data_dict['fridge_estar'] + data_dict['washer_estar'] + data_dict['dishwasher_estar'])
    if num_estar > 1:
        num_line += 1
        estarr.append(Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> ENERGYSTAR® Products''', pc272))
        estarr = [estarr]
    elif num_estar == 1:
        num_line += 1
        if data_dict['heater_estar'] and data_dict['heater_type'] == 'pump':
            estarr.append(Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> ENERGYSTAR® Heat Pump''', pc272))
        elif data_dict['water_estar'] and data_dict['water_type'] == 'heatpump':
            estarr.append(Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> ENERGYSTAR® Heat Pump Water Heater''', pc272))
        elif data_dict['heater_estar']:
            estarr.append(Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> ENERGYSTAR® Heating System''', pc272))
        elif data_dict['water_estar']: 
            estarr.append(Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> ENERGYSTAR® Water Heater''', pc272))
        elif data_dict['ac_estar']:
            estarr.append(Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> ENERGYSTAR® Air Conditioning''', pc272))
        elif data_dict['fridge_estar']:
            estarr.append(Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> ENERGYSTAR® Refrigerator''', pc272))
        elif data_dict['lighting_estar']:
            estarr.append(Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> ENERGYSTAR® Lighting''', pc272))
        elif data_dict['washer_estar']:
            estarr.append(Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> ENERGYSTAR® Clothes Washer''', pc272))
        elif data_dict['dishwasher_estar']:
            estarr.append(Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> ENERGYSTAR® Dishwasher''', pc272))
        estarr = [estarr]
    else:
        estarr = None
            
    if estarr is not None and num_line <= 4:
        estar_table = Table(estarr, colWidths = [5.4*inch])
        estar_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('BACKGROUND',(0,0),(-1,-1),colors.white),
         ]))   
        Story.append(estar_table)
    
    ## General comments
    t_achieve = []
    if data_dict['has_audit']:
        t_achieve.append([Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> Professional energy audit''', pc272)])
    else:
        t_achieve.append([Paragraph('''<img src="'''+check_img+'''" height="12" width="12"/> Generated a Vermont Home Energy Profile.''', pc272)])
    num_line += 1
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
    column_281 = ColorFrame(doc.leftMargin+doc.width/3, doc.bottomMargin+0.17*doc.height+10, (1/4)*(2/3)*doc.width, 0.04*doc.height, showBoundary=0, roundedBackground=CUSTOM_DTEAL, bottomPadding=10)    
    text_c281 = Paragraph('Take Action!', pc261)
    Story.append(text_c281)
    Story.append(FrameBreak)
    
    
#    pc262 = ParagraphStyle('column_2', alignment = TA_LEFT, fontSize = font_t, fontName = font_bold, textColor = CUSTOM_DTEAL, spaceBefore = -12, spaceAfter = -12)
    
    column_282 = Frame(doc.leftMargin+doc.width/3+(1/4)*(2/3)*doc.width, doc.bottomMargin+0.17*doc.height, (3/4)*(2/3)*doc.width, 0.06*doc.height, showBoundary=0, topPadding=10)    
    text_c282 = Paragraph('The following actions can help you save money on your energy costs for years to come', pc262)
    Story.append(text_c282)
    Story.append(FrameBreak)
    
    # Take Action Details    
    column_29 = Frame(doc.leftMargin+doc.width/3, doc.bottomMargin, (2/3)*doc.width, 0.17*doc.height, showBoundary=0, topPadding=0)    
    Story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color= CUSTOM_MGRAY, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='TOP', dash=None))        
    pc291 = ParagraphStyle('body_left', alignment = TA_LEFT, textColor = CUSTOM_DGRAY, fontSize = font_t, fontName = font_normal,  spaceBefore = 6, spaceAfter = 0, leading=10, backColor = 'white', bulletIndent = 12, firstLineIndent = 0, leftIndent = 12, rightIndent = 0)

    num_action = 0
    if data_dict['high_cost_action'] == 1:
        Story.append(Paragraph("Ensure attic, basement, band joists, walls are properly air sealed and insulated", pc291, bulletText=unchecked.encode('UTF8')))
        num_action += 1
    elif data_dict['high_cost_action'] == 2:
        Story.append(Paragraph("Consider investing in renewable energy to offset your home's electrical consumption", pc291, bulletText=unchecked.encode('UTF8')))
        num_action += 1
    elif data_dict['high_cost_action'] == 3:
        Story.append(Paragraph("Consider investing in heat pump technology or biomass heating", pc291, bulletText=unchecked.encode('UTF8')))
        num_action += 1

    if data_dict['low_cost_action'].find("1") != -1:
        num_action += 2
        Story.append(Paragraph("Schedule a professional energy assessment to identify cost-saving energy upgrades and financial incentives", pc291, bulletText=unchecked.encode('UTF8')))
    if data_dict['low_cost_action'].find("2") != -1:
        Story.append(Paragraph("Verify all appliances, lighting, mechanical equipment are ENERGY STAR® certified", pc291, bulletText=unchecked.encode('UTF8')))
        num_action += 1
    if data_dict['low_cost_action'].find("4") != -1:
        Story.append(Paragraph("If still using old thermostats, update to programmable or smart thermostats", pc291, bulletText=unchecked.encode('UTF8')))    
        num_action += 1
    if data_dict['low_cost_action'].find("3") != -1 or num_action < 7:
        Story.append(Paragraph("Schedule regular maintenance of heating/ac systems to optimize performance", pc291, bulletText=unchecked.encode('UTF8')))
        num_action += 1
        if num_action < 7:
            Story.append(Paragraph('Power down electronics completely to avoid “phantom electricity loads" or invest in an advanced power strip to do it for you', pc291, bulletText=unchecked.encode('UTF8')))
            num_action += 2
        if num_action < 7:
            Story.append(Paragraph("Remove dust behind and underneath the refrigerator at least once a year.  If you have a forced-air system, you can vacuum the vents and change air filters", pc291, bulletText=unchecked.encode('UTF8')))
            num_action += 2
                
    ### P2
    Story.append(NextPageTemplate('secondPage'))
    Story.append(FrameBreak)
    
    # Wedge and Table
    y_offset = 0.2
    p2_r1 = Frame(doc.leftMargin, doc.height*(1-y_offset), 0.3*doc.width, 0.2*doc.height, showBoundary=0, topPadding=10)
    Story.append(Paragraph('TOTAL ENERGY USE', pc202))
    Story.append(Spacer(1,12))
    p2_p1 = Paragraph('Below are features of homes with different levels of energy use to help guide your path to lower energy bills',tf_standard)
    Story.append(p2_p1)
    Story.append(FrameBreak)
    p2_r1b = Frame(doc.leftMargin+0.3*doc.width, doc.height*(1-y_offset), 0.70*doc.width, 0.2*doc.height, showBoundary=0, topPadding=10)
    pic = flowable_triangle(IMG_PATH+"/wedge3.png",0.12, -1.92, 2.1, 5.35,'')
    Story.append(pic)
    Story.append(FrameBreak)
    
    y_offset = 0.45
    p2_r2 = Frame(doc.leftMargin, doc.height*(1-y_offset), doc.width, 0.26*doc.height, showBoundary=0, topPadding=10)
    features_table_style = TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), 
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), 
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (1,0), (-1,-1), 0.1, CUSTOM_DGRAY),
        ('LINEABOVE', (0,0), (-5,-1), 0.1, CUSTOM_DGRAY),
        ('FONTSIZE', (0,0), (-1,-1), 7),
        ('BOX', (0,0), (-1,-1), 1, CUSTOM_DGRAY)
    ])

    p2_r10 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_s, fontName = font_bold, textColor = CUSTOM_DTEAL)
    p2_r11 = ParagraphStyle('body_left', alignment = TA_CENTER, fontSize = font_s, fontName = font_normal, textColor = CUSTOM_DGRAY)    
    p2_r12 = ParagraphStyle('body_left', alignment = TA_CENTER, fontSize = font_s, fontName = font_normal, textColor = CUSTOM_DGRAY, spaceBefore = 50)    
    
    features_table = Table([
        [Image(IMG_PATH+"/HomeEnergyProfile_icons-05.png", 0.05*doc.width,0.05*doc.width), Paragraph('INSULATION & AIR LEAKAGE',p2_r10),Paragraph('All cavities filled plus insulation covering framing, air sealing',p2_r11),Paragraph('Vermont energy code standards',p2_r12),Paragraph('Little to none',p2_r11)],
        [Image(IMG_PATH+"/HomeEnergyProfile_icons-06.png", 0.05*doc.width,0.05*doc.width), Paragraph('HEATING & COOLING SYSTEMS',p2_r10),Paragraph('ENERGY STAR Certified or better',p2_r11),Paragraph('Federal minimum standard efficiency',p2_r12),Paragraph('15+ years old, no annual maintenance',p2_r11)],
        [Image(IMG_PATH+"/HomeEnergyProfile_icons-07.png", 0.05*doc.width,0.05*doc.width), Paragraph('LIGHTS & APPLIANCES',p2_r10),Paragraph('ENERGY STAR Certified or better',p2_r11),Paragraph('Mix of ENERGY STAR and conventional lights and appliances',p2_r12),Paragraph('Incandescent bulbs, conventional appliances',p2_r11)],
        [Image(IMG_PATH+"/HomeEnergyProfile_icons-08.png", 0.05*doc.width,0.05*doc.width), Paragraph('RENEWABLE ENERGY',p2_r10),Paragraph('Sized to off-set all or most consumption',p2_r11),Paragraph('Some/None',p2_r12),Paragraph('None',p2_r11)],
    ], colWidths = [0.05*doc.width, 0.275*doc.width, 0.245*doc.width, 0.198*doc.width, 0.232*doc.width])
    features_table.setStyle(features_table_style)
    Story.append(features_table)
    Story.append(FrameBreak)
    
    y_offset = 0.80
    p2_r21 = ColorFrame(doc.leftMargin, doc.height*(1-y_offset), (1/3)*doc.width-12, 0.38*doc.height, showBoundary=0, roundedBackground=CUSTOM_LGRAY, topPadding=10)    
    pc_21 = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = font_h, fontName = font_bold, textColor = CUSTOM_DTEAL, leading = 14)  
    Story.append(Paragraph('Expected Annual Energy Use',pc_21))
    Story.append(Paragraph('All sources of energy used in this home (electricity plus oil, gas, propane and/or wood) are converted to a common unit called MMBtu: one million British Thermal Units. A low MMBtu identifies a home as energy efficient with lower energy costs and a smaller carbon footprint.', tf_standard))
#    Story.append(Spacer(1,12))
    Story.append(Paragraph("1 MMBtu = ",tf_standard))
    Story.append(Paragraph("7 gal fuel oil",tf_standard,bulletText=u'\u2022'))
    Story.append(Paragraph("710 therms of natural gas",tf_standard,bulletText=u'\u2022'))
    Story.append(Paragraph("11 gal of propane",tf_standard,bulletText=u'\u2022'))
    Story.append(Paragraph("293 kWh of electricity",tf_standard,bulletText=u'\u2022'))
    Story.append(Paragraph(".05 cords of wood",tf_standard,bulletText=u'\u2022'))
    Story.append(Paragraph("Average VT home referenced on pg. 1 is based on regional data from U.S. DOE", tf_standard))
    Story.append(FrameBreak)    
    
    p2_r22 = Frame(doc.leftMargin + (1/3)*doc.width, doc.height*(1-y_offset), (2/3)*doc.width, 0.38*doc.height, showBoundary=0, topPadding=0)    
    Story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color= CUSTOM_MGRAY, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='TOP', dash=None))
    Story.append(Spacer(1,12))
    Story.append(Paragraph('Additional Resources',pc_21))
    pc_22 = ParagraphStyle('standard', alignment = TA_LEFT, fontSize = font_h, fontName = font_normal, textColor = CUSTOM_DGRAY, leading = 20)  
    Story.append(Paragraph('<font name="InterstateBlack">Burlington Electric Department:</font> <link href="http://www.burlingtonelectric.com/">www.burlingtonelectric.com</link>', pc_22))
    Story.append(Paragraph('<font name="InterstateBlack">Drive Electric Vermont:</font> <a href="https://www.driveelectricvt.com/">www.driveelectricvt.com</a>', pc_22))
    Story.append(Paragraph('<font name="InterstateBlack">Efficiency Vermont:</font> <a href="https://www.efficiencyvermont.com/">www.efficiencyvermont.com</a>', pc_22))
    Story.append(Paragraph('<font name="InterstateBlack">Go! Vermont:</font> <a href="https://www.connectingcommuters.org/">www.connectingcommuters.org</a>', pc_22))
    Story.append(Paragraph('<font name="InterstateBlack">Renewable Energy Vermont:</font> <a href="https://www.revermont.org/">www.revermont.org</a>', pc_22))
    Story.append(Paragraph('<font name="InterstateBlack">Vermont Energy Saver:</font> <a href="https://energysaver.vermont.gov/">www.energysaver.vermont.gov</a>', pc_22))
    Story.append(Paragraph('<font name="InterstateBlack">Vermont Gas Systems</font> <a href="https://www.vermontgas.com/">www.vermontgas.com</a>', pc_22))
    Story.append(Paragraph('<font name="InterstateBlack">Vermont Weatherization Program</font> <a href="https://dcf.vermont.gov/benefits/weatherization">dcf.vermont.gov/benefits/weatherization</a>', pc_22))
    Story.append(Paragraph('<font name="InterstateBlack">Vermont Energy Code</font> <a href="https://publicservice.vermont.gov/energy_efficiency/rbes">publicservice.vermont.gov/energy_efficiency/rbes</a>', pc_22))
    Story.append(FrameBreak)
        
    p2_r3 = Frame(doc.leftMargin, doc.bottomMargin, doc.width, 0.18*doc.height, showBoundary=0, topPadding=10)
#    Story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color= CUSTOM_MGRAY, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='TOP', dash=None))
#    Story.append(Paragraph("For questions about this profile, <font name='InterstateBlack'>contact Efficiency Vermont at 888-921-5990 or info@efficiencyvermont.com</font>",  tf_standard))
    Story.append(Paragraph('Home Energy Labeling eXchange (HELIX) Energy Estimate', tf_small_bold))
    month = datetime.datetime.now().strftime('%B %Y')
    Story.append(Paragraph('HELIX, sponsored by the Northeast Energy Efficiency Partnership, hosts third-party certified home energy data to be used by realtors and lenders to properly value energy efficiency. www.neep.org/home-energy-labeling-information-exchange-helix. Clearly Energy generates energy estimates based on homeowner inputs and publicly-available data (home age, size, heating system type and fuel) or an energy model from a professional who has visited the home. Standard assumptions are used for variable factors such as weather and occupancy. Average fuel prices are obtained from the U.S. Energy Information Administration and the VT Public Service Dept. Historic fuel bills can inform costs but are specific to prior occupancy and weather',tf_small_squished))
    Story.append(Paragraph('Version: ' + month, tf_small_right))

### Optional Page 3
    if data_dict['comments']:
        ### P3
        Story.append(NextPageTemplate('thirdPage'))
        Story.append(FrameBreak)
        p3_c11 = Frame(doc.leftMargin, doc.height*(0.9), doc.width/3-12, 0.13*doc.height, showBoundary=0)
        Story.append(im)
        Story.append(FrameBreak)
        p3_c12 = ColorFrame(doc.leftMargin, doc.height-0.23*doc.height, doc.width/3-12, 0.13*doc.height, showBoundary=0, roundedBackground=CUSTOM_DTEAL, topPadding=10)    
        Story.append(text_c101)
        Story.append(text_c102)
        Story.append(text_c103)
        Story.append(FrameBreak)
        # Text Column
        p3_c13 = ColorFrame(doc.leftMargin, doc.bottomMargin, doc.width/3-12, 0.72*doc.height, showBoundary=0, roundedBackground=CUSTOM_LGRAY, topPadding=10)
        Story.append(text_c11)
        Story.append(Spacer(1,16))
        Story.append(HRFlowable(width="90%", thickness=1, lineCap='round', color=colors.white, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))
        Story.append(text_c12)
        Story.append(text_c13)
        Story.append(text_c14)
        Story.append(text_c15)
        Story.append(text_c16)
        Story.append(text_c17)
        Story.append(text_c18)
        Story.append(text_c19)
        Story.append(Spacer(1,16))
        Story.append(HRFlowable(width="90%", thickness=1, lineCap='round', color=colors.white, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))
        Story.append(text_c110)
        Story.append(text_c111)
        Story.append(text_c112)
        Story.append(text_c113)
        Story.append(text_c114)
        if text_c114b:
            Story.append(text_c114b)
        if text_c114c:
            Story.append(text_c114c)
        Story.append(Spacer(1,16))
        Story.append(HRFlowable(width="90%", thickness=1, lineCap='round', color=colors.white, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM', dash=None))
        Story.append(text_c115)
        Story.append(text_c116)
        Story.append(FrameBreak)
        # Column 2
        p3_c21 = Frame(doc.leftMargin+doc.width/3, doc.height*0.96, (2/3)*doc.width, 0.04*doc.height, showBoundary=0, topPadding=10)    
        text_p31 = Paragraph("COMMENTS:", pc13)
        Story.append(text_p31)
        Story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color= CUSTOM_MGRAY, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='TOP', dash=None))
        Story.append(FrameBreak)
        p3_c22 = Frame(doc.leftMargin+doc.width/3, doc.height*0.03, (2/3)*doc.width, 0.93*doc.height, showBoundary=0, topPadding=10)
        text_p32 = Paragraph(data_dict["comments"], tf_standard)
        Story.append(text_p32)
        Story.append(FrameBreak)
        
### BUILD PAGE
    page_1_frames = [column_10, column_11, column_12, column_211, column_212, column_22, column_231, column_232, column_24, column_251, column_252, column_253, column_261, column_262, column_27, column_281, column_282, column_29]
    page_2_frames = [p2_r1, p2_r1b, p2_r2, p2_r21, p2_r22, p2_r3]
    templates =[]
    templates.append(PageTemplate(frames=page_1_frames,id='firstPage'))
    templates.append(PageTemplate(frames=page_2_frames,id='secondPage'))
    if data_dict['comments']:
        page_3_frames = [p3_c11, p3_c12, p3_c13, p3_c21, p3_c22]
        templates.append(PageTemplate(frames=page_3_frames,id='thirdPage'))
    doc.addPageTemplates(templates)
    style = styles["Normal"]

    #populate story with paragraphs    
    doc.build(Story)

# Run with:  python3 -m label.populate_vermont_energy_profile
if __name__ == '__main__':
#    data_dict = {
#        'street': '18 BAILEY AVE', 'city': 'MONTPELIER', 'state': 'VT', 'zipcode': '05602', 
#        'yearbuilt': 1895, 'finishedsqft': 3704.0, 'score': 60, 'cons_mmbtu': 3, 'cons_mmbtu_avg': 120, 'cons_mmbtu_max':160, 'cons_mmbtu_min': 0,
#        'heatingfuel': 'Electric', 'ng_score': 0.0, 'elec_score': 60.0, 'ho_score': 0.0, 'propane_score': 00.0, 'wood_cord_score': 0.0, 'wood_pellet_score': 0, 'solar_score': 2110.0,
#        'cons_elec': 12129.0, 'cons_ng': 0.0, 'cons_ho': 0.0, 'cons_propane': 0.0, 'cons_wood_cord': 0.0, 'cons_wood_pellet': 0.0, 'cons_solar': -11000.0,
#        'rate_ho': 2.807, 'rate_propane': 3.39, 'rate_ng': 1.412, 'rate_elec': 0.175096666666667, 'rate_wood_cord': 199.0, 'rate_wood_pellet': 0.1,
#        'evt': None, 'leed': None, 'ngbs': None, 'hers_score': None, 'hes_score': None, 'estar_wh': False, 'iap': False, 'zerh': False, 'phius': False,
#        'high_cost_action': 2, 'low_cost_action': "1234",   
#        'heater_estar': False, 'water_estar': False, 'water_solar': True, 'ac_estar': False, 'fridge_estar': False, 'lighting_estar': False, 
#        'washer_estar': False, 'dishwasher_estar': False, 'evcharger': True, 
#        'heater_type': 'pump', 'water_type': 'heatpump', 
#        'has_audit': False, 'auditor': 'Joe', 'third_party': None, 'author_name': 'John Doe', 'author_company': 'Audit Corp 1',
#        'has_solar': True, 'capacity': 4.0, 'solar_ownership': 'owned','has_storage': False, 'rating': 'Homeowner Verified', 'weatherization': 'diy', 'bill': '3000ccf, 15000kwh, 1500gal', 'certified_bill': False, 
#        'comments': ''
#    }

#    data_dict = {"street":"19 HUBBARD PARK DR","postal_code":"05602","property_uid":"082-019000","author_name":"Veronique Bugnion","cons_elec":9592.2,"lighting_estar":4,"author_company":"ClearlyEnergy","organization_name":"Vermont Department of Public Service","dataset_name":"Vermont Profile","city":"MONTPELIER","state":"VT","zipcode":"05602",
#                 "yearbuilt":1962,"finishedsqft":2348.0,"heatingfuel":"ho","score":3880.0,"elec_score":1600,"ng_score":0,"ho_score":2270,"propane_score":0,"wood_cord_score":0,"wood_pellet_score":0,"solar_score":0.0,"cons_mmbtu":98.94315515261115,"cons_mmbtu_max":325.8,"cons_mmbtu_min":68.8,"cons_mmbtu_avg":138.2,"cons_ho":501.98768197088464,
#                 "cons_propane":0.0,"cons_ng":0.0,"cons_wood_cord":0.0,"cons_wood_pellet":0.0,"cons_solar":0.0,"rate_elec":0.184797142857143,"rate_ng":1.401,"rate_ho":4.53,"rate_propane":3.45,"rate_wood_cord":227.0,"rate_wood_pellet":285.0,"evt":None,"leed":None,"ngbs":None,"hers_score":None,"hes_score":None,"estar_wh":None,"zerh":None,"phius":None,"iap":None,"heater_estar":False,"water_estar":False,"water_solar":False,"ac_estar":False,"fridge_estar":False,"washer_estar":False,"dishwasher_estar":True,"heater_type":"standard","water_type":"tank","has_audit":False,"auditor":"","has_solar":False,"solar_ownership":"","capacity":5.0,"has_storage":False,"rating":"Professionally Verified","source":"Program Verifier","weatherization":"contractor","evcharger":False,"has_cert":None,"high_cost_action":2,"low_cost_action": "3561","certified_bill":False,"bill":"$3850","opt_out":False,"third_party":"","comments":""}

#    data_dict = {"street":"56 LIBERTY ST","postal_code":"05602","property_uid":"090-056000","author_name":"Veronique Bugnion","cons_elec":5741.0,"lighting_estar":4,"author_company":"ClearlyEnergy","organization_name":"Vermont Department of Public Service","dataset_name":"Vermont Profile","city":"MONTPELIER","state":"VT","zipcode":"05602","yearbuilt":1890,"finishedsqft":1690.0,"heatingfuel":"ho","score":4780.0,"elec_score":1060,"ng_score":0,"ho_score":3720,"propane_score":0,"wood_cord_score":0,"wood_pellet_score":0,"solar_score":0.0,"cons_mmbtu":132.9,"cons_mmbtu_max":427.5,"cons_mmbtu_min":79.3,"cons_mmbtu_avg":159.2,"cons_ho":820.0,"cons_propane":0.0,"cons_ng":0.0,"cons_wood_cord":0.0,"cons_wood_pellet":0.0,"cons_solar":0.0,"rate_elec":"0.184797142857143","rate_ng":1.401,"rate_ho":4.53,"rate_propane":3.45,"rate_wood_cord":227.0,"rate_wood_pellet":285.0,"evt":None,"leed":None,"ngbs":None,"hers_score":None,"hes_score":None,"estar_wh":None,"zerh":None,"phius":None,"iap":None,"heater_estar":False,"water_estar":False,"water_solar":False,"ac_estar":False,"fridge_estar":False,"washer_estar":False,"dishwasher_estar":False,"heater_type":"furnace","water_type":"tank","has_audit":None,"auditor":None,"has_solar":False,"solar_ownership":None,"capacity":0.0,"has_storage":False,"rating":"Professionally Verified","source":"Program Verifier","weatherization":None,"evcharger":False,"has_cert":None,"high_cost_action":1,"low_cost_action":"3561","certified_bill":False,"bill":"","opt_out":False,"third_party":"","comments":""}
    data_dict = {"street":"56 LIBERTY ST","postal_code":"05602","property_uid":"090-056000","author_name":"Veronique Bugnion","cons_elec":3145.7677053824364,"lighting_estar":4,"author_company":"ClearlyEnergy","organization_name":"Vermont Department of Public Service","dataset_name":"Vermont Profile","city":"MONTPELIER","state":"VT","zipcode":"05602","yearbuilt":1890,"finishedsqft":1690.0,"heatingfuel":"ho","score":2870.0,"elec_score":580,"ng_score":0,"ho_score":2200,"propane_score":80,"wood_cord_score":0,"wood_pellet_score":0,"solar_score":0.0,"cons_mmbtu":80.0962793404661,"cons_mmbtu_max":470.2,"cons_mmbtu_min":86.1,"cons_mmbtu_avg":173.2,"cons_ho":485.995079086116,"cons_propane":24.0,"cons_ng":0.0,"cons_wood_cord":0.0,"cons_wood_pellet":0.0,"cons_solar":0.0,"rate_elec":"0.184797142857143","rate_ng":1.401,"rate_ho":4.53,"rate_propane":3.45,"rate_wood_cord":227.0,"rate_wood_pellet":285.0,"evt":None,"leed":None,"ngbs":None,"hers_score":None,"hes_score":None,"estar_wh":None,"zerh":None,"phius":None,"iap":None,"heater_estar":False,"water_estar":True,"water_solar":False,"ac_estar":False,"fridge_estar":False,"washer_estar":True,"dishwasher_estar":True,"heater_type":"standard","water_type":"tank","has_audit":False,"auditor":"","has_solar":False,"solar_ownership":None,"capacity":5.0,"has_storage":False,"rating":"Professionally Verified","source":"Program Verifier","weatherization":"program","evcharger":False,"has_cert":None,"high_cost_action":2,"low_cost_action":"3561","certified_bill":False,"bill":"$2809","opt_out":False,"third_party":"","comments":""}
    out_file = 'VTLabel.pdf'
    write_vermont_energy_profile_pdf(data_dict, out_file)

