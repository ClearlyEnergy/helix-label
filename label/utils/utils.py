# implemented this class so that we can colour our frames, for this particular project we wanted to colour the first frame
import csv
import os
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.lib.colors import toColor
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Flowable, SimpleDocTemplate, Frame, Image
from reportlab.platypus import Paragraph


class ColorFrameSimpleDocTemplate(SimpleDocTemplate, object):
    def handle_frameBegin(self, **kwargs):
        super(ColorFrameSimpleDocTemplate, self).handle_frameBegin(**kwargs)

        if hasattr(self.frame, 'background'):
            self.frame.drawBackground(self.canv)

        if hasattr(self.frame, 'roundedBackground'):
            self.frame.drawRoundedBackground(self.canv)


class ColorFrame(Frame, object):
    """ Extends the reportlab Frame with the ability to draw a background color. """

    def __init__(
            self, x1, y1, width, height, leftPadding=6, bottomPadding=6,
            rightPadding=6, topPadding=6, id=None, showBoundary=0,
            overlapAttachedSpace=None, _debug=None, background=None, roundedBackground=None):

        Frame.__init__(
            self, x1, y1, width, height, leftPadding,
            bottomPadding, rightPadding, topPadding, id, showBoundary,
            overlapAttachedSpace, _debug)
        if background is not None:
            self.background = background
        if roundedBackground is not None:
            self.roundedBackground = roundedBackground

    def drawBackground(self, canv):
        color = toColor(self.background)

        canv.saveState()
        canv.setFillColor(color)
        canv.rect(
            self._x1, self._y1, self._x2 - self._x1, self._y2 - self._y1,
            stroke=0, fill=1
        )
        canv.restoreState()

    def drawRoundedBackground(self, canv):
        color = toColor(self.roundedBackground)

        canv.saveState()
        canv.setFillColor(color)
        canv.roundRect(
            self._x1, self._y1, self._x2 - self._x1, self._y2 - self._y1,
            4, stroke=0, fill=1
        )
        canv.restoreState()

    def addFromList(self, drawlist, canv):
        if self.background:
            self.drawBackground(canv)
        Frame.addFromList(self, drawlist, canv)


class Hes_Image(Image):

    def wrap(self, availWidth, availHeight):
        height, width = Image.wrap(self, availWidth, availHeight)
        return width, height

    def draw(self):

        # Image.canv.
        self.canv.drawString(100, 400, '8uiuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu')
        # self.canv.rotate(45)
        Image.draw(self)

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

class Charts():
    
    def pie_chart(data_dict, fuels, fuel_icons, fuel_color):
        drawing = Drawing(width=1.0*inch, height=1.0*inch)
        data = []
        labels = []
        order = []

        for num, fuel in enumerate(fuels):
            if data_dict['energyCost'+fuel] > 0:
                data.append(int(data_dict['energyCost'+fuel]))
    #            txt += FUELLABEL[num]
                labels.append(fuel_icons[num])
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
            pie.slices[i].fillColor = fuel_color[order[i]]
            pie.slices[i].fontName = 'FontAwesome'
            pie.slices[i].fontSize = 16
        drawing.add(pie)
        return drawing
    
class Scores():
    
    def map_scores(property_type):
        espm_score_mapping = {}
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'energy_star_score.csv')
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                espm_score_mapping[row['Category']] = row
        return espm_score_mapping[property_type]

