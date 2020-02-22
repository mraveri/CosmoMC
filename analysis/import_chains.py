# -*- coding: utf-8 -*-

"""
File that imports a collection of chains for later use.

The import performs various calculations to ensure the quality of the chain and
saves a cache containing the imported chains.
"""

"""
%load_ext autoreload
%autoreload 2
"""

################################################################################
# Initial imports:

from settings  import *
from utilities import *
from chains_utilities import *

################################################################################
# Directories with the chains. All of them will be explored for chains.

chains_dirs = [
                here+'/../0_test_chains',
                ]

################################################################################
# feedback preferences:

feedback = 1
# do not print all chains details:
if feedback<2:
    gsamp.chains.print_load_details = False

################################################################################
# hard coded import parameters:

# 1- Use cache if available, if not create one
use_cache              = True
# 2-
like_tollerance        = 0.005
# 3-
parameter_priors       = False
# 4-
thin_chains            = True
# 5-
thin_tollerance        = 0.001
# 6-
refine_ranges          = True
# 7-
forced_compression     = 0

################################################################################
# Setting for the statistical analysis of the imported chains:

analysis_settings = {'max_corr_2D': u'0.99',
                     'boundary_correction_order': u'0',
                     'converge_test_limit': u'0.95',
                     'smooth_scale_2D': u'0.3',
                     'credible_interval_threshold': u'0.05',
                     'contours': str(from_sigma_to_confidence(1))+' '+\
                                 str(from_sigma_to_confidence(2))+' '+\
                                 str(from_sigma_to_confidence(3))+' '+\
                                 str(from_sigma_to_confidence(4))+' '+\
                                 str(from_sigma_to_confidence(5)),
                     'fine_bins_2D': u'512',
                     'num_bins': u'200',
                     'mult_bias_correction_order': u'0',
                     'fine_bins': u'2048',
                     'num_bins_2D': u'80',
                     'max_scatter_points': u'2000',
                     'range_ND_contour': u'0',
                     'range_confidence': u'0.001',
                     'smooth_scale_1D': u'0.3',
                     'ignore_rows': u'0.3'}

################################################################################
# Helper class that holds the chains and auxiliary informations.

class chain_holder:
    """
    Class that holds a chain and all relevant informations
    """
    # 1- string with chain identifier:
    identifier   = ''
    # 2- string with chain name:
    name         = ''
    # 3- path to the original chain files:
    path         = ''
    # 4- directory of the original chain files:
    dirname      = ''
    # 5- path and root of the chain:
    chain        = ''
    # 6- samples as GetDist files:
    samples      = None
    # 7- GetDist type holding the chain maximum likelihood:
    minimum      = None
    # 8- GetDist type holding the chain maximum likelihood with all fixed params
    full_minimum = None

################################################################################
# Main chain importer:

