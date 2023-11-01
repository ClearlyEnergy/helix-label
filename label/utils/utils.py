# implemented this class so that we can colour our frames, for this particular project we wanted to colour the first frame

from reportlab.lib.colors import toColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Frame, Image
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

class Highlights():
    
    def cert_commercial(data_dict, font_size, font_normal, font_color, icon, alignment, num_line):
        t_cert = []
        pc272 = ParagraphStyle('body_left', alignment = alignment, textColor = font_color, fontSize = font_size, fontName = font_normal,  spaceBefore = -1, spaceAfter = 0, leading=10, backColor = 'white', bulletIndent = 12, firstLineIndent = 0, leftIndent = 12, rightIndent = 6)
        if 'energyStarCertificationYears' in data_dict and data_dict['energyStarCertificationYears']:
            t_cert.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> EPA ENERGYSTAR® Certified Building''', pc272)])
        
        t_cert.append(Paragraph("", pc272))
        t_cert = [t_cert]
        num_line += 1

        return t_cert, num_line

    def solar_commercial(data_dict, font_size, font_normal, font_color, icon, alignment, num_line):
        t_achieve = []
        pc272 = ParagraphStyle('body_left', alignment = alignment, textColor = font_color, fontSize = font_size, fontName = font_normal,  spaceBefore = -1, spaceAfter = 0, leading=10, backColor = 'white', bulletIndent = 12, firstLineIndent = 0, leftIndent = 12, rightIndent = 6)
        pc273 = ParagraphStyle('body_left', alignment = alignment, textColor = font_color, fontSize = font_size, fontName = font_normal)
        if data_dict['onSiteRenewableSystemGeneration'] > 0.0 and num_line < 4:
            t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"This building generated " + str(data_dict['onSiteRenewableSystemGeneration']) + 'KWh of solar or wind on site', pc273)])
            num_line +=1
        
        if (data_dict['numberOfLevelOneEvChargingStations'] > 0 or data_dict['numberOfLevelTwoEvChargingStations'] > 0 or data_dict['numberOfDcFastEvChargingStations'] > 0) and num_line < 4:
            t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"This building has an electric vehicle charging on-site", pc273)])
            num_line +=1

        return t_achieve, num_line

    def general_commercial(data_dict, font_size, font_normal, font_color, icon, alignment, num_line):
        t_achieve = []
        pc272 = ParagraphStyle('body_left', alignment = alignment, textColor = font_color, fontSize = font_size, fontName = font_normal,  spaceBefore = -1, spaceAfter = 0, leading=10, backColor = 'white', bulletIndent = 12, firstLineIndent = 0, leftIndent = 12, rightIndent = 6)

        if abs(data_dict['yoy_percent_change_site_eui_2022']) > 0:
            t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"Change in energy use intensity since last year: " + str(100.0*data_dict['yoy_percent_change_site_eui_2022'])+"%", pc272)])
            t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"Change in electricity consumption since last year: " + str(100.0*data_dict['yoy_percent_change_elec_2022'])+"%", pc272)])
        else:
            t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"This building’s energy use intensity was: " + str(data_dict['site_total'])+"MMBTU/ft2", pc272)])
            t_achieve.append([Paragraph('''<img src="'''+icon+'''" height="12" width="12"/> '''+"The national median energy use intensity for [supermarkets] was: " + str(data_dict['medianSiteIntensity'])+"MMBTU/ft2", pc272)])
        
        num_line += 2

        return t_achieve, num_line
