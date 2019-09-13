# -*- coding: utf-8 -*-
#! /usr/bin/python
# run with python label/populate_vermont_energy_profile.py

#import time
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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, Flowable, PageBreak
import pkg_resources
import datetime


#Adding Arial Unicode for checkboxes
FONT_PATH = pkg_resources.resource_filename('label', '.fonts/')

pdfmetrics.registerFont(TTFont('Inter',FONT_PATH+'Inter-Regular.ttf'))
pdfmetrics.registerFont(TTFont('InterBold',FONT_PATH+'Inter-Bold.ttf'))
pdfmetrics.registerFont(TTFont('InterItalic',FONT_PATH+'Inter-Italic.ttf'))
pdfmetrics.registerFont(TTFont('InterThin',FONT_PATH+'Inter-Thin-BETA.ttf'))
#pdfmetrics.registerFont(TTFont('Arial Unicode',FONT_PATH+'Arial Unicode.ttf'))
pdfmetrics.registerFont(TTFont("FontAwesome", FONT_PATH+"FontAwesome.ttf"))

IMG_PATH = pkg_resources.resource_filename('label', 'images/')
CUSTOM_LGREEN = colors.Color(red=(209.0/255),green=(229.0/255),blue=(202.0/255))
CUSTOM_DGREEN = colors.Color(red=(65.0/255),green=(173.0/255),blue=(73.0/255))
CUSTOM_MGREEN = colors.Color(red=(146.0/255),green=(200.0/255),blue=(74.0/255))
CUSTOM_LORANGE = colors.Color(red=(242.0/255),green=(151.0/255),blue=(152.0/255))
CUSTOM_YELLOW = colors.Color(red=(254.0/255),green=(230.0/255),blue=(153.0/255))
FUELS = ['elec', 'ng', 'ho', 'propane', 'wood_pellet', 'wood_cord']
FUELICONS = [u"\uf0e7",u"\uf06d",u"\uf043",u"\uf043",u"\uf1bb",u"\uf1bb",u"\uf185"]
FUELLABEL = ['Electric', 'Natural Gas', 'Heating Oil', 'Propane', 'Wood Pellet', 'Wood Cord']
FUELUNIT = ['kwh', 'ccf', 'gal', 'gal', 'cord', 'lb']
COLORLIST = [CUSTOM_LGREEN, CUSTOM_DGREEN, CUSTOM_MGREEN]

class flowable_triangle(Flowable):
    def __init__(self, imgdata, offset_x, offset_y, height, width, text):
        Flowable.__init__(self)
        self.img = ImageReader(imgdata)
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.height = height
        self.width = width
        self.text = text

    def draw(self):
        self.canv.drawImage(self.img, self.offset_x*inch, self.offset_y*inch, height = self.height*inch, width=self.width*inch)
        self.canv.setFont("Inter", 7)
        self.canv.setFillColor(colors.gray)
        self.canv.drawString(self.offset_x*inch, (self.offset_y-0.1)*inch, self.text)
        self.canv.setFont("FontAwesome", 30)
        icon = u"\uf1e3" # fa-futbol-o
        icon = u"\uf06d" #fire
        self.canv.drawString(self.offset_x*inch, (self.offset_y-0.1)*inch,icon)
        
    
def myFirstPage(canvas, doc):  
    canvas.saveState()  
    canvas.setFillColor(CUSTOM_LGREEN)
    canvas.rect(20,20,570,750,fill=1,stroke=0)
    canvas.restoreState()  
    
def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.white)
    canvas.rect(20,20,570,750,fill=1,stroke=0)
    canvas.restoreState()

#def add_legend(draw_obj, chart, data):
#    legend = Legend()
#    legend.alignment = 'right'
#    legend.x = 10
#    legend.y = 70
#    legend.colorNamePairs = Auto(obj=chart)
#    draw_obj.add(legend)

def pie_chart(data_dict):
    drawing = Drawing(width=1.25*inch, height=1.25*inch)
    data = []
    labels = []
        
    for num, fuel in enumerate(FUELS):
        if data_dict[fuel+'_score'] > 0:
            data.append(int(data_dict[fuel+'_score']))
#            txt += FUELLABEL[num]
            labels.append(FUELICONS[num])
    pie = Pie()
    pie.sideLabels = False
    pie.x = 10
    pie.y = -10
    pie.data = data
    pie.labels = labels
    pie.slices.strokeColor = colors.white
    pie.slices.strokeWidth = 0.25
    pie.simpleLabels = 0
    for i in range(len(data)):
        pie.slices[i].labelRadius = 0.5
        pie.slices[i].fillColor = COLORLIST[i]
        pie.slices[i].fontName = 'FontAwesome'
        pie.slices[i].fontSize = 16
    drawing.add(pie)
    return drawing

