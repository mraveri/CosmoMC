# -*- coding: utf-8 -*-

"""
Some chains utilities to be used with chains with duplicate parameters
"""

from settings  import *
from utilities import *
from import_chains import *
from tension_estimators import *

"""
For testing purposes
from import_chains import *
# directory with chains:
chains_dir = here+'/import_chains_sn.cache'
# import chains:
chains     = import_chains(chains_dir=chains_dir)
"""

# ***************************************************************************************

def split_copies( chain ):
    """
    Split a chain in different copies. We assume that all the copies have parameter
    names that end in _numcopy.
    chain = copy.deepcopy(chains['3_Planck2015_chains/3_plc15_TTTE_1copy'])
    """
    # get the parameter names and the number of copies:
    total_paramnames = chain.samples.getParamNames().list()
    copy_paramnames  = []
    for i in xrange(100):
        param_names = []
        for name in total_paramnames:
            if name[-2:]=='_'+str(i+1):
                param_names.append(name[:-2])
        if len(param_names)>0:
            copy_paramnames.append( copy.deepcopy(param_names) )
    # get the number of copies:
    num_copies = len(copy_paramnames)
    # check that there is at least one copy:
    if num_copies==0:
        return [chain]
    # check that all copies have the same parameter names:
    for _ind,_temp in enumerate(copy_paramnames):
        if not _temp==copy_paramnames[0]:
            raise( ValueError, 'Param names for copy '+str(_ind)+' are not the same as the first copy' )
    # since they are now all the same just use one:
    copy_paramnames = copy_paramnames[0]
    # cycle and create the new chains:
    copy_chains = []
    for _ind in xrange(num_copies):
        num_copy = _ind+1
        # 1) create the new chain holder with initialization:
        temp_chain            = chain_holder()
        temp_chain.name       = chain.name+'_copy'+str(num_copy)
        temp_chain.path       = chain.path
        temp_chain.chain      = temp_chain.path +'/'+temp_chain.name
        temp_chain.dirname    = os.path.basename( temp_chain.path )
        temp_chain.identifier = temp_chain.dirname+'/'+temp_chain.name
        # 2) get the loglikes and weights:
        _loglikes = copy.deepcopy( chain.samples.loglikes )
        _weights  = copy.deepcopy( chain.samples.weights )
        # get the parameter names:
        _paramnames = [ _nam+'_'+str(num_copy) for _nam in copy_paramnames ]
        # get the samples:
        _indexes  = [ chain.samples.getParamNames().list().index(par_name) for par_name in  _paramnames ]
        _samples  = copy.deepcopy( chain.samples.samples[:,_indexes] )
        # get the settings (forcing no burnin as it is already removed):
        _temp_settings = copy.deepcopy(analysis_settings)
        _temp_settings['ignore_rows']='0.0'
        # get the ranges:
        _ranges = {}
        for _nam,_cnam in zip(_paramnames,copy_paramnames):
            _ranges[_cnam] = [chain.samples.ranges.getLower(_nam), chain.samples.ranges.getUpper(_nam)]
        # get latex labels:
        _labels = [ _nam.label[:-7] for _nam in chain.samples.getParamNames().parsWithNames( _paramnames ) ]
        # initialize the samples:
        temp_chain.samples = gsamp.MCSamples( loglikes = _loglikes,
                                              weights  = _weights,
                                              samples  = _samples,
                                              settings = _temp_settings,
                                              ranges   = _ranges,
                                              names    = copy_paramnames,
                                              labels   = _labels )
        # set a couple of getdist things:
        temp_chain.samples.name_tag = temp_chain.name
        temp_chain.samples.updateBaseStatistics()
        # set distinction between base and derived parameters:
        for _nam in temp_chain.samples.getParamNames().parsWithNames(temp_chain.samples.getParamNames().list()):
            _nam.isDerived = chain.samples.getParamNames().parWithName(_nam.name+'_'+str(num_copy)).isDerived
        # 3) split the minimum:
        if chain.minimum is not None:
            _temp_minimum    = copy.deepcopy(chain.minimum)
            # delete the parameters of the other copy:
            _exclude_indexes = [ _temp_minimum.numberOfName(_nam) for _nam in total_paramnames if _nam not in  _paramnames ]
            _temp_minimum.deleteIndices(_exclude_indexes)
            # rename the names:
            for name, paramname, label in zip(_temp_minimum.names, copy_paramnames, _labels):
                name.name  = paramname
                name.label = label
            # save:
            temp_chain.minimum = copy.deepcopy( _temp_minimum )
        # 4) split the full minimum:
        if chain.full_minimum is not None:
            _temp_minimum    = copy.deepcopy(chain.full_minimum)
            # delete the parameters of the other copy:
            _exclude_indexes = [ _temp_minimum.numberOfName(_nam) for _nam in _temp_minimum.list() if _nam[-2:]!='_'+str(num_copy) ]
            _temp_minimum.deleteIndices(_exclude_indexes)
            for _nam in _temp_minimum.names:
                _nam.name  = _nam.name[:-2]
                _nam.label = _nam.label[:-7]
            # save:
            temp_chain.full_minimum = copy.deepcopy( _temp_minimum )
        # finalize:
        copy_chains.append( copy.deepcopy(temp_chain) )
    # return:
    return copy_chains

