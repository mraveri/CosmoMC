# -*- coding: utf-8 -*-

"""
File with various python utilities.

Author: Marco Raveri (mraveri@uchicago.edu)
"""

################################################################################
# import global settings:
from settings import *

################################################################################

def print_table( table, traspose=True, separator=None, indent='' ):
    """
    This function prints on the screen a nicely formatted table.

    :param table: a 2D list that should be printed on the screen.

    """
    # transpose the table:
    temp_table = format_table( table, traspose=traspose, separator=separator )
    # print:
    for line in temp_table:
        print indent+line

################################################################################

def format_table( table, traspose=True, separator=None ):
    """
    This function formats a table to be nicely printed.
    The idea is to pass a 2D table of strings of different length and have this
    function format everything.

    :param table: a 2D list that should be formatted.

    """
    # get the separator:
    if separator is None:
        _separator = '|'
    if separator is not None:
        _separator = separator
    # transpose the table:
    if traspose: table = map(list, zip(*table))
    # get the column width:
    col_width = [max(len(str(x)) for x in col) for col in zip(*table)]
    #
    return_table = []
    #return_table.append( " " )
    _temp = " "+_separator+" "
    for line in table:
        return_table.append( _separator+" " + _temp.join("{:{}}".format(x, col_width[i]) for i, x in enumerate(line)) + " "+_separator )
    #return_table.append( " " )

    return return_table

################################################################################

def gen_log_space( limit, n ):
    """
    Gives the indexes of a log spaced array.
    """
    result = [1]
    if n>1:  # just a check to avoid ZeroDivisionError
        ratio = (float(limit)/result[-1]) ** (1.0/(n-len(result)))
    while len(result)<n:
        next_value = result[-1]*ratio
        if next_value - result[-1] >= 1:
            # safe zone. next_value will be a different integer
            result.append(next_value)
        else:
            # problem! same integer. we need to find next_value by artificially incrementing previous value
            result.append(result[-1]+1)
            # recalculate the ratio so that the remaining values will scale correctly
            ratio = (float(limit)/result[-1]) ** (1.0/(n-len(result)))
    # round, re-adjust to 0 indexing (i.e. minus 1) and return np.uint64 array
    return np.array(map(lambda x: round(x)-1, result), dtype=np.uint64)

################################################################################

def from_confidence_to_sigma( P ):
    """
    Transforms a probability to effective number of sigmas.

    :param P: the input probability.

    """
    return np.sqrt(2.)*sp.erfinv( P )

################################################################################

def from_sigma_to_confidence( nsigma ):
    """
    Transforms a given number of effecive sigmas to a probability.

    :param nsigma: the input number of sigmas.

    """
    return sp.erf( nsigma/np.sqrt(2.) )

################################################################################

def num_to_mant_exp( num ):
    """
    This function returns the (base 10) exponent and mantissa of a number.

    :param num: input number.
    :type num: :class:`int` or :class:`float`
    :return: tuple (mantissa, exponent) of :class:`int` containing the mantissa
             and the exponent of the input number.
    :rtype: tuple

    """
    try:
        exponent = math.floor(math.log10(abs(num)))
    except ValueError:  # Case of log10(0)
        return (0, 0)   # Convention: 0 = 0*10^0
    mantissa = num/10**exponent
    try:
        return (mantissa, int(exponent))
    except:
        return (float('nan'),float('nan'))

################################################################################

def mant_exp_to_num( mant_exp ):
    """
    This function returns a float built with the given (base 10) mantissa
    and exponent.

    :param mant_exp: (mantissa, exponent) a tuple of two :class:`int` with the
                     mantissa and the exponent of the input number.
    :type mant_exp: tuple
    :return: output number built as mantissa*10**exponent.
    :rtype: :class:`float`

    """
    return mant_exp[0]*10**mant_exp[1]

################################################################################

def nice_number( num, mode=1, digits=1 ):
    """
    This function returns a nice number built with num. This is useful to build
    the axes of a plot.
    The nice number is built by taking the first digit of the number.

    :param num: input number
    :type num: :class:`float` or :class:`int`
    :param mode: (optional) operation to use to build the nice number

            | 0 -- use ceil
            | 1 -- use round
            | 2 -- use floor

    :type mode: :class:`int`
    :param digits: input number of digits to keep
    :type digits: :class:`int`
    :return: a nice number!
    :rtype: :class:`float`

    """
    # extract mantissa and exponent:
    mant, exp = num_to_mant_exp( num )
    # select the working mode and do the truncation:
    if ( mode==0 ):
        mant = np.ceil( mant*10**(digits-1) )/10**(digits-1)
    elif ( mode==1 ):
        mant = np.round( mant, digits-1)
    elif ( mode==2 ):
        mant = np.floor( mant*10**(digits-1) )/10**(digits-1)
    else:
        raise ValueError( 'Wrong worging mode for Fisher_utilities.nice_number' )

    return mant_exp_to_num( ( mant, exp ) )

