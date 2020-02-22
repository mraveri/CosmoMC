# -*- coding: utf-8 -*-

# define log-linear scale: far from being fully functional...
import numpy as np
from numpy import ma

from matplotlib import rcParams
from matplotlib import scale as mscale
from matplotlib.scale import ScaleBase
from matplotlib import transforms as mtransforms
from matplotlib.transforms import Transform
from matplotlib.ticker import Locator, Formatter, FixedLocator, LogFormatterSciNotation, NullFormatter

class LogLinLocator(Locator):
    """
    Determine the tick locations for log-lin axes
    """

    def __init__(self, transform=None, subs=None, linthresh=None, base=None):
        """
        place ticks on the location= base**i*subs[j]
        """
        if transform is not None:
            self._base = transform.base
            self._linthresh = transform.linthresh
        elif linthresh is not None and base is not None:
            self._base = base
            self._linthresh = linthresh
        else:
            raise ValueError("Either transform, or both linthresh "
                             "and base, must be provided.")
        if subs is None:
            self._subs = [1.0]
        else:
            self._subs = subs
        self.numticks = 15

    def set_params(self, subs=None, numticks=None):
        """Set parameters within this locator."""
        if numticks is not None:
            self.numticks = numticks
        if subs is not None:
            self._subs = subs

    def __call__(self):
        'Return the locations of the ticks'
        # Note, these are untransformed coordinates
        vmin, vmax = self.axis.get_view_interval()
        return self.tick_values(vmin, vmax)

    def tick_values(self, vmin, vmax):
        b = self._base
        t = self._linthresh

        if vmax < vmin:
            vmin, vmax = vmax, vmin

        # The domain is divided into three sections, only some of
        # which may actually be present.
        #
        # <======== -t ==0== t ========>
        # aaaaaaaaa    bbbbb   ccccccccc
        #
        # a) and c) will have ticks at integral linear positions.  The
        # number of ticks needs to be reduced if there are more
        # than self.numticks of them.
        #
        # b) has a tick at integral log positions.
        #
        # t will have a tick to mark the transition between scales.
        #
        # "simple" mode is when the range falls entirely within (-t,
        # t) -- it should just display (vmin, 0, vmax)
        has_a = has_b = has_c = False
        if vmin < -t:
            has_a = True
            if vmax > -t:
                has_b = True
                if vmax > t:
                    has_c = True
        elif vmin < 0:
            if vmax > 0:
                has_b = True
                if vmax > t:
                    has_c = True
            else:
                return [vmin, vmax]
        elif vmin < t:
            if vmax > t:
                has_b = True
                has_c = True
            else:
                return [vmin, vmax]
        else:
            has_c = True

        def get_log_range(lo, hi):
            lo = np.floor(np.log(lo) / np.log(b))
            hi = np.ceil(np.log(hi) / np.log(b))
            return lo, hi

        # First, calculate all the ranges, so we can determine striding
        if has_a:
            if has_b:
                a_range = get_log_range(t, -vmin + 1)
            else:
                a_range = get_log_range(-vmax, -vmin + 1)
        else:
            a_range = (0, 0)

        if has_c:
            if has_b:
                c_range = get_log_range(t, vmax + 1)
            else:
                c_range = get_log_range(vmin, vmax + 1)
        else:
            c_range = (0, 0)

        total_ticks = (a_range[1] - a_range[0]) + (c_range[1] - c_range[0])

        if has_b:
            total_ticks += 1
        stride = max(np.floor(float(total_ticks) / (self.numticks - 1)), 1)

        decades = []
        if has_a:
            decades.extend(-1 * (b ** (np.arange(a_range[0], a_range[1],
                                                 stride)[::-1])))

        if has_c:
            decades.extend(b ** (np.arange(c_range[0], c_range[1], stride)))

        # Add the subticks if requested
        if self._subs is None:
            subs = np.arange(2.0, b)
        else:
            subs = np.asarray(self._subs)

        if len(subs) > 1 or subs[0] != 1.0:
            ticklocs = []
            for decade in decades:
                ticklocs.extend(subs * decade)
        else:
            ticklocs = decades

        return self.raise_if_exceeds(np.array(ticklocs))

    def view_limits(self, vmin, vmax):
        'Try to choose the view limits intelligently'
        b = self._base
        if vmax < vmin:
            vmin, vmax = vmax, vmin

        if rcParams['axes.autolimit_mode'] == 'round_numbers':
            if not is_decade(abs(vmin), b):
                if vmin < 0:
                    vmin = -decade_up(-vmin, b)
                else:
                    vmin = decade_down(vmin, b)
            if not is_decade(abs(vmax), b):
                if vmax < 0:
                    vmax = -decade_down(-vmax, b)
                else:
                    vmax = decade_up(vmax, b)

            if vmin == vmax:
                if vmin < 0:
                    vmin = -decade_up(-vmin, b)
                    vmax = -decade_down(-vmax, b)
                else:
                    vmin = decade_down(vmin, b)
                    vmax = decade_up(vmax, b)

        result = mtransforms.nonsingular(vmin, vmax)
        return result

