# -*- coding: utf-8 -*-

"""
Creates the parameters files to run the mean and the maximum likelihood search
"""
from settings  import *
from utilities import *
from import_chains import *

# some feedback:
print color_print.bold( '**********************************************************' )
print color_print.bold( '** Generating parameter files                           **' )
print color_print.bold( '**********************************************************' )

# import all chains forcing update (it is important to excluded the cached results as the ranges will be off):
chains = import_chains( use_cache=False, save_cache=False, thin_chains=False, refine_ranges=False )

# header:
header = ''

# define the parameter for which we want the mean:
best_fit_use_mean = []
force_mean        = False

print
print color_print.green( 'Preparing parameter files' )
print

# cycle over the chains:
for name in sorted(chains.keys()):
    chain = chains[name]
    #
    print color_print.bold( 'Doing chain: '+chain.identifier )
    # get index of running and derived parameters:
    derived_array = [ temp_name.isDerived for temp_name in chain.samples.getParamNames().names ]
    running_array = np.logical_not( derived_array )
    derived_names = np.array( chain.samples.getParamNames().list() )[derived_array]
    running_names = np.array( chain.samples.getParamNames().list() )[running_array]
    # save the covariance:
    cov_name = os.path.basename(chain.path)+'/'+chain.name+'.covmat'
    chain.samples.writeCovMatrix( filename=chain.path+'/'+chain.name+'.covmat' )
    # get the mean and best fit:
    margestats = chain.samples.getMargeStats()
    likestats  = chain.samples.getLikeStats()
    # write the parameter file for sampling:
    param_outfile = chain.path+'/'+chain.name+'.inputrange'
    if not os.path.exists(os.path.dirname( param_outfile )): os.mkdir(os.path.dirname( param_outfile ))
    #
    param_file    = open( param_outfile, mode='w' )
    param_file.write(header+'\n')
    for _num, _name in enumerate(running_names):
        # compute:
        # mean value:
        _bf_value   = margestats.parWithName(_name).mean
        # best fit of the chains:
        _bf_value   = likestats.parWithName(_name).bestfit_sample
        # previous best fit:
        if chain.minimum is not None:
            _bf_value = chain.minimum.parWithName(_name).best_fit
        # 1 sigma range:
        _low  = min( margestats.parWithName(_name).limits[0].lower, _bf_value )
        _up   = max( margestats.parWithName(_name).limits[0].upper, _bf_value )
        # full range:
        _full_low  = min( chain.samples.ranges.getLower(_name), _bf_value )
        _full_up   = max( chain.samples.ranges.getUpper(_name), _bf_value )
        # Gaussian error:
        _err = margestats.parWithName(_name).err
        # proposer and initial spread:
        start_width   = _err/1.e7
        propose_width = _err
        # write out:
        string = 'param['+str(_name)+'] = '+str(_bf_value)+' '+str(_full_low)+' '+str(_full_up)+' '+str(start_width)+' '+str(propose_width)+'\n'
        param_file.write( string )
    param_file.write( 'propose_matrix='+cov_name+'\n' )
    param_file.close()

    # write the parameter file for maximizer:
    param_outfile = chain.path+'/'+chain.name+'.minimizer_inputrange'
    if not os.path.exists(os.path.dirname( param_outfile )): os.mkdir(os.path.dirname( param_outfile ))
    #
    param_file    = open( param_outfile, mode='w' )
    param_file.write(header+'\n')
    for _num, _name in enumerate(running_names):
        # compute:
        # mean value:
        _mean_value = margestats.parWithName(_name).mean
        # best fit of the chains:
        _bf_value   = likestats.parWithName(_name).bestfit_sample
        # use mean if wanted:
        if _name in best_fit_use_mean or force_mean:
            _bf_value = _mean_value
        # 1 sigma range:
        _low  = min( margestats.parWithName(_name).limits[0].lower, _bf_value )
        _up   = max( margestats.parWithName(_name).limits[0].upper, _bf_value )
        # full range:
        _full_low  = min( chain.samples.ranges.getLower(_name), _bf_value )
        _full_up   = max( chain.samples.ranges.getUpper(_name), _bf_value )
        # Gaussian error:
        _err = margestats.parWithName(_name).err
        # proposer and initial spread:
        start_width   = _err
        propose_width = _err
        # write out:
        string = 'param['+str(_name)+'] = '+str(_bf_value)+' '+str(_full_low)+' '+str(_full_up)+' '+str(start_width)+' '+str(propose_width)+'\n'
        param_file.write( string )
    param_file.write( 'propose_matrix='+cov_name+'\n' )
    param_file.close()

    # write the parameter file for best fit to check the likelihood:
    param_outfile = chain.path+'/'+chain.name+'.mean_inputrange'
    if not os.path.exists(os.path.dirname( param_outfile )): os.mkdir(os.path.dirname( param_outfile ))
    #
    param_file    = open( param_outfile, mode='w' )
    param_file.write(header+'\n')
    for _num, _name in enumerate(running_names):
        # mean value:
        _mean_value = margestats.parWithName(_name).mean
        if chain.minimum is not None:
            _mean_value = chain.minimum.parWithName(_name).best_fit
        # full range:
        _full_low  = min( chain.samples.ranges.getLower(_name), _mean_value )
        _full_up   = max( chain.samples.ranges.getUpper(_name), _mean_value )
        # Gaussian error:
        _err = margestats.parWithName(_name).err
        # write out:
        string = 'param['+str(_name)+'] = '+str(_mean_value)+' '+str(_full_low)+' '+str(_full_up)+' '+str(_err)+' '+str(_err)+'\n'
        param_file.write( string )
    #param_file.write( 'test_output_root='+chain.dirname+'/'+chain.name+'.mean\n' )
    param_file.write( 'propose_matrix=\n' )
    param_file.close()

# exit if the file is directly called:
if __name__ == "__main__":
    exit()
