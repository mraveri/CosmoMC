# -*- coding: utf-8 -*-

"""
Monitors the running of the chains.
"""

# 1- general import:

from settings  import *
from utilities import *
import subprocess as subprocess
import argparse

# 2- parse command line options:
parser = argparse.ArgumentParser(description='Shows the convergence of the chains')
parser.add_argument('folder', nargs='*', help='folders with the chains')
parser.add_argument("--verbose", help="increase output verbosity",action="store_true")
args = parser.parse_args()

# 3- get the running chains if on the cluster:
try:
    # get the squeue output:
    result = subprocess.check_output(['squeue','--format="%.18i %.9P %.30j %.8u %.1T %.10M %.9l %.6D %R"'])
    # get the lines:
    result = result.split('\n')
    # get the split lines:
    _temp  = []
    for res in result:
        _temp_res = [ _t.replace(" ", "") for _t in res.split(' ') ]
        _temp_res = filter(None, _temp_res)
        _temp.append(_temp_res)
    _temp = filter(None, _temp)
    # prepare list of running jobs:
    running_jobs = copy.deepcopy(_temp)
    _running_on_cluster = True
except:
    # in case this fails we proceed as not running on cluster:
    running_jobs = None
    _running_on_cluster = False

# 4- print some feedback:
print color_print.bold( '**********************************************************' )
if _running_on_cluster:
    print color_print.bold( '** Chains monitor (on cluster)                          **' )
else:
    print color_print.bold( '** Chains monitor                                       **' )
print color_print.bold( '**********************************************************' )

# 5- define the helper to get running chains:
def _helper_is_running( jobs, name ):
    # initial check:
    if jobs is None: return
    if name is None: return
    # cycle through the jobs query:
    _in_queue = False
    status    = ''
    for _line in jobs:
        if name in _line:
            _in_queue = True
            if 'R' in _line:
                status = 'R'
            if 'P' in _line:
                status = 'Q'
            return _in_queue, status
    return _in_queue, status

# 6- cycle over chain dirs:
for _chain_dir in args.folder:
    print color_print.bold( 'Monitoring chains directory: '+_chain_dir )
    for _converge_file in sorted( [ _file for _file in os.listdir(_chain_dir) if 'converge_stat' in _file ] ):
        _file  = open(_chain_dir+'/'+_converge_file)
        _lines = _file.read().split('\n')
        _root = _converge_file.split('.')[0]
        if _lines[1]=='Done':
            if not args.verbose: continue
        def helper_file_len(fname):
            with open(fname) as f:
                for i, l in enumerate(f):
                    pass
            return i
        _samples = []
        _ind     = 1
        while os.path.isfile(_chain_dir+'/'+_root+'_'+str(_ind)+'.txt'):
            _samples.append( helper_file_len(_chain_dir+'/'+_root+'_'+str(_ind)+'.txt'))
            _ind += 1
        # get if the chain is running:
        _chain_is_running, status =  _helper_is_running( running_jobs, _root )
        # print the feedback:
        print color_print.green( '* '+_root+' R = '+str('{}'.format(nice_number(float(_lines[0]),digits=3))) ),
        if _lines[1]=='Done':
            print color_print.bold('(DONE)'),
            print 'samples: ',sum(_samples)
            continue
        if _chain_is_running:
            print color_print.bold('('+status+')')
        else:
            print
        print '  samples      : ', _samples
        print '  total samples: ',sum(_samples)
        _samples = np.array(_samples)
        print '  mean samples : ',int(np.mean(_samples)), 'variance: ', int(np.sqrt(np.var(_samples)))

# exit if the file is directly called:
if __name__ == "__main__":
    pass
    exit()