def write_vermont_energy_profile_pdf(data_dict, output_pdf_path):
    doc = SimpleDocTemplate(output_pdf_path,pagesize=letter,
                            rightMargin=20,leftMargin=20,
                            topMargin=20,bottomMargin=20)
                            
    font_xxl = 28
    font_xl = 24
    font_ll = 16
    font_l = 14
    font_h = 10
    font_t = 9
    font_s = 8
    font_normal = 'Inter'
    font_bold = 'InterBold'
    font_italic = 'InterItalic'
    checked = u"\u2713"
    unchecked = u"\u2752"
    leq = u"\u2264"
    geq = u"\u2265"
    registered = u"\u00AE"
    space = u"\u0009"
    
    colors_lgreen = ''

    Story=[]
    Story.append(Spacer(1, 12))
    
    ### HEADER
    vthep_logo = IMG_PATH+"VHESLogoV4.jpg"
    im = Image(vthep_logo, 1.63*inch, 1.65*inch)
    
    wedge = IMG_PATH+"wedge.png"
    im2 = Image(wedge, 3.67*inch, 1.65*inch)

    styles = getSampleStyleSheet()
    p1_1 = ParagraphStyle('headers', alignment = TA_LEFT, fontSize = font_l, fontName = font_normal, textColor=colors.white)
    p1_2 = ParagraphStyle('headers', alignment = TA_LEFT, fontSize = font_xxl, fontName = font_bold, textColor=colors.white)
    p1_5 = ParagraphStyle('headers', alignment = TA_LEFT, fontSize = font_h, fontName = font_italic, textColor=colors.red, spaceBefore=30)
    p1_3 = ParagraphStyle('headers', alignment = TA_LEFT, fontSize = font_s, fontName = font_bold, textColor=colors.black, leading = 117, spaceBefore=-117, leftIndent=135)
    p1_4 = ParagraphStyle('headers', alignment = TA_LEFT, fontSize = font_s, fontName = font_bold, textColor=colors.lightgrey, leading = 20, spaceBefore=-20, leftIndent=235)

    text_cost_1 = Paragraph("THIS HOME'S ANNUAL EXPECTED ENERGY COST", p1_1)
    text_cost_2 = Paragraph('$'+"{:,}".format(int(data_dict['score'])), p1_2)
    text_cost_3 = Paragraph('*Third-Party Verified', p1_5)

    text_use_1 = Paragraph(str(int(data_dict['cons_mmbtu']))+' MMBtu', p1_3)
    text_use_2 = Paragraph(str(int(data_dict['cons_mmbtu_max'])), p1_4)

    header_table = Table([['','','','',''],['', im, '',[text_cost_1, text_cost_2, text_cost_3], [im2, text_use_1, text_use_2], ''],['','','','','']],
        colWidths=[0.3*inch, 1.63 * inch, 0.1*inch, 1.93 * inch, 3.67 * inch,0.1*inch],
        rowHeights=[0.1*inch, 1.65 * inch, 0.1*inch], spaceBefore=0, spaceAfter=20)
    header_table.setStyle(TableStyle([
        ('BACKGROUND',(3,1),(3,1),colors.HexColor('#f3901d')), #orange background 2nd box
        ('BACKGROUND',(0,0),(5,0),colors.white), #top row
        ('BACKGROUND',(0,2),(5,2),colors.white), #bottom row
        ('BACKGROUND',(0,0),(0,2),colors.white), #left column
        ('BACKGROUND',(5,0),(5,2),colors.white), #right column
        ('BACKGROUND',(2,0),(2,2),colors.white), #middle column
        ('TEXTCOLOR',(1,0),(-1,0),colors.white), 
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), 
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE') 
        ]))
    Story.append(header_table)
    # add moving triangles, start reference 4.29, end reference 7.42
    triangle = IMG_PATH+"triangle.png"
    offset_x = 4.35 + data_dict['cons_mmbtu']/data_dict['cons_mmbtu_max']*(7.45-4.35)
    pic = flowable_triangle(triangle,offset_x, 1.73, 0.1, 0.173,'')
    Story.append(pic)
    triangle2 = IMG_PATH+"triangle2.png"
    offset_x = 4.35 + data_dict['cons_mmbtu_min']/data_dict['cons_mmbtu_max']*(7.45-4.35)
    pic = flowable_triangle(triangle2,offset_x, 0.7,0.08, 0.138,'High Performance Home')
    Story.append(pic)
    

    ### BODY
    ##BODY LEFT
    p3 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_t, fontName = font_normal, leading = 12, spaceBefore = 24)
    p4 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_t, fontName = font_bold, leading = 12, spaceBefore = 16, spaceAfter = 12)
    p5 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_s, fontName = font_bold, leading = 12)
    p6 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_t, fontName = font_normal, leading = 12, spaceBefore = 0)
    text_left_1 = Paragraph("The Vermont Home Energy Profile is a report a home's expected annual energy costs and usage. The Profile also documents verified home energy upgrades completed by a professional contractror specializing in energy efficiency.  <font name='InterBold'> Energy usage and costs are estimates only.</font> Standardized assumptions are used for variable factors such as weather, occupancy, lights and appliance usage. See reverse side for details.", p3)
    text_left_4 = Paragraph("HOME INFORMATION", p4)
    text_left_5 = Paragraph("LOCATION:", p5)
    text_left_6 = Paragraph(data_dict['street'],p6)
    text_left_7 = Paragraph(data_dict['city'] + ", " + data_dict["state"] + " " + data_dict["zipcode"], p6)
    text_left_8 = Paragraph("YEAR BUILT:", p5)
    text_left_9 = Paragraph(str(int(data_dict['yearbuilt'])),p6)
    text_left_10 = Paragraph("CONDITIONED FLOOR AREA:",p5)
    text_left_11 = Paragraph(str(int(data_dict['finishedsqft']))+' sq. ft.',p6)
    text_left_12 = Paragraph("REPORT INFORMATION", p4)
    text_left_13 = Paragraph("PROFILE ISSUE DATE:", p5)
    text_left_13b = Paragraph(datetime.datetime.now().strftime("%m/%d/%Y"),p6)
    text_left_14 = Paragraph("PROFILE GENERATED BY:", p5)
    text_left_14b = Paragraph(data_dict['author_name'],p6)
    text_left_15 = Paragraph("<font name='InterItalic'>Brought to you by a collaboration of Vermont Residential Energy Labeling Stakeholders and HELIX | Where home energy performance data creates market value.</font>", p5)
    
    left_table = Table([[text_left_1], [text_left_4], [text_left_5], [text_left_6], [text_left_7], 
        [text_left_8], [text_left_9], [text_left_10], [text_left_11], [text_left_12], [text_left_13], [text_left_13b],
        [text_left_14], [text_left_14b], [text_left_15]], 
        colWidths = [1.73 * inch])
    left_table.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 1, CUSTOM_LGREEN),
        ('LINEBELOW',(0,0),(-1,-15), 0.3, colors.white),
        ('LINEBELOW',(0,8),(-1,-7), 0.3, colors.white),
        ('LINEBELOW',(0,13),(-1,-2), 0.3, colors.white),
     ]))    
     
    ##BODY RIGHT
    # COSTS
    chevron = IMG_PATH+"chevron_green.jpg"
    im2 = Image(chevron, 5.80*inch, 0.6*inch)
    
    p7 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_xl, fontName = font_bold, spaceBefore = -38, leftIndent = 10, textColor=colors.white)
    p8 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_l, fontName = font_bold, spaceBefore = -6, leftIndent = 120, spaceAfter = 30)
    p8b = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_s, fontName = font_italic, textColor=colors.red)
    tc1 = Paragraph('$'+"{:,}".format(int(data_dict['score'])), p7)
    tc2 = Paragraph("Expected Annual Energy Costs", p8)
    p14 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_t, fontName = font_bold,  spaceBefore = 0)
    p15 = ParagraphStyle('body_left', alignment = TA_RIGHT, fontSize = font_t, fontName = font_normal,  spaceBefore = -12)
    p16 = ParagraphStyle('body_left', alignment = TA_RIGHT, fontSize = font_t, fontName = font_normal,  spaceBefore = 0)
    tct1 = Paragraph("<font name='InterBold'>The breakdown of fuel usage is an estimate </font><font name='Helvetica'>based on the fuels used in this home</font>", p14) 
    tct = []
    data_dict['elec_score'] = data_dict['solar_score'] + data_dict['elec_score']
    for num, fuel in enumerate(FUELS):
        if data_dict[fuel+'_score'] != 0:
            tct.append([[Paragraph("<font name='FontAwesome'>"+FUELICONS[num]+"</font> " + FUELLABEL[num], p14), Paragraph('$'+"{:,}".format(int(data_dict[fuel+'_score'])), p15), Paragraph("{:,}".format(int(data_dict['cons_'+fuel])) + ' ' + FUELUNIT[num], p16), Paragraph('{0:.2f}'.format(data_dict['rate_'+fuel]) + ' $/'+FUELUNIT[num], p16)]])

    if data_dict['solar_score'] > 0:
        tct.append([[Paragraph("<font name='FontAwesome'>"+FUELICONS[-1]+"</font> Solar", p14), Paragraph('$'+"{:,}".format(int(data_dict['solar_score'])), p15), Paragraph("{:,}".format(int(data_dict['cons_solar'])) + ' kwh', p16)]])
        
    cost_subTable = Table(tct, colWidths = [1.93*inch])
    cost_subTable.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 1, CUSTOM_LGREEN),
     ]))    
    if data_dict['solar_score'] > 0:
        cost_subTable.setStyle(TableStyle([
            ('INNERGRID', (-1,-2), (-1, -1), 1, CUSTOM_DGREEN),
         ]))    
    pie = pie_chart(data_dict)
    if data_dict['evt'] or data_dict['estar_wh'] or data_dict['hers_score'] or data_dict['hes_score']:
        if data_dict['hers_score']:
            t_source = Paragraph("Source: RESNET HERS Index", p8b)
        if data_dict['hes_score']:
            t_source = Paragraph("Source: DOE Home Energy Score", p8b)
    
    
    cost_table = Table([[[tct1], cost_subTable, [pie]],[t_source]], colWidths = [1.94*inch, 1.93*inch, 1.93*inch], spaceBefore=-10)
    cost_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND',(0,0),(-1,-1),colors.white),