v_nice_number = np.vectorize(nice_number)

################################################################################

# prints the nice number avoiding ugly prints:
def nice_print(number):
    """
    Formats a nice_number to appear well on the screen.
    With some python versions the format of the nice_number print has to be
    manually enforced.
    """
    return str('{}'.format(number))

################################################################################

def significant_digits( num_err, mode=1, digits=1 ):
    """
    This function returns the number in num_err at the precision of error.

    :param num_err: (number, error) input number and error in a tuple.
    :type num_err: tuple
    :param mode: (optional) operation to use to build the number

            | 0 -- use ceil
            | 1 -- use round
            | 2 -- use floor

    :type mode: :class:`int`
    :param digits: input number of digits to keep
    :type digits: :class:`int`
    :return: a number with all the significant digits according to error
    :rtype: :class:`float`

    """
    number = num_err[0]
    error  = num_err[1]
    number_mant_exp = num_to_mant_exp(number)
    error_mant_exp  = num_to_mant_exp(error)

    temp = mant_exp_to_num( (number_mant_exp[0], number_mant_exp[1]-error_mant_exp[1]) )
    # select the working mode
    if ( mode==0 ):
        temp = np.ceil( temp*10**(digits-1) )/10**(digits-1)
    elif ( mode==1 ):
        temp = np.round( temp, digits-1 )
    elif ( mode==2 ):
        temp = np.floor( temp*10**(digits-1) )/10**(digits-1)
    else:
        raise ValueError('Fisher_utilities.significant_digits called with mode='+str(mode)+' legal values are 0,1,2')

    return temp*10**(error_mant_exp[1])

################################################################################

from matplotlib import markers
from matplotlib.path import Path

def align_marker(marker, halign='center', valign='middle',):
    """
    create markers with specified alignment.

    Parameters
    ----------

    marker : a valid marker specification.
      See mpl.markers

    halign : string, float {'left', 'center', 'right'}
      Specifies the horizontal alignment of the marker. *float* values
      specify the alignment in units of the markersize/2 (0 is 'center',
      -1 is 'right', 1 is 'left').

    valign : string, float {'top', 'middle', 'bottom'}
      Specifies the vertical alignment of the marker. *float* values
      specify the alignment in units of the markersize/2 (0 is 'middle',
      -1 is 'top', 1 is 'bottom').

    Returns
    -------

    marker_array : numpy.ndarray
      A Nx2 array that specifies the marker path relative to the
      plot target point at (0, 0).

    Notes
    -----
    The mark_array can be passed directly to ax.plot and ax.scatter, e.g.::

        ax.plot(1, 1, marker=align_marker('>', 'left'))

    """

    if isinstance(halign, (str, unicode)):
        halign = {'right': -1.,
                  'middle': 0.,
                  'center': 0.,
                  'left': 1.,
                  }[halign]

    if isinstance(valign, (str, unicode)):
        valign = {'top': -1.,
                  'middle': 0.,
                  'center': 0.,
                  'bottom': 1.,
                  }[valign]

    # Define the base marker
    bm = markers.MarkerStyle(marker)

    # Get the marker path and apply the marker transform to get the
    # actual marker vertices (they should all be in a unit-square
    # centered at (0, 0))
    m_arr = bm.get_path().transformed(bm.get_transform()).vertices

    # Shift the marker vertices for the specified alignment.
    m_arr[:, 0] += halign / 2
    m_arr[:, 1] += valign / 2

    return Path(m_arr, bm.get_path().codes)

################################################################################

def make_list( elements ):
    """
    Checks if elements is a list.
    If yes returns elements without modifying it.
    If not creates and return a list with elements inside.

    :param elements: an element or a list of elements
    :return: a list containing elements if elements is not a list, elements otherwise.
    :rtype: list

    """
    if isinstance(elements, (list, tuple)):
        return elements
    else:
        return [elements]

################################################################################

def KL_decomposition( a, b ):
    """
    Computes the KL decomposition of the matrix A and B.
    Notice that B has to be real, symmetric and positive.
    Taken from http://fourier.eng.hmc.edu/e161/lectures/algebra/node7.html
    """
    # compute the eigenvalues of b, lambda_b:
    _lambda_b, _phi_b = np.linalg.eigh( b )
    # check that this is positive:
    if np.any(_lambda_b<0.):
        raise ValueError('B is not positive definite')
    _sqrt_lambda_b  = np.diag( 1./np.sqrt( _lambda_b ) )
    _phib_prime     = np.dot( _phi_b, _sqrt_lambda_b )
    _a_prime        = np.dot( np.dot( _phib_prime.T, a), _phib_prime )
    _lambda, _phi_a = np.linalg.eigh( _a_prime )
    _phi            = np.dot( np.dot( _phi_b, _sqrt_lambda_b), _phi_a )
    return _lambda, _phi