# ***************************************************************************************

def difference_chain( chain ):
    """
    Get the chain with the parameter differences
    chain = copy.deepcopy(chains['5_SN_chains/2p2_SNC_zcut0p3_abs'])
    """
    # get the parameter names and the number of copies:
    total_paramnames = chain.samples.getParamNames().list()
    copy_paramnames  = []
    for i in xrange(100):
        param_names = []
        for name in total_paramnames:
            if name[-2:]=='_'+str(i+1):
                param_names.append(name[:-2])
        if len(param_names)>0:
            copy_paramnames.append( copy.deepcopy(param_names) )
    # get the number of copies:
    num_copies = len(copy_paramnames)
    # test:
    if num_copies!=2:
        raise ValueError('Parameter difference requires only two copies.')
    # check that all copies have the same parameter names:
    for _ind,_temp in enumerate(copy_paramnames):
        if not _temp==copy_paramnames[0]:
            raise( ValueError, 'Param names for copy '+str(_ind)+' are not the same as the first copy' )
    # since they are now all the same just use one:
    copy_paramnames = copy_paramnames[0]
    # now write the parameter difference chain:
    temp_chain            = chain_holder()
    temp_chain.name       = chain.name+'_difference'
    temp_chain.path       = chain.path
    temp_chain.chain      = temp_chain.path +'/'+temp_chain.name
    temp_chain.dirname    = os.path.basename( temp_chain.path )
    temp_chain.identifier = temp_chain.dirname+'/'+temp_chain.name
    # get the loglikes and weights:
    _loglikes = copy.deepcopy( chain.samples.loglikes )
    _weights  = copy.deepcopy( chain.samples.weights )
    # get the parameter names:
    _paramnames_1 = [ _nam+'_1' for _nam in copy_paramnames ]
    _paramnames_2 = [ _nam+'_2' for _nam in copy_paramnames ]
    # get the samples:
    _indexes_1  = [ chain.samples.getParamNames().list().index(par_name) for par_name in  _paramnames_1 ]
    _indexes_2  = [ chain.samples.getParamNames().list().index(par_name) for par_name in  _paramnames_2 ]
    _samples_1  = copy.deepcopy( chain.samples.samples[:,_indexes_1] )
    _samples_2  = copy.deepcopy( chain.samples.samples[:,_indexes_2] )
    _difference_samples = _samples_1-_samples_2
    # get the settings (forcing no burnin as it is already removed):
    _temp_settings = copy.deepcopy(analysis_settings)
    _temp_settings['ignore_rows']='0.0'
    # get the names and labels:
    param_names  = [ 'delta_'+_nam for _nam in copy_paramnames ]
    param_labels = [ '\\Delta '+_nam.label[:-7] for _nam in chain.samples.getParamNames().parsWithNames( _paramnames_1 ) ]
    # get the ranges:
    _ranges = {}
    for _nam,_min,_max in zip( param_names, np.amin(_difference_samples,axis=0), np.amax(_difference_samples,axis=0) ):
        _ranges[_nam] = [_min,_max]
    # initialize the samples:
    temp_chain.samples = gsamp.MCSamples( loglikes = _loglikes,
                                          weights  = _weights,
                                          samples  = _difference_samples,
                                          settings = _temp_settings,
                                          ranges   = _ranges,
                                          names    = param_names,
                                          labels   = param_labels )
    # set a couple of getdist things:
    if hasattr( chain.samples, 'chain_offsets' ):
        temp_chain.samples.chain_offsets = chain.samples.chain_offsets
    temp_chain.samples.name_tag = temp_chain.name
    temp_chain.samples.updateBaseStatistics()
    temp_chain.samples.deleteFixedParams()
    # set distinction between base and derived parameters:
    for _nam in temp_chain.samples.getParamNames().parsWithNames(temp_chain.samples.getParamNames().list()):
        _temp_name = _nam.name.replace('delta_','')+'_1'
        _nam.isDerived = chain.samples.getParamNames().parWithName(_temp_name).isDerived
    # set the minimum:
    if chain.minimum is not None:
        temp_chain.minimum = None
    if chain.full_minimum is not None:
        temp_chain.full_minimum = None
    # return:
    return copy.deepcopy( temp_chain )

