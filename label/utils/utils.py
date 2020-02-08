# implemented this class so that we can colour our frames, for this particular project we wanted to colour the first frame

from reportlab.platypus import SimpleDocTemplate, Frame, Image
from reportlab.lib.colors import toColor


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
