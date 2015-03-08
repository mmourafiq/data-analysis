import numpy as np
import matplotlib.pyplot as plt


def plot_data(xs, ys, c, lw, label, linestyle, **kwargs):
    if ys is not None:
        plt.plot(xs, ys, c=c, lw=lw, linestyle=linestyle, label=label, **kwargs)
    else:
        plt.plot(xs, c=c, lw=lw, linestyle=linestyle, label=label, **kwargs)


def plot_measurements(xs, ys=None, c='r', lw=2, label='Measurements', linestyle='--', **kwargs):
    plot_data(xs=xs, ys=ys, c=c, lw=lw, linestyle=linestyle, label=label, **kwargs)


def plot_predictions(xs, ys=None, c='b', lw=2, label='Measurements', linestyle=':', **kwargs):
    plot_data(xs=xs, ys=ys, c=c, lw=lw, linestyle=linestyle, label=label, **kwargs)


def plot_filter(xs, ys=None, c='g', lw=4, label='Filter', linestyle='-', **kwargs):
    plot_data(xs=xs, ys=ys, c=c, lw=lw, linestyle=linestyle, label=label, **kwargs)


def plot_track(xs, ys=None, c='k', lw=2, label='Track', linestyle='-', **kwargs):
    plot_data(xs=xs, ys=ys, c=c, lw=lw, linestyle=linestyle, label=label, **kwargs)


def generate_measurements(x_0, dx, num_measurements, noise, acceleration=0):
    data = []
    for i in xrange(num_measurements):
        data.append(x_0 + dx * i + np.random.randn() * noise)
        dx += acceleration
    return data


def g_h_filter(measurements, x_0, g, h, dx, dt=1.):
    """
    Performs g-h filter on 1 state variable with a fixed g and h.
    :param measurements:
    :param x_0: initial value.
    :param g: g scale factor in g-h filter.
    :param h: h scale factor in g-h filter.
    :param dx: initial change rate.
    :param dt: time step.
    :return:
    """
    x_i = x_0
    predictions = []
    filtered_measurements = []
    for measurement in measurements:
        # predict the value
        x_prediction = x_i + dx * dt
        predictions.append(x_prediction)

        # calculate the residual
        residual = measurement - x_prediction

        # update the change rate
        dx += h * residual / dt
        # update the initial guess/value
        x_i = x_prediction + g * residual

        filtered_measurements.append(x_i)

    return np.array(predictions), np.array(filtered_measurements)


def plot_g_h_results(measurements, predictions, filtered_data, title='', z_label='Scale', ):
    plot_measurements(measurements, label=z_label)
    plot_predictions(predictions)
    plot_filter(filtered_data)
    plt.legend(loc=4)
    plt.title(title)
    plt.gca().set_xlim(left=0, right=len(measurements))
    plt.show()


test = [
    {'title': 'test', 'x_0': 160, 'dx': 1, 'num_x': 30, 'noise': 3},  # testing assumptions
    {'title': 'bad initial', 'x_0': 5, 'x_0_guess': 30, 'dx': 1, 'num_x': 100, 'noise': 10},  # bad initial guess
    {'title': 'extreme noise', 'x_0': 5, 'dx': 1, 'num_x': 100, 'noise': 100},  # extreme noise
    {'title': 'acceleration', 'x_0': 10, 'dx': 0, 'num_x': 20, 'noise': 0, 'acceleration': 2, 'g': 0.2, 'h': 0.02},
    # acceleration, shows the lag error or systemic error

    # varying g, greater g favors measurement instead of prediction
    {'title': 'g = 0.1', 'x_0': 5, 'x_0_guess': 0, 'dx': 5, 'num_x': 100, 'noise': 50, 'g': 0.1},  # g 0.1
    {'title': 'g = 0.5', 'x_0': 5, 'x_0_guess': 0, 'dx': 5, 'num_x': 100, 'noise': 50, 'g': 0.5},  # g 0.5
    {'title': 'g = 0.9', 'x_0': 5, 'x_0_guess': 0, 'dx': 5, 'num_x': 100, 'noise': 50, 'g': 0.9},  # g 0.9]

    # varying h, greater h makes the filter react rapidly to transient changes
    {
        'title': 'h = 0.05', 'x_0': 0, 'x_0_guess': 0, 'dx': 0, 'num_x': 50, 'noise': 50, 'h': 0.05,
        'measurements': np.linspace(0, 1, 50)
    },  # g 0.1
    {
        'title': 'h = 0.05', 'x_0': 0, 'x_0_guess': 0, 'dx': 2, 'num_x': 50, 'noise': 50, 'h': 0.05,
        'measurements': np.linspace(0, 1, 50)
    },  # g 0.5
    {
        'title': 'h = 0.5', 'x_0': 0, 'x_0_guess': 0, 'dx': 2, 'num_x': 50, 'noise': 50, 'h': 0.5,
        'measurements': np.linspace(0, 1, 50)
    },  # g 0.9


]
for t in test:
    g = t.get('g', 0.2)
    h = t.get('h', 0.01)
    x_0 = t.get('x_0_guess', t['x_0'])
    measurements = t.get('measurements')
    if measurements is None:
        measurements = generate_measurements(t['x_0'], t['dx'], t['num_x'], t['noise'], t.get('acceleration', 0))
    plt.xlim([0, t['num_x']])
    plot_track([0, t['num_x']], [measurements[0], measurements[t['num_x'] - 1]], label='Actual weight')
    xs = xrange(1, t['num_x']+1)
    line = np.poly1d(np.polyfit(xs, measurements, 1))
    plot_data(xs, line(xs),  label='least squares', c='y', lw=3, linestyle='-')
    predictions, filtered_measurements = g_h_filter(measurements=measurements, x_0=x_0, dx=t['dx'],
                                                    g=g, h=h, dt=1.)
    plot_g_h_results(measurements, predictions, filtered_measurements, title=t['title'])

measurements = [5, 6, 7, 8, 9, 9, 9, 9, 9, 10, 11, 12, 13, 14, 15, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16]

predictions, filtered_measurements = g_h_filter(measurements=measurements, x_0=4., dx=1., dt=1., g=.302, h=0.054)
plot_g_h_results(measurements, predictions, filtered_measurements, 'g = 0.302, h = 0.054')

predictions, filtered_measurements = g_h_filter(measurements=measurements, x_0=4., dx=1., dt=1., g=.546, h=0.205)
plot_g_h_results(measurements, predictions, filtered_measurements, 'g = 0.546, h = 0.205')