# -*- coding: utf-8 -*-

"""
Some chains utilities
"""

from settings  import *
from utilities import *

feedback_level = 0

# ***************************************************************************************

def weighted_thin( chain, factor ):
    """
    Thin an MCMC chain with integer weights by accounting for the weights
    """
    thin_ix = chain.thin_indices(factor)
    unique, counts = np.unique(thin_ix, return_counts=True)
    chain.setSamples( chain.samples[unique, :],
                      loglikes = None if chain.loglikes is None else chain.loglikes[unique],
                      weights  = counts,
                      min_weight_ratio=-1)

# ***************************************************************************************

def find_best_burnin( samps, min_burn=0.0, max_burn=0.3 ):
    """
    Finds the burn in value that gives the best R value. The search is limited to [min_burn,max_burn]
    """
    burn_fraction = 0.0
    # start removing burn in values:
    burn_values = np.linspace( min_burn, max_burn, 100 )
    R_values, D_values = [], []
    # get the covariance:
    for _frac in burn_values:
        # copy the input chain:
        _temp_samps  = copy.deepcopy( samps )
        # remove from all chains separately:
        _temp_chains = _temp_samps.getSeparateChains()
        for _chain in _temp_chains: _chain.removeBurn( _frac )
        # rebuild from the thinned chains:
        _temp_samps.chains = _temp_chains
        _temp_samps.makeSingle()
        _temp_samps.updateBaseStatistics()
        # compute R-1:
        R_values.append( _temp_samps.getGelmanRubin() )
        # do covariance change:
        _filter    = np.logical_not( [ temp_name.isDerived for temp_name in _temp_samps.getParamNames().names ] )
        _thin_cov  = _temp_samps.getCov()[_filter,:][:,_filter]
        _thin_dets = [np.linalg.det( _chain.getCov()[_filter,:][:,_filter] ) for _chain in _temp_samps.getSeparateChains() ]
        D_values.append( np.amax( np.abs( _thin_dets/np.linalg.det( _thin_cov )-1.) ) )
    #
    return R_values, D_values

# ***************************************************************************************

def find_loseless_thin( samps, tollerance=0.01 ):
    """
    Finds the thin value that results in R-1=tollerance and does not alter the determinant of the covariance
    by more than tollerance with respect to the full chain.
    """
    thin_factor = 1
    try:
        # get maximum thin factor:
        _temp     = samps.getConvergeTests( what=['RafteryLewis'] )
        _max_thin = samps.Markov_thin
        # get the covariance:
        _filter   = np.logical_not( [ temp_name.isDerived for temp_name in samps.getParamNames().names ] )
        _full_cov = samps.getCov()[_filter,:][:,_filter]
        # helper for the thinning:
        def _helper_thinning(_factor):
            # copy the input chain:
            _temp_samps  = copy.deepcopy( samps )
            # thin separately all the chains:
            _temp_chains = _temp_samps.getSeparateChains()
            for _chain in _temp_chains: weighted_thin(_chain,_factor)
            # rebuild from the thinned chains:
            _temp_samps.chains = _temp_chains
            _temp_samps.makeSingle()
            _temp_samps.updateBaseStatistics()
            # do R convergence tests:
            _Gelman_test = _temp_samps.getGelmanRubin()
            # do covariance change:
            _filter   = np.logical_not( [ temp_name.isDerived for temp_name in _temp_samps.getParamNames().names ] )
            _thin_cov = _temp_samps.getCov()[_filter,:][:,_filter]
            _det_test = np.abs( 1.-np.linalg.det( _thin_cov )/np.linalg.det( _full_cov ) )
            # do the test:
            _test = _Gelman_test<tollerance and _det_test<tollerance
            # feedback:
            if feedback_level>=1:
                print '   Thin: ', _factor, 'R-1', _Gelman_test, 'det', _det_test
            #
            return _test
        # feedback:
        if feedback_level>=2:
            print '   RL thin    = ', _max_thin
            print '   tollerance = ', tollerance
        # do bisection:
        if True:
            _a  = 2
            _b  = _max_thin
            _fa = _helper_thinning(_a)
            _fb = _helper_thinning(_b)
            # two is already bad, return
            if not _fa:
                thin_factor = 1
                return thin_factor
            # RL thin is enough, return
            if _fb:
                thin_factor = _max_thin
                return thin_factor
            # start bisection:
            _c = int( (_a+_b)/2. )
            while _b-_a > 1:
                _val = _helper_thinning(_c)
                if _val:
                    _a = _c
                else:
                    _b = _c
                _c = int( (_a+_b)/2. )
            thin_factor = _c
        # cycle over thinning:
        if False:
            for _ind in range(_max_thin+1)[2:]:
                if _helper_thinning(_ind):
                    thin_factor = _ind
                    break
    except Exception,e:
        print '\033[93m'+'WARNING'+'\033[0m'
        print e
    #
    return thin_factor

# ***************************************************************************************

def compute_bayesian_complexity( samps, mean=None, best_fit=None ):
    """
    Computes Bayesian complexity of the samples
    """
    results        = {}
    num_params     = samps.getParamNames().numNonDerived()
    # mean chi2:
    mean_chi2      = samps.mean( 2.0*samps.loglikes )
    # compute mean complexity:
    if mean is not None:
        complexity_mean = mean_chi2 -2.0*mean.logLike
        results['mean'] = complexity_mean
    # compute best fit complexity:
    if best_fit is not None:
        complexity_bf = mean_chi2 -2.0*best_fit.logLike
        results['bf'] = complexity_bf
    # sample best fit:
    complexity_sbf = mean_chi2 -2.0*np.amin(samps.loglikes)
    results['sbf'] = complexity_sbf
    #
    return results