def import_chains( chains_dir=None, use_cache=use_cache, save_cache=True, analysis_settings=analysis_settings,
                   parameter_priors=parameter_priors, thin_chains=thin_chains, thin_tollerance=thin_tollerance,
                   refine_ranges=refine_ranges, forced_compression=forced_compression, import_max=True ):
    """
    Function that imports all the chains
    """
    # 0) check for cached results:
    if chains_dir is not None:
        chains_dir = make_list(chains_dir)
        if os.path.exists(chains_dir[0]):
            temp_file = chains_dir[0]
        else:
            errmsg = 'WARNING directory %s does not exist, will use cache from current directory'%chains_dir
            print color_print.warning( errmsg )
            temp_file = here+'/import_chains.cache'
    else:
        temp_file    = here+'/import_chains.cache'
    if not os.path.isfile(temp_file):
        temp_file    = here+'/import_chains.cache'
    cache_chains = use_cache and os.path.isfile(temp_file)
    if cache_chains:
        # get the chains from cache:
        print 'Loading the chains cache from: ', temp_file
        dump_file = open(temp_file, 'r')
        #chains = plk.load( dump_file )
        chains = joblib.load( dump_file )
    else:
        # get the chains from file:
        chains = {}
        for chain_dir in chains_dirs:
            for name_temp in sorted( [ f for f in os.listdir( chain_dir ) if '.paramnames' in f ] ):
                if feedback>0:
                    print
                    print color_print.green(  'Importing chain:' ),
                try:
                    # 1- the chain:
                    temp_chain       = chain_holder()
                    temp_chain.name  = ('.').join( name_temp.split('.')[:-1] )
                    temp_chain.path  = chain_dir
                    temp_chain.chain = temp_chain.path +'/'+temp_chain.name
                    if feedback>0: print os.path.relpath( temp_chain.chain, here )
                    temp_chain.dirname    = os.path.basename( temp_chain.path )
                    temp_chain.identifier = temp_chain.dirname+'/'+temp_chain.name
                    temp_chain.samples    = copy.deepcopy( gsamp.loadMCSamples( temp_chain.chain , no_cache = not use_cache, settings = analysis_settings ) )
                    temp_chain.samples.out_dir = temp_chain.path
                    temp_chain.samples.rootdirname = temp_chain.path+'/'+temp_chain.name
                except Exception as e:
                    if feedback>0: print color_print.fail( 'WARNING CHAIN CANNOT BE IMPORTED' )
                    if feedback>0: print e
                    continue
                # 2- the maximum likelihood:
                if import_max:
                    try:
                        minima, full_minima = load_all_minimum_files( temp_chain )
                        if len(minima)==0: raise( ValueError, 'No minimum files')
                        temp_chain.minimum      = copy.deepcopy( minima[ np.argmin( [ _min.logLike for _min in  minima ] ) ] )
                        temp_chain.full_minimum = copy.deepcopy( full_minima[ np.argmin( [ _min.logLike for _min in  minima ] ) ] )
                        # test:
                        if temp_chain.minimum.logLike > temp_chain.samples.getLikeStats().logLike_sample+like_tollerance:
                            if feedback>0: print color_print.warning( 'WARNING best fit is worse than chains best fit' )
                            if feedback>0: print 'minimum: ', temp_chain.minimum.logLike
                            if feedback>0: print 'chains : ', temp_chain.samples.getLikeStats().logLike_sample
                            temp_chain.minimum = None
                        # now exclude parameters that are not in the chain (deleted as fixed):
                        if temp_chain.minimum is not None:
                            _exclude_names = [ _nam for _nam in temp_chain.minimum.list() if _nam not in temp_chain.samples.getParamNames().list() ]
                            _exclude_index = [ temp_chain.minimum.numberOfName(_nam) for _nam in _exclude_names ]
                            temp_chain.minimum.deleteIndices(_exclude_index)
                    except Exception as e:
                        if feedback>0: print color_print.fail( 'WARNING MINIMUM NOT FOUND' )
                        if feedback>1: print e
                # 3- apply additional parameter priors:
                if parameter_priors:
                    try:
                        name   = temp_chain.identifier
                        samps       = copy.deepcopy( temp_chain.samples )
                        param_names = samps.getParamNames()
                        # filter out Nan's:
                        _filter = np.logical_not(np.isnan(samps.samples).any(axis=1))
                        num_new, num_old = np.sum( _filter ), samps.samples.shape[0]
                        if  num_new < num_old:
                            if feedback>0: print '* Nan eliminating ', num_old-num_new, ' samples in ', samps.numrows, '(', int((num_old-num_new)/float(num_old)*100.0),'%)'
                            samps.filter( _filter )
                            samps.updateBaseStatistics()
                        # make sure sigma8 is ok:
                        params = samps.getParams()
                        if 'sigma8' in param_names.list():
                            _filter = (params.sigma8 > 0.0) & (params.sigma8 < 3.0)
                            num_new, num_old = np.sum( _filter ), samps.samples.shape[0]
                            if  num_new < num_old:
                                if feedback>0: print '* sigma8 eliminating ', num_old-num_new, ' samples in ', samps.numrows, '(', int((num_old-num_new)/float(num_old)*100.0),'%)'
                                samps.filter( _filter )
                                samps.updateBaseStatistics()
                        # make sure omegam is ok:
                        params = samps.getParams()
                        if 'omegam' in param_names.list():
                            _filter = (params.omegam < 1.0) & (params.omegam > 0.0) & (np.isfinite( params.omegam ))
                            num_new, num_old = np.sum( _filter ), samps.samples.shape[0]
                            if  num_new < num_old:
                                if feedback>0: print '* omegam eliminating ', num_old-num_new, ' samples in ', samps.numrows, '(', int((num_old-num_new)/float(num_old)*100.0),'%)'
                                samps.filter( _filter )
                                samps.updateBaseStatistics()
                    except Exception as e:
                        if feedback>0: print color_print.fail( 'EXTRA PRIOR FAILED. CHECK RANGES.' )
                        if feedback>1: print e
                    # update:
                    temp_chain.samples = copy.deepcopy( samps )
                # 4- thin the chains:
                if thin_chains:
                    _thin_factor = find_loseless_thin( temp_chain.samples, tollerance=thin_tollerance )
                    # force thinning:
                    if forced_compression>0:
                        _thin_factor = _thin_factor*(forced_compression)
                    if _thin_factor>1:
                        if feedback>0: print color_print.bold( '* Thinning chain by '+str(_thin_factor) )
                        if forced_compression>0:
                            if feedback>0: print color_print.bold( '* Forced compression factor '+str(forced_compression) )
                        # thin separately all the chains:
                        _temptemp_chains = temp_chain.samples.getSeparateChains()
                        for _ch in _temptemp_chains: weighted_thin( _ch, _thin_factor )
                        # rebuild from the thinned chains:
                        temp_chain.samples.chains = _temptemp_chains
                        temp_chain.samples.makeSingle()
                        temp_chain.samples.updateBaseStatistics()
                        del temp_chain.samples.chains
                        temp_chain.samples.chains = None
                    else:
                        if feedback>0: print color_print.bold( '* Not thinning the chains')
                    try:
                        if feedback>0: print '   final R-1 =', '{}'.format(nice_number( temp_chain.samples.getGelmanRubin(), digits=2 ))
                    except Exception as e:
                        if feedback>0: print color_print.fail( 'CANNOT COMPUTE FINAL R-1, CHAIN CANNOT BE IMPORTED' )
                        if feedback>1: print e
                        continue
                # 5- refine ranges:
                if refine_ranges:
                    # get parameters:
                    p = temp_chain.samples.getParams()
                    # initialize dictionary:
                    new_ranges = {}
                    # loop over parameters:
                    for _name in temp_chain.samples.getParamNames().list():
                        _samps = getattr(p, _name)
                        new_ranges[_name] = [np.amin(_samps), np.amax(_samps)]
                    # set it and update:
                    temp_chain.samples.setRanges( new_ranges )
                    temp_chain.samples.updateBaseStatistics()

                # 6- copy:
                chains[ temp_chain.identifier ] = copy.deepcopy(temp_chain)

        # dump to file the cache:
        if save_cache:
            dump_file = open(temp_file, 'w')
            print color_print.green( 'Saving cache to '+temp_file )
            #plk.dump( chains, dump_file, plk.HIGHEST_PROTOCOL )
            joblib.dump( chains, dump_file )
            dump_file.close()

    # return:
    return chains