class LogLinTransform(Transform):
    input_dims = 1
    output_dims = 1
    is_separable = True
    has_inverse = True

    def __init__(self, base, linthresh, linscale):
        Transform.__init__(self)
        self.base = base
        self.linthresh = linthresh
        self.linscale = linscale
        self._linscale_adj = (linscale / (1.0 - self.base ** -1))
        self._log_base = np.log(base)

    def transform_non_affine(self, a):
        sign = np.sign(a)
        masked = ma.masked_outside(a,
                                  -self.linthresh,
                                  self.linthresh,
                                  copy=False)
        log = sign * self.linthresh * (
            self._linscale_adj +
            ma.log(np.abs(masked) / self.linthresh) / self._log_base)
        if masked.mask.any():
            return ma.where(masked.mask, a * self._linscale_adj, log)
        else:
            return log

    def inverted(self):
        return InvertedLogLinTransform(self.base, self.linthresh,
                                               self.linscale)

class InvertedLogLinTransform(Transform):
    input_dims = 1
    output_dims = 1
    is_separable = True
    has_inverse = True

    def __init__(self, base, linthresh, linscale):
        Transform.__init__(self)
        loglin = LogLinTransform(base, linthresh, linscale)
        self.base = base
        self.linthresh = linthresh
        self.invlinthresh = loglin.transform(linthresh)
        self.linscale = linscale
        self._linscale_adj = (linscale / (1.0 - self.base ** -1))

    def transform_non_affine(self, a):
        sign = np.sign(a)
        masked = ma.masked_outside(a, -self.invlinthresh,
                                  self.invlinthresh, copy=False)
        exp = sign * self.linthresh * (
            ma.power(self.base, (sign * (masked / self.linthresh))
            - self._linscale_adj))
        if masked.mask.any():
            return ma.where(masked.mask, a / self._linscale_adj, exp)
        else:
            return exp

    def inverted(self):
        return LogLinTransform(self.base,
                                       self.linthresh, self.linscale)


class LogLinScale(ScaleBase):
    """
    The symmetrical logarithmic scale is logarithmic in both the
    positive and negative directions from the origin.

    Since the values close to zero tend toward infinity, there is a
    need to have a range around zero that is linear.  The parameter
    *linthresh* allows the user to specify the size of this range
    (-*linthresh*, *linthresh*).
    """
    name = 'loglin'
    # compatibility shim
    LogLinTransform = LogLinTransform
    InvertedLogLinTransform = InvertedLogLinTransform

    def __init__(self, axis, **kwargs):
        """
        *basex*/*basey*:
           The base of the logarithm

        *linthreshx*/*linthreshy*:
          A single float which defines the range (-*x*, *x*), within
          which the plot is linear. This avoids having the plot go to
          infinity around zero.

        *subsx*/*subsy*:
           Where to place the subticks between each major tick.
           Should be a sequence of integers.  For example, in a log10
           scale: ``[2, 3, 4, 5, 6, 7, 8, 9]``

           will place 8 logarithmically spaced minor ticks between
           each major tick.

        *linscalex*/*linscaley*:
           This allows the linear range (-*linthresh* to *linthresh*)
           to be stretched relative to the logarithmic range.  Its
           value is the number of decades to use for each half of the
           linear range.  For example, when *linscale* == 1.0 (the
           default), the space used for the positive and negative
           halves of the linear range will be equal to one decade in
           the logarithmic range.
        """
        if axis.axis_name == 'x':
            base = kwargs.pop('basex', 10.0)
            linthresh = kwargs.pop('linthreshx', 2.0)
            subs = kwargs.pop('subsx', None)
            linscale = kwargs.pop('linscalex', 1.0)
        else:
            base = kwargs.pop('basey', 10.0)
            linthresh = kwargs.pop('linthreshy', 2.0)
            subs = kwargs.pop('subsy', None)
            linscale = kwargs.pop('linscaley', 1.0)

        if base <= 1.0:
            raise ValueError("'basex/basey' must be larger than 1")
        if linthresh <= 0.0:
            raise ValueError("'linthreshx/linthreshy' must be positive")
        if linscale <= 0.0:
            raise ValueError("'linscalex/linthreshy' must be positive")

        self._transform = self.LogLinTransform(base,
                                                       linthresh,
                                                       linscale)

        self.base = base
        self.linthresh = linthresh
        self.linscale = linscale
        self.subs = subs

    def set_default_locators_and_formatters(self, axis):
        """
        Set the locators and formatters to specialized versions for
        symmetrical log scaling.
        """
        axis.set_major_locator(LogLinLocator(self.get_transform()))
        axis.set_major_formatter(LogFormatterSciNotation(self.base))
        axis.set_minor_locator(LogLinLocator(self.get_transform(),
                                                     self.subs))
        axis.set_minor_formatter(NullFormatter())

    def get_transform(self):
        """
        Return a :class:`LogLinTransform` instance.
        """
        return self._transform

mscale.register_scale(LogLinScale)

if __name__=='__main__':

    import matplotlib.pyplot as plt

    x = np.linspace(1.,2500.,1000)
    y = np.sin(10*x)

    plt.plot(x,y)
    plt.gca().set_xscale('loglin', linthreshx=100.,linscalex=.1)
    #plt.gca().set_xticks([10,20,30])
    #plt.gca().set_xticklabels([10,20,30])
    plt.savefig('test.pdf')