# ***************************************************************************************

def difference_chain_uncorrelated( chain_1, chain_2, boost=1, num_split=8 ):
    """
    Get the chain with the parameter differences given two chains
    chain_1 = copy.deepcopy(chains['5_SN_chains/1p2_SN1_zcut0p3_abs'])
    chain_2 = copy.deepcopy(chains['5_SN_chains/1p2_SN2_zcut0p3_abs'])
    boost   = 1
    """
    # get the parameter names:
    _pname_1 = chain_1.samples.getParamNames().list()
    _pname_2 = chain_2.samples.getParamNames().list()
    # get the common names:
    _param_names = [ _p for _p in _pname_1 if _p in _pname_2 ]
    _num_params  = len(_param_names)
    # now write the parameter difference chain:
    temp_chain            = chain_holder()
    temp_chain.name       = chain_1.name+chain_2.name+'_diff'
    temp_chain.path       = chain_1.path
    temp_chain.chain      = chain_1.path +'/'+temp_chain.name
    temp_chain.dirname    = os.path.basename( temp_chain.path )
    temp_chain.identifier = temp_chain.dirname+'/'+temp_chain.name
    # get the loglikes and weights:
    _weights_1   = chain_1.samples.weights
    _weights_2   = chain_2.samples.weights
    _num_samps_1 = len(_weights_1)
    _num_samps_2 = len(_weights_2)
    _num_samples = min(_num_samps_1,_num_samps_2)
    _indexes_1  = [ chain_1.samples.getParamNames().list().index(par_name) for par_name in  _param_names ]
    _indexes_2  = [ chain_2.samples.getParamNames().list().index(par_name) for par_name in  _param_names ]
    # get samples, weights and loglikes:
    _weights            = []
    _loglikes           = []
    _difference_samples = []
    for ind in xrange(boost):
        base_ind = int(float(ind)/float(boost)*_num_samps_2)
        _indexes = range(base_ind, base_ind+_num_samples)
        _weights.append( _weights_1[:_num_samples]*np.take(_weights_2,_indexes,mode='wrap') )
        _loglikes.append( chain_1.samples.loglikes[:_num_samples]-np.take(chain_2.samples.loglikes,_indexes,mode='wrap') )
        _samples_1 = copy.deepcopy( chain_1.samples.samples[:_num_samples,_indexes_1] )
        _samples_2 = copy.deepcopy( chain_2.samples.samples[:,_indexes_2] )
        _difference_samples.append( _samples_1-np.take(_samples_2,_indexes,axis=0,mode='wrap') )
    _weights            = np.array(_weights).reshape((_num_samples*boost))
    _loglikes           = np.array(_loglikes).reshape((_num_samples*boost))
    _difference_samples = np.array(_difference_samples).reshape((_num_samples*boost,_num_params))
    # now thin by boost/2:
    _thin_factor        = max(1,boost//2)
    _weights            = _weights[::_thin_factor]
    _loglikes           = _loglikes[::_thin_factor]
    _difference_samples = _difference_samples[::_thin_factor,:]
    # get the settings (forcing no burnin as it is already removed):
    _temp_settings = copy.deepcopy(analysis_settings)
    _temp_settings['ignore_rows']='0.0'
    # get the names and labels:
    param_names  = [ 'delta_'+_nam for _nam in _param_names ]
    param_labels = [ '\\Delta '+_nam.label for _nam in chain_1.samples.getParamNames().parsWithNames( _param_names ) ]
    # get the ranges:
    _ranges = {}
    for _nam,_min,_max in zip( param_names, np.amin(_difference_samples,axis=0), np.amax(_difference_samples,axis=0) ):
        _ranges[_nam] = [_min,_max]
    # initialize the samples:
    temp_chain.samples = gsamp.MCSamples( loglikes = _loglikes,
                                          weights  = _weights,
                                          samples  = _difference_samples,
                                          settings = _temp_settings,
                                          ranges   = _ranges,
                                          names    = param_names,
                                          labels   = param_labels )
    # now set the indexes to split the chain if needed:
    temp_chain.samples.chain_offsets = [ i*len(_loglikes)/num_split for i in xrange(num_split) ]+[len(_loglikes)]
    # set a couple of getdist things:
    temp_chain.samples.name_tag = temp_chain.name
    temp_chain.samples.updateBaseStatistics()
    temp_chain.samples.deleteFixedParams()
    # set distinction between base and derived parameters:
    for _nam in temp_chain.samples.getParamNames().parsWithNames(temp_chain.samples.getParamNames().list()):
        _temp_name = _nam.name.replace('delta_','')
        _nam.isDerived = chain_1.samples.getParamNames().parWithName(_temp_name).isDerived
    # set the minimum:
    if chain_1.minimum is not None and chain_2.minimum is not None:
        temp_chain.minimum = None
    if chain_1.full_minimum is not None and chain_2.full_minimum is not None:
        temp_chain.full_minimum = None
    # return:
    return copy.deepcopy( temp_chain )

# ***************************************************************************************

def find_common_names_with_copies( Split_paramnames, Joint_paramnames ):
    """
    Function that finds common names in chains when there are parameter copies
    One chain is the Split (S) and the other the Joint (J)

    For testing purpose:
    chain_S = copy.deepcopy( chains['3_Planck2015_chains/3_plc15_TTEE_1copy'] )
    chain_J = copy.deepcopy( chains['3_Planck2015_chains/4_plc15_TTEE_joint'] )
    """
    # split and joint common parameter names:
    common_split = []
    common_joint = []
    for i, _Jpar in enumerate(Joint_paramnames):
        for j, _Spar in enumerate(Split_paramnames):
            # check if joint name is part of split parameter name:
            if _Jpar in _Spar:
                # do not double-count parameters in split:
                if _Spar not in common_split:
                    common_split.append(_Spar)
                # do not double-count parameters in joint:
                if _Jpar not in common_joint:
                    common_joint.append(_Jpar)
    # return lists of joint and split parameter names:
    return common_split, common_joint

# ***************************************************************************************

def find_common_names_between_copies( copy_chain_names, chain_1_names, chain_2_names ):
    """
    Function that finds common names in chains when there are parameter copies
    One chain is the Split (S) and the other the Joint (J)

    For testing purpose:
    copy_chain = copy.deepcopy( chains['3_Planck2015_chains/3_plc15_TTEE_1copy'] )
    chain_1 = copy.deepcopy( chains['3_Planck2015_chains/1_plc15_TT'] )
    chain_2 = copy.deepcopy( chains['3_Planck2015_chains/1_plc15_EE'] )
    copy_chain_names = get_running_names(copy_chain)
    chain_1_names = get_running_names(chain_1)
    chain_2_names = get_running_names(chain_2)
    """
    # get names of the two copies:
    names_copy1 = get_copy_param_names( copy_chain_names, use_copy=1 )
    names_copy2 = get_copy_param_names( copy_chain_names, use_copy=2 )
    # find common names:
    common_names_copy1 = []
    common_names_copy2 = []
    for i, _copy1_name in enumerate(names_copy1):
        # if copy index exists, remove it:
        if _copy1_name[-2] == '_':
            _copy1_name_noindx = _copy1_name[:-2]
        else:
            _copy1_name_noindx = _copy1_name
        for j, _copy2_name in enumerate(names_copy2):
            # if copy index exists, remove it:
            if _copy2_name[-2] == '_':
                _copy2_name_noindx = _copy2_name[:-2]
            else:
                _copy2_name_noindx = _copy2_name
            # keep name if it is common in the two copies and single chains
            if _copy1_name_noindx == _copy2_name_noindx:
                if (_copy1_name_noindx in chain_1_names and _copy1_name_noindx in chain_2_names):
                    common_names_copy1.append(_copy1_name_noindx)
                if (_copy2_name_noindx in chain_2_names and _copy2_name_noindx in chain_1_names):
                    common_names_copy2.append(_copy2_name_noindx)
    # return lists of common names:
    return common_names_copy1, common_names_copy2

# ***************************************************************************************

def get_copy_param_names( names, use_copy=1 ):
    """
    Function that finds parameters from a specified copy

    For testing purpose:
    chains = import_chains(chains_dir='/media/georgez/Data/Datasets/planck_analysis')
    chain = copy.deepcopy( chains['3_Planck2015_chains/3_plc15_TTEE_1copy'] )
    """
    # look for parameters of the specified copy:
    _names_copy = []
    for i, _param in enumerate(names):
        # if name ends in copy index keep it:
        if _param[-2:]=='_'+str(use_copy):
            _names_copy.append(_param)
        # also keep parameters that are not duplicated:
        if _param[-2]!='_':
            _names_copy.append(_param)
    # return list of the names:
    return _names_copy