################################################################################

def list_minimum_files( chain ):
    """
    List all minimum files for a chain:
    """
    # get list of minimum files:
    minimum_files = [ _file for _file in os.listdir( chain.path ) if chain.name+'.minimum' in _file ]
    minimum_files = [ _file for _file in minimum_files if 'minimum' in os.path.splitext( _file )[1] ]
    #
    return sorted( minimum_files )

################################################################################

def load_all_minimum_files( chain ):
    """
    Load all the minimum files existing for a chain:
    """
    minimum_files = list_minimum_files( chain )
    # import all of them:
    minima      = []
    full_minima = []
    for _file in minimum_files:
        if os.path.isfile(chain.chain+'.paramnames'):
            _temp = gtypes.BestFit(fileName=chain.path+'/'+_file, setParamNameFile=chain.chain+'.paramnames', want_fixed=False )
            minima.append( copy.deepcopy(_temp) )
            _temp = gtypes.BestFit(fileName=chain.path+'/'+_file, setParamNameFile=chain.chain+'.paramnames', want_fixed=True )
            full_minima.append( copy.deepcopy(_temp) )
        else:
            _temp = gtypes.BestFit(fileName=chain.path+'/'+_file, want_fixed=False )
            minima.append( copy.deepcopy(_temp) )
            _temp = gtypes.BestFit(fileName=chain.path+'/'+_file, want_fixed=True )
            full_minima.append( copy.deepcopy(_temp) )
    #
    return minima, full_minima

################################################################################