#        ('INNERGRID', (-2, -3), (-1, -1), 1, CUSTOM_LGREEN),
     ]))
    
    # TAKE ACTION
    p9 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_h, fontName = font_bold, spaceBefore = -30, leftIndent = 10, textColor=colors.white)
    p10 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_l, fontName = font_bold, spaceBefore = -14, leftIndent = 120, spaceAfter = 30, backColor = 'white')
    p10b = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_h, fontName = font_bold, spaceBefore = -14, leftIndent = 120, spaceAfter =17, backColor = 'white')

    p11 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_t, fontName = font_normal,  spaceBefore = -8, spaceAfter = 0, leading=20, backColor = 'white', bulletIndent = 12, firstLineIndent = 0, leftIndent = 12, rightIndent = 12, borderPadding = (0, 12, 0, 12))
    p12 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_t, fontName = font_normal,  spaceBefore = -1, spaceAfter = 0, leading=20, backColor = 'white', bulletIndent = 12, firstLineIndent = 0, leftIndent = 12, rightIndent = 12, borderPadding = (0, 12, 0, 12))
    p13 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_t, fontName = font_italic,  spaceBefore = -1, spaceAfter = 0, leading=20, backColor = 'white', firstLineIndent = 0, leftIndent = 12, rightIndent = 12, borderPadding = (0, 12, 0, 12))
    p14 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_t, fontName = font_normal,  spaceBefore = -1, spaceAfter = 20, leading=20, backColor = 'white', bulletIndent = 12, firstLineIndent = 0, leftIndent = 12, rightIndent = 12, borderPadding = (0, 12, 0, 12))
    
    tc3 = Paragraph('TAKE ACTION!', p9)
    tc4 = Paragraph("The following actions can help you save money on your energy costs for years to come", p10b)
    if data_dict["evt"] or data_dict["estar_wh"] or data_dict["hers_score"] or data_dict["hes_score"]:
        tb = [Paragraph("Contact a certified energy professional to learn how to make your home more efficient and comfortable and what financial incentives are available.", p11, bulletText=unchecked.encode('UTF8')), 
        Paragraph('Turn it off. ALL the way off. When not in use, power down all electronics completely to avoid “phantom electricity loads" or invest in an advanced power strip to do it for you.', p12, bulletText=unchecked.encode('UTF8')), 
        Paragraph("Vacuum coils, vents, and ducts. Remove the dust buildup collecting on your refrigerator and heating systems by vacuuming the coils and condenser unit behind and underneath the refrigerator at least once a year.  If you have a forced-air system, you can vacuum the vents and ducts and change air filters.", p14, bulletText=unchecked.encode('UTF8'))]
    else:
        tb = [Paragraph("Schedule regular maintenance with a professional for your heating and cooling (if applicable) equipment to ensure optimum performance.", p11, bulletText=unchecked.encode('UTF8')), 
        Paragraph("Ensure insulation levels meet Vermont Residential Building Energy Standards.", p12, bulletText=unchecked.encode('UTF8')), 
        Paragraph("Discover if unseen air leaks are contributing to heat loss and creating uncomfortable drafts in your home.", p12, bulletText=unchecked.encode('UTF8')),
        Paragraph("Verify all appliances and mechanical equipment are ENERGY STAR&reg; certified.", p14, bulletText=unchecked.encode('UTF8'))]
    tb5 = Paragraph(" ", p14)

    tc5 = Paragraph('ACHIEVEMENTS', p9)
    tc6 = Paragraph("Completed Actions, Home Energy Certifications and Improvement Measures", p10b)
    t_achieve = []
    t_achieve.append(Paragraph(" ",p11))
    
    if data_dict['evt'] or data_dict['estar_wh'] or data_dict['hers_score'] or data_dict['hes_score']:
        if data_dict['evt']:
            t_achieve.append(Paragraph(data_dict['evt'], p12, bulletText=checked.encode('UTF8')))
        if data_dict['estar_wh']:
            t_achieve.append(Paragraph('EPA ENERGYSTAR® Home', p12, bulletText=checked.encode('UTF8')))
        if data_dict['hers_score']:
            t_achieve.append(Paragraph('HERS Index Score: ' + str(data_dict['hers_score']), p12, bulletText=checked.encode('UTF8')))
        if data_dict['hes_score']:
            t_achieve.append(Paragraph('Home Energy Score: ' + str(data_dict['hes_score']) + '/10', p12, bulletText=checked.encode('UTF8')))
    else:
        t_achieve.append(Paragraph("Generated a Vermont Home Energy Profile.", p12, bulletText=checked.encode('UTF8')))
        t_achieve.append(Paragraph("Congratulations! You've taken the first step to understanding your home's energy use… ", p13))  
    
    body_table = Table([[left_table, 
        [im2, tc1, tc2, cost_table, Spacer(1, 12), im2, tc5, tc6, t_achieve, Spacer(1, 12), im2, tc3, tc4, tb]]], 
        colWidths = [1.73 * inch, 5.97 * inch])
    body_table.setStyle(TableStyle([
#        ('BACKGROUND',(1,0),(-1,0),colors.HexColor('#41ad49')), 
        ('ALIGN', (0,0), (-1,-1), 'LEFT'), 
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    Story.append(body_table)

### Page 2
    Story.append(PageBreak())
    p15 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_ll, fontName = font_bold,  spaceBefore = 10, spaceAfter = 10, leading=0, firstLineIndent = 0, textColor=CUSTOM_DGREEN)
    p16 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_s, fontName = font_normal,  spaceBefore = 12, spaceAfter = 2, leading=12, firstLineIndent = 0)
    p17 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_s, fontName = font_normal,  spaceBefore = 12, spaceAfter = -11, leading=12, firstLineIndent = 0)
    p18 = ParagraphStyle('body_left', alignment = TA_LEFT, fontSize = font_t, fontName = font_bold,  spaceBefore = 10, spaceAfter = 10, leading=0, firstLineIndent = 0)
    p19 = styles["BodyText"]
    p19.fontSize = 7
    p19.alignment = TA_CENTER
    p19.leading = 8
    
    p2_h1 = Paragraph("How do a Home's Features Impact Expected Energy Costs?",p15)
    Story.append(p2_h1)
    
    line_table = Table([''], colWidths = [7.8*inch])
    line_table.setStyle(TableStyle([
         ("LINEBELOW", (0,0), (-1,-1), 1, colors.grey),
       ]))
    Story.append(line_table)
    Story.append(Spacer(1, 10))
    
    
    p2_t1_tt1 = Paragraph("LOW ENERGY USE",p19)
    p2_t1_tt2 = Paragraph("VERMONT ENERGY CODE",p19)
    p2_t1_tt3 = Paragraph("HIGH ENERGY USE",p19)
    p2_t1_tt4 = Paragraph("<font name='InterItalic'>Efficiency Vermont Certified High Performance Home</font>",p19)
    p2_t1_tt5 = Paragraph("<font name='InterItalic'>Vermont 2015 Residential Building Energy Standards (RBES)</font>",p19)
    p2_t1_tt6 = Paragraph("<font name='InterItalic'>Typical Pre-Weatherized Existing Home</font>",p19)
    p2_t1_t1 = Paragraph("Triple-Pane, LowE, High Solar Gain",p19)
    p2_t1_t2 = Paragraph("Double-Pane (U-0.32), LowE", p19)
    p2_t1_t3 = Paragraph("Single-Pane, Clear",p19)
    p2_t1_t4 = Paragraph(geq.encode('UTF8') + "90 AFUE, ENERGYSTAR" + registered.encode('UTF8'),p19)
    p2_t1_t5 = Paragraph("80 AFUE, Federal minimum", p19)
    p2_t1_t6 = Paragraph(leq.encode('UTF8') + "70 AFUE",p19)
    p2_t1_t4b = Paragraph(geq.encode('UTF8') + "9 HSPF, (NEEP ccASHP specification)",p19)
    p2_t1_t5b = Paragraph("8.2 HSPF, Federal minimum", p19)
    p2_t1_t6b = Paragraph(leq.encode('UTF8') + "7 HSPF",p19)
    p2_t1_t4c = Paragraph(geq.encode('UTF8') + "0.74 UEF, ENERGYSTAR" + registered.encode('UTF8'),p19)
    p2_t1_t5c = Paragraph("0.56 UEF, Federal minimum", p19)
    p2_t1_t6c = Paragraph(leq.encode('UTF8') + "0.55 UEF",p19)
    p2_t1_t4d = Paragraph(geq.encode('UTF8') + "2 UEF, ENERGYSTAR" + registered.encode('UTF8'),p19)
    p2_t1_t5d = Paragraph("0.92 UEF, Federal minimum", p19)
    p2_t1_t6d = Paragraph(leq.encode('UTF8') + "0.87 UEF",p19)
    p2_t1_t7 = Paragraph("R-20 (cavity) or R-15 (continuous)",p19)
    p2_t1_t8 = Paragraph(leq.encode('UTF8') + "1 ACH50", p19)
    p2_t1_t9 = Paragraph(geq.encode('UTF8') + "7 ACH50", p19)
    p2_t1_t10 = Paragraph(geq.encode('UTF8') + "R-60", p19)
    p2_t1_t11 = Paragraph(leq.encode('UTF8') + "R-19", p19)
    p2_t1_t12 = Paragraph(geq.encode('UTF8') + "R-25", p19)
    p2_t1_t13 = Paragraph(leq.encode('UTF8') + "R-3", p19)
    p2_t1_t14 = Paragraph('R-20 (cavity) or R-15 (continuous)', p19)
    p2_t1_t15 = Paragraph(geq.encode('UTF8') + '15 SEER, ENERGYSTAR' + registered.encode('UTF8'), p19)
    p2_t1_t16 = Paragraph("14 SEER (Federal Minimum)", p19)
    p2_t1_t17 = Paragraph(leq.encode('UTF8') + "11 SEER", p19)
    p2_t1_t18 = Paragraph('ENERGY STAR' + registered.encode('UTF8'), p19)
    p2_t1_t19 = Paragraph(geq.encode('UTF8') + "75% 'high efficiency'", p19)    
    
    features_table_style = TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'), 
        ('ALIGN', (1,0), (-1,-1), 'CENTER'), 
        ('ALIGN', (-3,-1), (-1,-1), 'RIGHT'), 
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LINEABOVE',(0,2),(-1,-1), 0.15, colors.black),
#        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('FONTSIZE',(0,0),(-1,-1),7),
        ('BACKGROUND',(1,0),(-3,-2),CUSTOM_LGREEN),
        ('BACKGROUND',(2,0),(-2,-2),CUSTOM_YELLOW),
        ('BACKGROUND',(3,0),(-1,-2),CUSTOM_LORANGE),
        ('BACKGROUND',(1,14),(-1,-1),colors.lightgrey),
    ])    
    features_table = Table([
        ['',p2_t1_tt1,p2_t1_tt2,p2_t1_tt3],
        ['',p2_t1_tt4,p2_t1_tt5,p2_t1_tt6],
        ['Building Tightness',p2_t1_t8,'3 ACH50',p2_t1_t9],
        ['Attic Insulation',p2_t1_t10,'R-49',p2_t1_t11],
        ['Wall Insulation',p2_t1_t12, p2_t1_t14, p2_t1_t13],
        ['Basement Wall Insulation','R-40',p2_t1_t7,'R-0'],
        ['Windows & Glass Doors',p2_t1_t1,p2_t1_t2,p2_t1_t3],
        ['Heating System - Gas',p2_t1_t4,p2_t1_t5,p2_t1_t6],
        ['Heating System - Electric',p2_t1_t4b,p2_t1_t5b,p2_t1_t6b],
        ['Cooling System',p2_t1_t15,p2_t1_t16,p2_t1_t17],
        ['Hot Water (50gal) - Gas',p2_t1_t4c,p2_t1_t5c,p2_t1_t6c],
        ['Hot Water (50gal) - Electric',p2_t1_t4d,p2_t1_t5d,p2_t1_t6d],
        ['Appliances & Electronics',p2_t1_t18,'n/a','conventional'],
        ['Lighting',"100% LEDs & CFLs",p2_t1_t19,'Incadescent, Halogen'],
        ['Solar PV Present?','','','Solar photovoltaics (PV) generate electricity from the sun with zero emissions'],
    ], 
        colWidths = [1.45*inch, 1.24*inch, 1.24*inch, 1.24*inch])
    features_table.setStyle(features_table_style)
    
    p2_s1_t1 = Paragraph("Mind your R's and U's!", p18)
    p2_s1_t2 = Paragraph("Becoming familiar with the efficiency values of the various components of a home will help you understand why the home uses energy the way it does.  Energy features that contribute to a home’s Expected Annual Energy Use and  Costs are listed to the right.  Learn where this home falls on the energy spectrum and where opportunities are to reduce energy waste!",p16)
    work_table_style = TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'), 
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
#        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
#         ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ])
    work_table = Table([[[p2_s1_t1, p2_s1_t2],[features_table]]], 
        colWidths = [2.6 * inch, 5.2*inch])
    work_table.setStyle(work_table_style)
    Story.append(work_table)
    
    p2_h2 = Paragraph('What are the components of the Vermont Home Energy Profile?',p15)
    Story.append(p2_h2)    
    Story.append(line_table)
    Story.append(Spacer(1, 10))
    
    p2_s2_i1 = Image(wedge, 2.4*inch, 0.99*inch) 
    genericpie = IMG_PATH+"GenericExpectedEnergyChart.png"
    p2_s2_i2 = Image(genericpie, 0.99*inch, 0.99*inch)
     

    p2_s2_t1 = Paragraph("EXPECTED ENERGY USE", p18)
    p2_s2_t2 = Paragraph("This section converts the total energy used in this home (electricity and fossil fuels like oil or gas) to a common unit of energy (MMBtu). A low MMBtu identifies a home as energy efficient with a smaller carbon footprint and lower energy costs.",p16)
    p2_s2_t3 = Paragraph("1MMBtu = ",p17)
    p2_s2_t4 = Paragraph("7 gal fuel oil",p17,bulletText=u'\u2022')
    p2_s2_t5 = Paragraph("710 therms of natural gas",p17,bulletText=u'\u2022')
    p2_s2_t6 = Paragraph("11 gal of propane",p17,bulletText=u'\u2022')
    p2_s2_t7 = Paragraph("293 kWh of electricity",p17,bulletText=u'\u2022')
    p2_s2_t8 = Paragraph(".05 cords of wood",p17,bulletText=u'\u2022')
    
    p2_s2_t9 = Paragraph("EXPECTED ENERGY COSTS", p18)
    p2_s2_t10 = Paragraph("When the source of Energy Costs is AEM, publicly available information about a home, such as its age, size, heating system type and fuel are used to provide an alogrithm-based estimate the home's likely annual energy costs.",p16)
    p2_s2_t10b = Paragraph("When the source of Energy Costs is Third-Party Verified, an energy professional has visited the home and generated an energy model using detailed information about the home's actual energy features. Standard assumptions are used for variable factors such as weather and occupancy.", p16)
    p2_s2_t10c = Paragraph('Average annual fuel prices are obtained from the <a href="https://www.eia.gov/petroleum/data.php">U.S. Energy Information Administration (EIA)</a> and the <a href="https://publicservice.vermont.gov/publications-resources/publications/fuel_report">Vermont Public Service Department</a>.', p16)

    p2_s2_t11 = Paragraph("USEFUL ENERGY TERMS & DEFINITIONS", p18)
    p2_s2_t12 = Paragraph("<font name='InterBold'>R-Value:</font> Measures the resistance of heat flow through a material such as insulation.  Higher R-Values mean more heat stays inside your home and heating systems run less.", p17)
    p2_s2_t12b = Paragraph("<font name='InterBold'>U-Value:</font> The performance rating for windows. A lower U-Value indicates a better performing window and a more comfortable home.", p17)
    p2_s2_t12c = Paragraph("<font name='InterBold'>Low-E:</font> Low emissivity is a coating applied to windows that reflects heat back to its source so it helps your home stay cooler in the summer and warmer in the winter.", p17)
    p2_s2_t12d = Paragraph("<font name='InterBold'>ACH50:</font> Air changes per hour at 50 pascals.  Lower values mean the home is properly-sealed and has fewer air leaks.", p17)
    p2_s2_t12e = Paragraph("<font name='InterBold'>AFUE:</font> Annual Fuel Utilization Efficiency. Defines the efficiency of fossil fuel furnaces and boilers. Higher is better.", p17)
    p2_s2_t12f = Paragraph("<font name='InterBold'>HSPF:</font> Heating Seasonal Performance Factor. Defines the efficiency of air source heat pumps in heating mode. Higher is better.", p17)
    p2_s2_t12e = Paragraph("<font name='InterBold'>SEER:</font> Seasonal Energy Efficiency Ratio. Defines the efficiency of central air conditioners and air source heat pumps in cooling mode. Higher is better.", p17)
    p2_s2_t12g = Paragraph("<font name='InterBold'>SEER:</font> Uniform Energy Factor measures water heaters performance. A higher UEF rating is more energy efficient. Higher is better.", p17)
    cost_table = Table([[p2_s2_i2,p2_s2_i1, ''], [[p2_s2_t9, p2_s2_t10, p2_s2_t10b, p2_s2_t10c], [p2_s2_t1, p2_s2_t2, p2_s2_t3, p2_s2_t4, p2_s2_t5, p2_s2_t6, p2_s2_t7, p2_s2_t8],[p2_s2_t11, p2_s2_t12, p2_s2_t12b, p2_s2_t12c, p2_s2_t12d, p2_s2_t12e, p2_s2_t12f, p2_s2_t12g]]], 
        colWidths = [2.6 * inch, 2.6 * inch, 2.6*inch])
    cost_table_style = TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'), 
        ('ALIGN', (0,0), (-2,-2), 'CENTER'), 
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND',(0,0),(-2,-2),colors.lightgrey),
        ('INNERGRID', (0,0), (-2,-2), 5, colors.white),
