import numpy as np
import matplotlib.pyplot as plt


def linear_regression(x, y=[]):
    if type(x[0]) == tuple:
        x, y = zip(*x)
        x = np.array(x)
        y = np.array(y)
    elif type(x[0]) == list:
        temp = np.array(x)
        x = temp[:, 0]
        y = temp[:, 1]
    else:
        x = np.array(x)
        y = np.array(y)
    if len(x) != len(y):
        return 'ERROR. You have ' + str(len(x)) + ' x-coordinates and ' + str(len(y)) + ' y-coordinates.'
    n = len(x)

    slope = ((x - x.mean()) * y).sum() / ((x - x.mean()) ** 2).sum()
    slope00 = ((x * y).sum()) / (x ** 2).sum()

    intercept = y.mean() - slope * x.mean()
    intercept00 = 0.0

    residuals_squared = (y - slope * x - intercept) ** 2
    residuals_squared00 = (y - slope * x) ** 2
    residuals_squared_sum = residuals_squared.sum()
    residuals_squared00_sum = residuals_squared00.sum()
    D = ((x - x.mean()) ** 2).sum()

    slope_error = np.sqrt((1 / (n - 2)) * residuals_squared_sum / D)
    slope_error00 = np.sqrt(residuals_squared00_sum / ((n - 1) * (x ** 2).sum()))

    intercept_error = np.sqrt(((1 / n) + (x.mean() ** 2) / D) * residuals_squared_sum / (n - 2))

    r = (n * ((x * y).sum()) - (x.sum()) * (y.sum())) / (
                (((n * (x ** 2).sum()) - (x.sum()) ** 2) ** .5) * ((n * ((y ** 2).sum()) - (y.sum()) ** 2) ** .5))
    r00 = np.sqrt(1.0 - (((y - x * slope00) ** 2).sum()) / ((y ** 2).sum()))

    r_squared = r ** 2
    r00_squared = r00 ** 2

    bfl_string = 'LINEAR LEAST-SQUARES REGRESSION ANALYSIS\n\nBEST FIT LINE:\n'
    slope_string = 'slope = ' + str(slope) + '\n'
    intercept_string = 'intercept = ' + str(intercept) + '\n'
    slope_error_string = 'std. error, slope = ' + str(slope_error) + '\n'
    intercept_error_string = 'std. error, intercept = ' + str(intercept_error) + '\n'
    r_squared_string = 'r-squared = ' + str(r_squared) + '\n'
    r_string = 'r = ' + str(r) + '\n'
    number_of_data_points = 'number of data points = ' + str(n)
    bfl_data = (bfl_string + slope_string + intercept_string +
                slope_error_string + intercept_error_string + r_string
                + r_squared_string + number_of_data_points) + '\n\n'
    bfl_string00 = 'BEST FIT LINE THROUGH THE ORIGIN, (0,0):\n'
    slope_string00 = 'slope = ' + str(slope00) + '\n'
    intercept_string00 = 'intercept = ' + str(intercept00) + '\n'
    slope_error_string00 = 'std. error, slope = ' + str(slope_error00) + '\n'

    r_string00 = 'r = ' + str(r00) + '\n'
    r_squared_string00 = 'r-squared = ' + str(r00_squared) + '\n'

    bfl_data00 = (bfl_string00 + slope_string00 + intercept_string00
                  + slope_error_string00 + r_string00
                  + r_squared_string00 + number_of_data_points)
    print(bfl_data + bfl_data00)

    axis_font = {'family': 'serif',
                 'color': 'black',
                 'weight': 'bold',
                 'size': 12,
                 }
    font_big = {'family': 'serif',
                'color': 'black',
                'weight': 'bold',
                'size': 16,
                }
    xmin = x.min()
    xmax = x.max()
    equation = 'y = ' + str(slope) + 'x + ' + str(intercept)
    equation00 = 'y = ' + str(slope00) + 'x'
    xpoints = np.linspace(xmin * .95, xmax * 1.05, 100)

    fig, ax = plt.subplots(2, 1, figsize=(8, 12))

    ax[0].plot(xpoints, xpoints * slope + intercept)
    ax[0].scatter(x, y)
    ax[0].grid()
    ax[0].text(0.5, 0.75, equation, ha='center', va='center', transform=ax[0].transAxes)
    ax[0].set_xlabel('x', fontdict=axis_font)
    ax[0].set_ylabel('y', fontdict=axis_font)
    ax[0].axis('tight')

    ax[1].plot(xpoints, xpoints * slope00)
    ax[1].scatter(x, y)
    ax[1].grid()
    ax[1].text(0.5, 0.75, equation00, ha='center', va='center', transform=ax[1].transAxes)
    ax[1].set_xlabel('x', fontdict=axis_font)
    ax[1].set_ylabel('y', fontdict=axis_font)
    ax[1].axis('tight')

    plt.show()