def order_minimum_files( chain ):
    """
    Orders minimum files, the best one gets renamed .minimum, the other are numbered
    """
    def _extension(name):
        return os.path.splitext( name )[1]
    # get list of minimum files:
    minimum_files = list_minimum_files( chain )
    if len(minimum_files)==0:
        return
    # import all of them:
    minima, full_minima = load_all_minimum_files( chain )
    # get the best fit likelihood:
    best_fits = [ _min.logLike for _min in minima ]
    # get its index:
    best_index = np.argmin( best_fits )
    # if .minimum is already the best then return:
    if _extension( minimum_files[best_index] ) == '.minimum': return
    # move minimum file to temporary name:
    if os.path.isfile( chain.chain+'.minimum' ):
        os.rename( chain.chain+'.minimum', chain.chain+'.minimum_temp' )
    if os.path.isfile( chain.chain+'.minimum.inputparams' ):
        os.rename( chain.chain+'.minimum.inputparams', chain.chain+'.minimum_temp.inputparams' )
    if os.path.isfile( chain.chain+'.minimum.theory_cl' ):
        os.rename( chain.chain+'.minimum.theory_cl', chain.chain+'.minimum_temp.theory_cl' )
    # now move best minimum to .minimum:
    if os.path.isfile( chain.path+'/'+minimum_files[best_index] ):
        os.rename( chain.path+'/'+minimum_files[best_index], chain.chain+'.minimum' )
    if os.path.isfile( chain.path+'/'+minimum_files[best_index]+'.inputparams' ):
        os.rename( chain.path+'/'+minimum_files[best_index]+'.inputparams', chain.chain+'.minimum.inputparams' )
    if os.path.isfile( chain.path+'/'+minimum_files[best_index]+'.theory_cl' ):
        os.rename( chain.path+'/'+minimum_files[best_index]+'.theory_cl', chain.chain+'.minimum.theory_cl' )
    # now finish swapping:
    if os.path.isfile( chain.chain+'.minimum_temp' ):
        os.rename( chain.chain+'.minimum_temp', chain.path+'/'+minimum_files[best_index] )
    if os.path.isfile( chain.chain+'.minimum_temp.inputparams' ):
        os.rename( chain.chain+'.minimum_temp.inputparams', chain.path+'/'+minimum_files[best_index]+'.inputparams' )
    if os.path.isfile( chain.chain+'.minimum_temp.theory_cl' ):
        os.rename( chain.chain+'.minimum_temp.theory_cl', chain.path+'/'+minimum_files[best_index]+'.theory_cl' )

################################################################################

def print_minimum_info( chains_dir=chains_dirs ):
    """
    Function that prints infos on the minimum files:
    """
    for chain_dir in chains_dirs:
        for name_temp in sorted( [ f for f in os.listdir( chain_dir ) if '.paramnames' in f ] ):
            if feedback>0:
                print
                print color_print.green(  'Chain:' ),
            # 1- get basic info on the chain:
            try:
                temp_chain       = chain_holder()
                temp_chain.name  = ('.').join( name_temp.split('.')[:-1] )
                temp_chain.path  = chain_dir
                temp_chain.chain = temp_chain.path +'/'+temp_chain.name
                if feedback>0: print os.path.relpath( temp_chain.chain, here )
                temp_chain.dirname    = os.path.basename( temp_chain.path )
                temp_chain.identifier = temp_chain.dirname+'/'+temp_chain.name
            except Exception as e:
                if feedback>0: print color_print.fail( 'FAILED:' )
                if feedback>1: print e
            # 2- get the maximum likelihood:
            try:
                # get minima:
                minima, full_minima = load_all_minimum_files( temp_chain )
                if len(minima)==0: raise( ValueError, 'No minimum files')
                # get list of minimum files:
                minimum_files = [ _file for _file in os.listdir( temp_chain.path ) if temp_chain.name in _file and 'minimum' in _file ]
                minimum_files = [ _file for _file in minimum_files if 'minimum' in os.path.splitext( _file )[1] ]
                # result table:
                table = format_table( zip( sorted(minimum_files), [ round(_min.logLike,2) for _min in minima ] ), traspose=False)
                #
                for line in table: print '    '+line
            except Exception as e:
                if feedback>0: print color_print.fail( 'WARNING MINIMUM NOT FOUND' )
                if feedback>1: print e

################################################################################
# If the file is directly called import all the chains and create the cache
# This could contain some command line interface to facilitate some tasks.

if __name__ == "__main__":
    # import chains:
    chains = import_chains( chains_dir=chains_dirs, use_cache=False, save_cache=True, analysis_settings=analysis_settings )
    #
    exit()
