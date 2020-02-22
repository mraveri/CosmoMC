# -*- coding: utf-8 -*-

"""
Prints and orders best fit files:
"""

from settings  import *
from utilities import *
from chains_utilities import *
from import_chains import *

def print_order_minimum_info( chains_dir=chains_dirs, order=False ):
    """
    Function that prints infos on the minimum files:
    """
    for chain_dir in chains_dirs:
        # get the name of the minmum files:
        all_files    = [ f for f in os.listdir( chain_dir ) ]
        all_names    = [ f.split('.')[0] for f in all_files ]
        all_names    = filter(None, all_names)
        chains_roots = sorted(list(set(all_names)))
        for name_temp in chains_roots:
            # 1- get basic info on the chain:
            try:
                temp_chain       = chain_holder()
                temp_chain.name  = name_temp
                temp_chain.path  = chain_dir
                temp_chain.chain = temp_chain.path +'/'+temp_chain.name

                temp_chain.dirname    = os.path.basename( temp_chain.path )
                temp_chain.identifier = temp_chain.dirname+'/'+temp_chain.name
            except Exception as e:
                if feedback>0: print color_print.fail( 'FAILED:' )
                if feedback>0: print e
            # 2- get the maximum likelihood:
            try:
                # get minima:
                minima, full_minima = load_all_minimum_files( temp_chain )
                # if no minimum continue:
                if len(minima)==0: continue
                # feednack:
                if feedback>0:
                    print
                    print color_print.green(  'Chain:' ),
                    print os.path.relpath( temp_chain.chain, here )
                # get list of minimum files:
                minimum_files = [ _file for _file in os.listdir( temp_chain.path ) if temp_chain.name in _file and 'minimum' in _file ]
                minimum_files = [ _file for _file in minimum_files if 'minimum' in os.path.splitext( _file )[1] ]
                # result table:
                table = format_table( zip( sorted(minimum_files), [ round(_min.logLike,2) for _min in minima ] ), traspose=False)
                #
                for line in table: print '    '+line
            except Exception as e:
                if feedback>0: print color_print.fail( 'WARNING MINIMUM NOT FOUND' )
                if feedback>0: print e
            # 3- now order:
            if order:
                order_minimum_files(temp_chain)

# exit if the file is directly called:
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Prints the information of the best fit and orders best fit files.')
    parser.add_argument('--order', action='store_true',default=False, help='order the files' )
    args = parser.parse_args()
    print_order_minimum_info( chains_dir=chains_dirs, order=args.order )
    exit()