#         ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ])        
    cost_table.setStyle(cost_table_style)
    Story.append(cost_table)
    

    p2_h3 = Paragraph('Take action!',p15)
    Story.append(p2_h3)    
    Story.append(line_table)
    Story.append(Spacer(1, 10))
    
    p2_s3_t1 = Paragraph("<font name='InterBold'>Information is power!</font> The Vermont Home Energy Profile can inform the next steps to improve this home’s energy efficiency by indicating specific features that can be improved.", p16)
    p2_s3_t2 = Paragraph("If you have questions about how to interpret this Profile please contact Efficiency Vermont at 888-921-5990.",p16)
    p2_s3_t3 = Paragraph("For energy saving tips, links to qualified contractors, financing, and cash back rebates on energy saving equipment and services, contact the organizations listed here:",p16)
    p2_s3_t4 = Paragraph("<font name='InterBold'>Efficiency Vermont •</font> 888-921-5990",p17)
    p2_s3_t5 = Paragraph('<a href="www.efficiencyvermont.com">www.efficiencyvermont.com</a>',p17)
    p2_s3_t6 = Paragraph("<font name='InterBold'>Vermont Gas Systems •</font> 888-921-5990",p17)
    p2_s3_t7 = Paragraph('<a href="www.vermontgas.com">www.vermontgas.com</a>',p17)
    p2_s3_t8 = Paragraph("<font name='InterBold'>Burlington Electric Department</font>",p17)
    p2_s3_t9 = Paragraph('802-865-7342 • <a href="www.burlingtonelectric.com">www.burlingtonelectric.com</a>',p17)
    p2_s3_t10 = Paragraph("<font name='InterBold'>Vermont’s Weatherization Program</font>",p17)
    p2_s3_t11 = Paragraph('<a href="www.dcf.vermont.gov/oeo/weatherization">www.dcf.vermont.gov/oeo/weatherization</a>',p17)
    
    action_table = Table([[[p2_s3_t1, p2_s3_t2],[p2_s3_t3],[p2_s3_t4, p2_s3_t5, p2_s3_t6, p2_s3_t7, p2_s3_t8, p2_s3_t9, p2_s3_t10, p2_s3_t11]]], 
        colWidths = [2.6 * inch, 2.6 * inch, 2.6*inch])
    action_table_style = TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'), 
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ])        
    action_table.setStyle(action_table_style)
    Story.append(action_table)
    
    
    
