# -*- coding: utf-8 -*-
# samples the chains to impose extra priors:
from settings import *

# define the chains on which to operate:
chains_dirs = [
                here+'/../3_Planck2015_chains',
                ]

# define backup location:
chains_backup_dir = [ chain_dir+'.backup' for chain_dir in chains_dirs ]

# create backup folders:
for chain_dir in chains_backup_dir:
    if not os.path.exists(chain_dir):
        os.mkdir(chain_dir)
    else:
        print 'Chain backup directory : '+chain_dir+' exists.'
        print 'NOT overwriting. Delete the past backup if you want to proceed.'
        exit()

# get the chains:
chains = []
for chain_dir in chains_dirs:
    for name_temp in sorted( [ f for f in os.listdir( chain_dir ) if '.paramnames' in f ] ):
        chains.append( chain_dir +'/'+('.').join( name_temp.split('.')[:-1] ) )

# loop over the chains:
for chain in chains:

    chain_name = os.path.basename( chain )
    chain_path = os.path.dirname( chain )

    print '\033[92m'+'Doing: '+chain_name+'\033[0m'

    try:
        # get paramnames:
        paramnames  = gpar.ParamNames(fileName=chain+'.paramnames')
        # loop over the chains files:
        i = 1
        while os.path.exists(chain_path+'/'+chain_name+'_'+str(i)+'.txt'):
            # preliminary:
            in_name = chain_path+'/'+chain_name+'_'+str(i)+'.txt'
            bu_name = chain_path+'.backup/'+chain_name+'_'+str(i)+'.txt'
            # some feedback:
            print 'Processing : '+in_name
            # get the chain file:
            chain_file = np.loadtxt( in_name )

            # now apply extra prior:
            full_filter = None
            # 1- cut out Nans:
            try:
                filter_list = np.logical_not(np.isnan(chain_file).any(axis=1))
                cut_elements = np.size(chain_file[:,0])-np.count_nonzero(filter_list)
                if cut_elements>0: print 'Cutting', cut_elements, 'for Nans'
            except Exception,e:
                print '\033[93m'+'WARNING'+'\033[0m'
                print e
            full_filter = copy.deepcopy( filter_list )

            # 2- cut omegam to be between 0 and 1:
            try:
                param_index = paramnames.list().index('omegam')+2
                filter_list = (chain_file[:,param_index]>=0.0)&(chain_file[:,param_index]<=1.0)
                cut_elements = np.size(chain_file[:,param_index])-np.count_nonzero(filter_list)
                if cut_elements>0: print 'Cutting', cut_elements, 'for omegam'
            except Exception,e:
                print '\033[93m'+'WARNING'+'\033[0m'
                print e
            full_filter = np.logical_and( full_filter, copy.deepcopy( filter_list ) )
            cut_elements = np.size(full_filter)-np.count_nonzero(full_filter)

            # 3- cut sigma8 to be between 0 and 3:
            try:
                param_index = paramnames.list().index('sigma8')+2
                filter_list = (chain_file[:,param_index]>=0.0)&(chain_file[:,param_index]<=2.9)
                cut_elements = np.size(chain_file[:,param_index])-np.count_nonzero(filter_list)
                if cut_elements>0: print 'Cutting', cut_elements, 'for sigma8'
            except Exception,e:
                print '\033[93m'+'WARNING'+'\033[0m'
                print e
            full_filter = np.logical_and( full_filter, copy.deepcopy( filter_list ) )
            cut_elements = np.size(full_filter)-np.count_nonzero(full_filter)

            # feedback:
            if cut_elements>=1:
                total_elements = len(chain_file[:,param_index])
                print 'Cutting out '+str(cut_elements)+' elements out of '+str(total_elements)+' or '+str(round(float(cut_elements)/float(total_elements)*100.0,2))+' percent elements.'
                # move the original chain file:
                os.rename( in_name, bu_name )
                # apply the cut:
                chain_file = chain_file[full_filter]
                # save the chain file:
                np.savetxt( in_name, chain_file )

            # increment:
            i = i +1

    except Exception,e:
        print '\033[91m'+'FAIL'+'\033[0m'
        print e
        continue

# exit if the file is directly called:
if __name__ == "__main__":
    exit()
