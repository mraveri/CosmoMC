# -*- coding: utf-8 -*-

"""
Simple file to test convergence of the chains
"""

from settings import *
from import_chains import *
from chains_copy_utilities import *

# some feedback:
print color_print.bold( '**********************************************************' )
print color_print.bold( '** Generating CAMB parameters                           **' )
print color_print.bold( '**********************************************************' )

# get chains:
chains = import_chains( )
# define output directory:
out_dir = here+'/camb_best_fit/parameters'
if not os.path.exists(out_dir): os.mkdir(out_dir)

# cycle through chains:
for name in sorted(chains.keys()):
    # get the chain:
    ch = chains[name]
    # check that the chain has best fit:
    if ch.full_minimum is None:
        continue
    # split copies if needed:
    chs = split_copies(ch)
    for _ch in chs:
        # start the calculation:
        try:
            print color_print.bold( 'Doing chain: '+_ch.identifier )
            # write the parameter file for sampling:
            param_outfile = out_dir+'/'+_ch.name+'.best_parameters'
            if not os.path.exists(os.path.dirname( param_outfile )): os.mkdir(os.path.dirname( param_outfile ))
            # get the minimum:
            _minimum = _ch.full_minimum
            # open the file and write header:
            param_file = open( param_outfile, mode='w' )
            header     = '# Parameter file for CAMB with the best fit parameters for the _chain '+_ch.identifier
            param_file.write(header+'\n\n')
            # get base LCDM parameters:
            param_file.write( 'hubble = '+str(_minimum.parWithName('H0').best_fit)+'\n' )
            param_file.write( 'ombh2  = '+str(_minimum.parWithName('omegabh2').best_fit)+'\n' )
            param_file.write( 'omch2  = '+str(_minimum.parWithName('omegach2').best_fit)+'\n' )
            param_file.write( 'omnuh2 = '+str(_minimum.parWithName('omeganuh2').best_fit)+'\n' )
            param_file.write( 'helium_fraction = '+str(_minimum.parWithName('yheused').best_fit)+'\n' )
            param_file.write( 'scalar_amp(1) = '+str(_minimum.parWithName('A').best_fit*10**(-9.))+'\n' )
            param_file.write( 'scalar_spectral_index(1) = '+str(_minimum.parWithName('ns').best_fit)+'\n' )
            param_file.write( 're_optical_depth = '+str(_minimum.parWithName('tau').best_fit)+'\n' )
            param_file.write( '\n' )
            # add common parameters:
            param_file.write( '\nDEFAULT(base_params.ini)\n' )
            # close the file:
            param_file.close()
        except Exception as e:
            if feedback>0: print color_print.fail( 'WARNING' )
            if feedback>0: print e
            continue
