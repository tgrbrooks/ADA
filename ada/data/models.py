import numpy as np

from ada.data.processor import exponent_text, exponent_text_errors


class GrowthModel:
    def __init__(self, latex, params, latex_params, units):
        self.latex = latex
        self.params = params
        self.latex_params = latex_params
        self.units = units

    def param_text(self, fit_result):
        text = ''
        for i, param in enumerate(self.latex_params):
            text += param + ' = ' + \
                exponent_text(fit_result[i]) + ' ' + self.units[i]
            if i < (len(self.params) - 1):
                text += '\n'
        return text

    def param_text_error(self, fit_result, covm):
        errors = np.sqrt(np.diag(covm))
        text = ''
        for i, param in enumerate(self.latex_params):
            text += param + ' = ' + \
                exponent_text_errors(fit_result[i], errors[i]) + ' ' + self.units[i]
            if i < (len(self.params) - 1):
                text += '\n'
        return text

    def get_latex_param(self, param_name):
        for i, param in enumerate(self.params):
            if param == param_name:
                return self.latex_params[i]
        return ''

    def get_units(self, param_name):
        for i, param in enumerate(self.params):
            if param == param_name:
                return self.units[i]
        return ''


class FlatLine(GrowthModel):
    def __init__(self, x_unit, y_unit):
        super().__init__('$y = p$', ['Y intercept (p)'], ['$p$'], [y_unit])

    def func(self):
        def return_func(x, p):
            return np.ones(len(x)) * p
        return return_func


class Linear(GrowthModel):
    def __init__(self, x_unit, y_unit):
        super().__init__('$y = p_1 \cdot x + p_0$',
                         ['Y intercept (p0)', 'Gradient (p1)'],
                         ['$p_0$', '$p_1$'],
                         [y_unit, y_unit + '/' + x_unit])

    def func(self):
        def return_func(x, p0, p1):
            return p1 * x + p0
        return return_func


class Quadratic(GrowthModel):
    def __init__(self, x_unit, y_unit):
        super().__init__('$y = p_2 \cdot x^2 + p_1 \cdot x + p_0$',
                         ['Constant (p0)', 'Linear (p1)', 'Quadratic (p2)'],
                         ['$p_0$', '$p_1$', '$p_2$'],
                         [y_unit, y_unit + '/' + x_unit, y_unit + '/' + x_unit + '$^2$'])

    def func(self):
        def return_func(x, p0, p1, p2):
            return p2 * np.power(x, 2) + p1 * x + p0
        return return_func


class Exponential(GrowthModel):
    def __init__(self, x_unit, y_unit):
        super().__init__('$y = p_0 \cdot \exp(p_1 \cdot x)$',
                         ['Scale (p0)', 'Exponent (p1)'],
                         ['$p_0$', '$p_1$'],
                         [y_unit, x_unit + '$^{-1}$'])

    def func(self):
        def return_func(x, p0, p1):
            return p0 * np.exp(p1 * x)
        return return_func


class Zweitering(GrowthModel):
    def __init__(self, x_unit, y_unit):
        super().__init__('$y = y_0 + (A - y_0)/(1 + \exp((4\mu/A)\cdot(\lambda - x) + 2))$',
                         ['Starting absorbance (y0)', 'Biomass yield (A)', 'Max growth rate (mu)', 'Lag time (lambda)'],
                         ['$y_0$', '$A$', '$\mu$', '$\lambda$'],
                         [y_unit, y_unit, y_unit + '/' + x_unit, x_unit])

    def func(self):
        def return_func(x, y0, A, mu, lam):
            exp_val = (4*mu/A) * (lam - x) + 2
            return y0 + (A - y0) / (1 + np.exp(exp_val))
        return return_func


def get_model(name, x_unit='', y_unit=''):
    if name == 'flat line':
        return FlatLine(x_unit, y_unit)
    if name == 'linear':
        return Linear(x_unit, y_unit)
    if name == 'quadratic':
        return Quadratic(x_unit, y_unit)
    if name == 'exponential':
        return Exponential(x_unit, y_unit)
    if name == 'zweitering':
        return Zweitering(x_unit, y_unit)
    raise RuntimeError('Model not found')
