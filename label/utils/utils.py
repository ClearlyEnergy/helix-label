# implemented this class so that we can colour our frames
from reportlab.platypus import SimpleDocTemplate, Frame 
from reportlab.lib.colors import toColor

class ColorFrameSimpleDocTemplate(SimpleDocTemplate,object):
    def handle_frameBegin(self, **kwargs):
        super(ColorFrameSimpleDocTemplate,self).handle_frameBegin(**kwargs)
        
        if hasattr(self.frame, 'background'):
            self.frame.drawBackground(self.canv)

# From http://blog.stacktrace.ch/post/27830893647
class ColorFrame(Frame,object):
    """ Extends the reportlab Frame with the ability to draw a background color. """
    
    def __init__(self, x1, y1, width,height, leftPadding=6, bottomPadding=6,
            rightPadding=6, topPadding=6, id=None, showBoundary=0,
            overlapAttachedSpace=None,_debug=None,background=None):
        
        Frame.__init__(self, x1, y1, width, height, leftPadding,
            bottomPadding, rightPadding, topPadding, id, showBoundary,
            overlapAttachedSpace, _debug)
        
        self.background = background

    def drawBackground(self, canv):
        color = toColor(self.background)
        
        canv.saveState()
        canv.setFillColor(color)
        canv.rect(
            self._x1, self._y1, self._x2 - self._x1, self._y2 - self._y1,
            stroke=0, fill=1
        )
        canv.restoreState()

    def addFromList(self, drawlist, canv):
        if self.background:
            self.drawBackground(canv)
        Frame.addFromList(self, drawlist, canv)