class Highlights():
    
    def score_box(data_dict, category, colors, font_s, font_h, font_xxl, font_bold, alignment):
        if category == 'ESTAR_SCORE':
            pc101 = ParagraphStyle('column_1', alignment = alignment, fontSize = font_h, fontName = font_bold, textColor=colors.white, leading=14)
            pc102 = ParagraphStyle('column_1', alignment = alignment, fontSize = font_xxl, fontName = font_bold, textColor = colors.white)
            pc103 = ParagraphStyle('column_2', alignment = alignment, fontSize = font_s, fontName = font_bold, textColor = colors.white, spaceBefore=26)
            text_c101 = Paragraph("ENERGY STAR SCORE", pc101)
            if data_dict['energy_star_score']:
                text_c102 = Paragraph(str(int(data_dict['energy_star_score']))+'/100', pc102)
            else:
                text_c102 = Paragraph('No score', pc102)                
            text_c103 = Paragraph('50=median, 75=high performer', pc103)
        else:
            text_c101 = Paragraph("TBD", pc101)
            text_c102 = Paragraph('value', pc102)
            text_c103 = Paragraph('range', pc103)
        
        return text_c101, text_c102, text_c103
        
    def cert_commercial(data_dict, font_size, font_normal, font_color, icon, alignment, num_line):
        t_cert = []
        pc272 = ParagraphStyle('body_left', alignment = alignment, textColor = font_color, fontSize = font_size, fontName = font_normal,  spaceBefore = -1, spaceAfter = 0, leading=10, backColor = 'white', bulletIndent = 12, firstLineIndent = 0, leftIndent = 12, rightIndent = 6)
        if 'energyStarCertificationYears' in data_dict and data_dict['energyStarCertificationYears']:
            t_cert.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> EPA ENERGYSTAR® Certified Building''', pc272)])
        
        t_cert.append(Paragraph("", pc272))
        t_cert = [t_cert]
        num_line += 1

        return t_cert, num_line

    def general_commercial(data_dict, font_size, font_normal, font_color, icon, alignment, num_line):
        t_achieve = []
        pc272 = ParagraphStyle('body_left', alignment = alignment, textColor = font_color, fontSize = font_size, fontName = font_normal,  spaceBefore = -1, spaceAfter = 0, leading=10, backColor = 'white', bulletIndent = 12, firstLineIndent = 0, leftIndent = 12, rightIndent = 6)
        
        t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"This building’s greenhouse gas consumption was: " + str(data_dict['totalGHGEmissions'])+" metric tons CO2e", pc272)])
        num_line += 1
        t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"This building’s energy use intensity was: " + str(data_dict['site_total'])+" MMBTU/ft2", pc272)])
        num_line += 1
        t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"The national median energy use intensity for " +  data_dict['systemDefinedPropertyType'].lower()+ " was: " + str(data_dict['medianSiteIntensity'])+" MMBTU/ft2", pc272)])
        num_line += 1
        if 'yoy_percent_change_site_eui_2022' in data_dict:
            if abs(data_dict['yoy_percent_change_site_eui_2022']) > 0:
                if num_line <= 5:
                    t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"Change in energy use intensity since last year: " + str(100.0*data_dict['yoy_percent_change_site_eui_2022'])+" %", pc272)])
                    num_line += 1
                if num_line <= 5:
                    t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"Change in electricity consumption since last year: " + str(100.0*data_dict['yoy_percent_change_elec_2022'])+" %", pc272)])
                    num_line += 1
#Can you vertically center the “Take Action!” label?
#Can you add Building Type under Building Information and pull the Primary Property Use field?

        return t_achieve, num_line

    def solar_commercial(data_dict, font_size, font_normal, font_color, icon, alignment, num_line):
        t_achieve = []
        pc272 = ParagraphStyle('body_left', alignment = alignment, textColor = font_color, fontSize = font_size, fontName = font_normal,  spaceBefore = -1, spaceAfter = 0, leading=10, backColor = 'white', bulletIndent = 12, firstLineIndent = 0, leftIndent = 12, rightIndent = 6)
        pc273 = ParagraphStyle('body_left', alignment = alignment, textColor = font_color, fontSize = font_size, fontName = font_normal)
        if data_dict['onSiteRenewableSystemGeneration'] > 0.0 and num_line <= 5:
            t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"This building generated " + str(data_dict['onSiteRenewableSystemGeneration']) + ' KWh of solar or wind on site', pc273)])
            num_line +=1
        
        if (data_dict['numberOfLevelOneEvChargingStations'] > 0 or data_dict['numberOfLevelTwoEvChargingStations'] > 0 or data_dict['numberOfDcFastEvChargingStations'] > 0) and num_line <= 5:
            t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"This building has an electric vehicle charging on-site", pc273)])
            num_line +=1

        return t_achieve, num_line
