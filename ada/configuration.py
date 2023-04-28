# Global configuration for the app
file_types = ["Algem Pro", "Algem HT24", "IP", "PSI", "ADA", "MicrobeMeter", "SpectroStar"]
replicate_types = ["Algem Pro", "IP", "PSI", "ADA", "MicrobeMeter"]
xaxis_units = ["seconds", "minutes", "hours", "days"]
unit_map = {
    "seconds": 24 * 60 * 60,
    "minutes": 24 * 60,
    "hours": 24,
    "days": 1
}
info_options = ["none", "reactor", "profile", "title", "date", "time",
                "date+time"]
line_style_options = ["solid", "dashed", "dashdot", "dotted", "none"]
marker_style_options = {"none": "", "circle": "o", "triangle": "v", "square": "s", "plus": "+", "cross": "x", "diamond": "D"}
style_options = ["default", "greyscale", "colour blind", "pastel", "deep"]
font_options = ["sans-serif", "serif", "cursive", "fantasy", "monospace"]
table_row_options = ["profile", "reactor", "gradient", "time to",
                     "average of condition", "condition at time",
                     "fit parameter"]
fit_options = ["flat line", "linear", "quadratic", "exponential", "zweitering"]
test_options = ["T-test", "ANOVA"]
measurement_options = ['',"gradient", "time to", "fit parameter"]

conf_colors = ['r', 'g', 'b', 'y', 'c', 'm', 'k']

# Width and height ratio
wr = 1.
hr = 1.

# Plotting default values

title = ''

# X axis config
xvar = ''
xname = ''
xunit = ''
xmin = -1
xmax = -1
xlog = False

# Y axis config
yvar = ''
yname = ''
yunit = ''
ymin = -1
ymax = -1
ylog = False
ynormlog = False

# Condition y axis config
condition_yvar = ''
condition_yname = ''
condition_yunit = ''
condition_ymin = -1
condition_ymax = -1
condition_ylog = False

# Data config
smooth = False
align = False
y_alignment = -1
initial_y = -1
auto_remove = False
remove_above = None
remove_below = None
downsample = -1
growth_average = None
condition_average = None
show_events = False

# Measurement config
cursor = False
# Legend config
legend = False
condition_legend = False
legend_title = ''
condition_legend_title = ''
label_names = []
condition_label_names = []
extra_info = 'none'
condition_extra_info = 'none'
only_extra = False
condition_only_extra = False

# Style config
style = ''
font_style = ''
title_size = 14
legend_size = 12
label_size = 12
marker_size = 0
line_width = 2
axis_colour = -1
capsize = 2
grid = False
save_dpi = 600

# Stats config
std_err = False
sig_figs = 2
show_fit_text = False
show_fit_result = False
show_fit_errors = False

# Advanced configuration
sg_window_size = 61
sg_order = 0
sg_deriv = 0
sg_rate = 1
outlier_threshold = 20

# Fitting configuration
do_fit = False
fit_curve = ''
fit_type = ''
fit_from = 0
fit_to = 0
fit_start = []
fit_min = []
fit_max = []