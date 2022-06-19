# Global configuration for the app
file_types = ["Algem Pro", "Algem HT24", "IP", "PSI", "ADA"]
replicate_types = ["Algem Pro", "IP", "PSI", "ADA"]
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