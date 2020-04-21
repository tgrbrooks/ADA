class Configuration():

    def __init__(self):
        self.title = ''
        # X axis config
        self.xvar = ''
        self.xname = ''
        self.xunit = ''
        self.xmin = -1
        self.xmax = -1
        # Y axis config
        self.yvar = ''
        self.yname = ''
        self.yunit = ''
        self.ymin = -1
        self.ymax = -1
        # Condition y axis config
        self.condition_yvar = ''
        self.condition_yname = ''
        self.condition_yunit = ''
        self.condition_ymin = -1
        self.condition_ymax = -1
        # Data config
        self.smooth = False
        self.align = False
        self.auto_remove = False
        self.remove_above = -1
        self.remove_below = -1
        self.downsample = -1
        # Legend config
        self.legend = False
        self.condition_legend = False
        self.legend_title = ''
        self.condition_legend_title = ''
        self.label_names = []
        self.condition_label_names = []
        self.cursor = False
        self.grid = False
        # Style config
        self.style = ''
        self.font_style = ''
        self.font_size = -1
        self.line_width = -1
