# Global configuration for the app
xaxis_units = ["seconds", "minutes", "hours", "days"]
info_options = ["none", "reactor", "profile", "title", "date", "time",
                "date+time"]
style_options = ["default", "greyscale", "colour blind", "pastel", "deep"]
font_options = ["sans-serif", "serif", "cursive", "fantasy", "monospace"]
table_row_options = ["profile", "reactor", "gradient", "time to",
                     "average of condition", "condition at time",
                     "fit parameter"]
fit_options = ["flat line", "linear", "quadratic", "exponential", "zweitering"]

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
auto_remove = False
remove_zeros = False
remove_above = -1
remove_below = -1
downsample = -1
condition_average = -1
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
title_size = -1
legend_size = -1
label_size = -1
line_width = -1
axis_colour = -1
grid = False

# Stats config
std_err = False

# Fitting configuration
do_fit = False
fit_curve = ''
fit_type = ''
fit_from = 0
fit_to = 0