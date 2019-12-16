import os

from matplotlib import pylab
import numpy


class GoldenSection:
    def __init__(self, a, b, e=.1, fi=0.618, f_expr='x**2 + 3x + 1'):
        self.a = a
        self.b = b
        self.e = e
        self.fi = fi
        self.f_expr = f_expr
        self.label = self.f_expr.replace('**', '^').replace('*', '')
        self.interval_label = '{};{}'.format(self.a, self.b)

    def f(self, x):
        result = eval(self.f_expr)
        return result

    def get_axis(self):
        x_axis = numpy.linspace(self.a, self.b, 100)
        y_axis = [self.f(el) for el in x_axis]
        return x_axis, y_axis

    @staticmethod
    def log_step(tolerance, step):
        print('calculation tolerance [{:.2f}] in step [{}]'.format(
            tolerance, step
        ))

    def log_result(self, tolerance, result):
        print('Minimum: [x = {:.2f} +- {:.2f}]'.format(
            result, tolerance))
        print('with value [f(x) = {:.2f}]'.format(
            self.f(result)))

    def run(self):
        print('')
        print(self.label)

        x_lo, x_hi = self.a, self.b
        step = 0
        current_tolerance = x_hi - x_lo
        try:
            os.mkdir('{}'.format(self.label))
        except FileExistsError:
            pass
        try:
            os.mkdir('{}/{}'.format(self.label, self.interval_label))
        except FileExistsError:
            pass

        while current_tolerance >= self.e:
            pylab.clf()
            current_tolerance = x_hi - x_lo
            step += 1

            self.log_step(current_tolerance, step)
            pylab.title('{}: Step {}'.format(self.label, step))
            pylab.xlabel('x')
            pylab.ylabel('f(x)')
            pylab.grid()

            x1 = x_hi - self.fi * x_hi + self.fi * x_lo
            x2 = self.fi * x_hi - self.fi * x_lo + x_lo

            pylab.axvline(x=x1, color='r', linestyle='dashed')
            pylab.axvline(x=x2, color='g', linestyle='dashed')

            pylab.axvline(x=x_lo, color='g')
            pylab.axvline(x=x_hi, color='r')

            # non wide
            pylab.text(x_lo, self.f(x_lo), format(x_lo, '.4f'))
            pylab.text(x_hi, self.f(x_hi), format(x_hi, '.4f'))
            x_axis = numpy.linspace(x_lo, x_hi, 100)

            # wide
            # x_axis = numpy.linspace(self.a, self.b, 100)

            y_axis = [self.f(el) for el in x_axis]
            pylab.plot(x_axis, y_axis)

            pylab.savefig('{}/{}/step{}.png'.format(self.label, self.interval_label, step))
            # pylab.savefig('{}/{}/wide_step{}.png'.format(self.label, self.interval_label, step))

            # pylab.show()
            # pylab.pause(1)

            if self.f(x1) > self.f(x2) and current_tolerance >= self.e:
                x_lo = x1
            elif current_tolerance >= self.e:
                x_hi = x2

        result = (x_hi + x_lo) / 2
        print(x_hi, x_lo, result)
        self.log_result(current_tolerance, result)


if __name__ == '__main__':

    runs = [
        {'a': -20, 'b': 20, 'f_expr': 'x**2 + 3*x - 5'},
        {'a': -500, 'b': 500, 'f_expr': 'x**2 + 3*x - 5'},
        {'a': -1000, 'b': -600, 'f_expr': 'x**2 + 3*x - 5'},

        {'a': -20, 'b': 20, 'f_expr': '40*x**2 + 70*x + 1000'},
        {'a': -500, 'b': 500, 'f_expr': '40*x**2 + 70*x + 1000'},
        {'a': 1000, 'b': 1600, 'f_expr': '40*x**2 + 70*x + 1000'},

        {'a': 0, 'b': 100, 'f_expr': '7*x + 7'},
        {'a': 0, 'b': 5000, 'f_expr': '7*x + 7'},
    ]
    for values in runs:
        GoldenSection(**values).run()
