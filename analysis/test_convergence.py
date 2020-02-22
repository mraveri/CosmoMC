# -*- coding: utf-8 -*-

"""
Simple file to test convergence of the chains
"""

from settings import *
from import_chains import *

# some feedback:
print color_print.bold( '**********************************************************' )
print color_print.bold( '** Testing convergence of the chains                    **' )
print color_print.bold( '**********************************************************' )

# results directory:
out_dir = results_dir+'/convergence'
if not os.path.exists(out_dir): os.mkdir(out_dir)

# set up feedback:
if __name__ == "__main__":
    sys.stdout = Logger(out_dir+'/log.txt')

# get chains:
chains = import_chains( chains_dir=chains_dirs )

# cycle through chains:
for name in sorted(chains.keys()):
    # get the chain:
    ch       = chains[name]
    _samples = ch.samples
    # print feedback:
    print color_print.bold( 'Doing convergence and stat tests on: '+ch.identifier )
    # check output folder:
    out_folder = out_dir+'/'+ch.dirname
    if not os.path.exists(out_folder): os.mkdir(out_folder)
    # write covariance:
    _samples.writeCovMatrix(filename=out_folder+'/'+ch.name+'.cov')
    # write correlation:
    _samples.writeCorrelationMatrix(filename=out_folder+'/'+ch.name+'.corr')
    # write marginal statistics:
    _samples.getMargeStats().saveAsText( out_folder+'/'+ch.name+'.margestats' )
    # write global likelihood stats:
    _samples.getLikeStats().saveAsText( out_folder+'/'+ch.name+'.likestats')
    # do convergence diagnostics:
    _samples.getConvergeTests( writeDataToFile=True, filename=out_folder+'/'+ch.name+'.converge', feedback=False)
    _R = _samples.GelmanRubin
    print color_print.green( 'R = '+str('{}'.format(nice_number( _R, digits = 2 ))) )