################################################################################

def smooth_gaussian( x, y, sigma ):
    """
    Takes an array and applies Gaussian smoothing in units of the input
    x array.

    Sigma is the smoothing scale in whatever units x has.

    """
    # get the spacing:
    dx     = (np.amax(x)-np.amin(x))/float(len(x))
    # test for legality of sigma:
    if np.abs(3.*sigma) <= dx:
        raise ValueError('smoothing scale (sigma) is smaller than discretization grid')
    # get the grid:
    gx     = np.arange(-3*sigma, 3*sigma, dx)
    # define the un-normalized kernel:
    kernel = np.exp(-(gx/sigma)**2/2)
    # normalize the kernel:
    kernel = kernel/integrate.simps(kernel,xrange(len(kernel)))
    # perform the convolution:
    _temp    = np.convolve(y, kernel, mode="same")
    #
    return _temp

################################################################################

def compute_bounds( samples, weights, confidence_levels=[0.68,0.95,0.997], type='upper' ):
    """
    Computes upper bounds on a parameter starting from a 1D array of samples.
    Specify a list of confidence levels.
    Type can be upper or lower
    """
    # sort the array:
    if type=='upper':
        _idx            = np.argsort( samples )
    elif type=='lower':
        _idx            = np.argsort( -samples )
    _sorted_samples = samples[_idx]
    # compute total number of (weigthed samples):
    total_elements  = np.sum( weights )
    # compute cumulative sum of the weigths and divide by total elements:
    _cum_sum        = np.cumsum( weights[_idx] )/total_elements
    # confidence levels calculation:
    # fast (but not that precise algorithm):
    if False:
        _conf_idx = [ np.abs(_cum_sum-_conf).argmin() for _conf in confidence_levels ]
        cl_bounds = samples[_idx[_conf_idx]]
    # slightly more precise at high confidence:
    if True:
        cl_bounds = []
        for _conf in confidence_levels:
            _temp_weights  = _cum_sum-_conf
            try:
                zero_crossings = np.where(np.diff(np.signbit(_temp_weights)))[0][0]
                cl_bounds.append( -(_sorted_samples[zero_crossings]-_sorted_samples[zero_crossings+1])/(_temp_weights[zero_crossings]-_temp_weights[zero_crossings+1])*_temp_weights[zero_crossings+1]+_sorted_samples[zero_crossings+1] )
            except:
                cl_bounds.append( None )
    # return:
    return cl_bounds

################################################################################

from contextlib import contextmanager

def fileno(file_or_fd):
    fd = getattr(file_or_fd, 'fileno', lambda: file_or_fd)()
    if not isinstance(fd, int):
        raise ValueError("Expected a file (`.fileno()`) or a file descriptor")
    return fd

@contextmanager
def stdout_redirected(to=os.devnull, stdout=None):
    if stdout is None:
       stdout = sys.stdout

    stdout_fd = fileno(stdout)
    # copy stdout_fd before it is overwritten
    #NOTE: `copied` is inheritable on Windows when duplicating a standard stream
    with os.fdopen(os.dup(stdout_fd), 'wb') as copied:
        stdout.flush()  # flush library buffers that dup2 knows nothing about
        try:
            os.dup2(fileno(to), stdout_fd)  # $ exec >&to
        except ValueError:  # filename
            with open(to, 'wb') as to_file:
                os.dup2(to_file.fileno(), stdout_fd)  # $ exec > to
        try:
            yield stdout # allow code to be run with the redirected stdout
        finally:
            # restore stdout to its previous value
            #NOTE: dup2 makes stdout_fd inheritable unconditionally
            stdout.flush()
            os.dup2(copied.fileno(), stdout_fd)  # $ exec >&copied

################################################################################

class Logger(object):
    """
    Logger class to redirect output to both screen and terminal
    """
    def __init__(self,filename):
        self.terminal    = sys.stdout
        self.log         = open(filename, "w")
        # to avoid ansi colors in the output log:
        self.ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    def write(self, message):
        self.terminal.write(message)
        self.log.write(self.ansi_escape.sub('', message))
    def flush(self):
        pass

################################################################################

def QR_inverse(matrix):
    _Q,_R = np.linalg.qr(matrix)
    return np.dot(_Q,np.linalg.inv(_R.T))

################################################################################

# exit if the file is directly called:
if __name__ == "__main__":
    exit()