# ***************************************************************************************

def total_data_chi2( chain ):
    """
    Compute total data best-fit chi square:
    """
    # protect against no minimum:
    if chain.minimum is None:
        return np.inf
    # get the running data sets:
    _temp = chain.minimum.sortedChiSquareds()
    data  = [ _bf[0] for _bf in _temp if 'prior' not in _bf ]
    # get the total data chi2:
    total_chi2 = 0.0
    chi_squares = chain.minimum.sortedChiSquareds()
    for i in chi_squares:
        if i[0] in data:
            for j in i[1]:
                total_chi2 += j.chisq
    #
    return total_chi2

def print_data_chi2( chain ):
    """
    Print to screen the data decomposition of the best-fit chi square:
    """
    print color_print.green( chain.identifier+':' )
    # protect against no minimum:
    if chain.minimum is None:
        print color_print.warning( 'chain has no minimum' )
        return
    # get the running data sets:
    _temp = chain.minimum.sortedChiSquareds()
    data  = [ _bf[0] for _bf in _temp if 'prior' not in _bf ]
    # print loop:
    chi_squares = chain.minimum.sortedChiSquareds()
    for i in chi_squares:
        if i[0] in data:
            print color_print.bold(i[0])
            for j in i[1]:
                print '    '+j.name+' :', j.chisq
    print color_print.bold( 'Total : '+str(total_data_chi2( chain )) )

def compare_data_chi2( chain1, chain2 ):
    """
    Print to screen the comparison of the data pieces of the best-fit chi square:
    """
    print color_print.green( chain1.identifier+' vs '+chain2.identifier )
    # protect against no minimum:
    if chain1.minimum is None:
        print color_print.warning( 'chain '+chain1.identifier+' has no minimum' )
        return
    if chain2.minimum is None:
        print color_print.warning( 'chain '+chain2.identifier+' has no minimum' )
        return
    # get the running data sets for the first chain:
    _temp  = chain1.minimum.sortedChiSquareds()
    data1  = [ _bf[0] for _bf in _temp if 'prior' not in _bf ]
    # get the running data sets for the second chain:
    _temp  = chain2.minimum.sortedChiSquareds()
    data2  = [ _bf[0] for _bf in _temp if 'prior' not in _bf ]
    # check that they are the same:
    if not data1==data2:
        print color_print.warning( 'the two chains do not have the same data sets' )
        return
    data = data2
    # do the printing:
    chi_squares_1 = dict( chain1.minimum.sortedChiSquareds() )
    chi_squares_2 = dict( chain2.minimum.sortedChiSquareds() )
    # now cycle through the data:
    for _key in chi_squares_1.keys():
        if _key in data:
            print color_print.bold(_key)
            _temp_total = []
            for d1,d2 in zip(chi_squares_1[_key],chi_squares_2[_key]):
                _diff = d1.chisq-d2.chisq
                print '    '+d1.name+' :', str('{}'.format(nice_number(d1.chisq,digits=4))), '-', \
                    str('{}'.format(nice_number(d2.chisq,digits=4))), '=',str('{}'.format(nice_number(_diff,digits=3)))
                _temp_total.append(_diff)
            print '    total :', str('{}'.format(nice_number(np.sum(_temp_total),digits=3)))
    total_difference = total_data_chi2( chain1 )-total_data_chi2( chain2 )
    total_sigma      = from_confidence_to_sigma( scs.chi2.cdf( total_difference, 1 ) )
    print color_print.bold( 'Total : '+str('{}'.format(nice_number( total_difference, digits=3))) )
    print color_print.bold( 'sigma : '+str('{}'.format(nice_number( total_sigma     , digits=3))) )

# ***************************************************************************************

def gaussian_approximation( chain ):
    """
    Get the Gaussian approximation of a chain:
    """
    # get the mean and covariance:
    _mean = chain.samples.setMeans()
    _cov  = chain.samples.cov()
    # get parameter names and labels:
    _param_names  = chain.samples.getParamNames().list()
    _param_labels = [ _n.label for _n in chain.samples.getParamNames().parsWithNames(_param_names) ]
    # initialize the Gaussian distribution:
    gaussian_approx = ggaussian.GaussianND(_mean, _cov, names=_param_names, labels=_param_labels, label='GLM' )
    #
    return gaussian_approx

# ***************************************************************************************

def separate_chains( chain ):
    """
    Gets a list of chains from one multi-chain
    """
    # copy in the chain:
    temp_chain = copy.deepcopy( chain )
    # loop over the chains:
    chainlist = []
    for off1, off2 in zip(chain.samples.chain_offsets[:-1], chain.samples.chain_offsets[1:]):
        _samps = gsamp.MCSamples( ranges      = chain.samples.ranges,
                                  samples     = chain.samples.samples[off1:off2],
                                  weights     = chain.samples.weights[off1:off2],
                                  loglikes    = chain.samples.loglikes[off1:off2],
                                  names       = [ _n.name for _n in chain.samples.getParamNames().names ],
                                  labels      = [ _n.label for _n in chain.samples.getParamNames().names ],
                                  ignore_rows = 0.0
                                  )
        _samps.setParamNames(chain.samples.getParamNames())
        temp_chain.samples = _samps
        chainlist.append(copy.deepcopy(temp_chain))
    #
    return chainlist

# ***************************************************************************************

# run for all chains:
if __name__ == "__main__":
    #
    from import_chains import *
    # import all chains:
    chains = import_chains()
    #
    chain = chains[chains.keys()[0]]
    pass