### BUILD PAGE
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)


if __name__ == '__main__':
    data_dict = {'street': '123 Main St', 'city': 'Montpelier', 'state': 'VT', 'zipcode': '05000', 
        'yearbuilt': 2005, 'finishedsqft': 2200, 'score': 3137.0, 'cons_mmbtu': 93.0, 'cons_mmbtu_max': 231.0, 'cons_mmbtu_min': 25.0,
        'heatingfuel': 'Natural Gas', 'ng_score': 1531, 'elec_score': 1600, 'ho_score': 251, 'propane_score': 0, 'wood_cord_score': 0, 'wood_pellet_score': 0, 'solar_score': 1450,
        'cons_elec': 15000,'cons_ng': 150, 'cons_ho': 50, 'cons_propane': 0, 'cons_wood_cord': 0, 'cons_wood_pellet': 0, 'cons_solar': 1500,
        'rate_ho': 2.5,  'rate_propane': 3.0, 'rate_ng': 1.4, 'rate_elec': 0.2, 'rate_wood_cord': 200, 'rate_wood_pellet': 0.1,
        'evt': '', 'hers_score': None, 'hes_score': 10, 'estar_wh': False, 'author_name': 'John Doe'}
    out_file = 'VTLabel.pdf'
    write_vermont_energy_profile_pdf(data_dict, out_file)