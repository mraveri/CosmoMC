# -*- coding: utf-8 -*-

"""
Do some test plots to see how far are we from a good distribution
"""

from settings import *
from import_chains import *
from chains_copy_utilities import *

# results directory:
out_folder = results_dir+'/chains_comparison'
if not os.path.exists(out_folder): os.mkdir(out_folder)

# set up feedback:
if __name__ == "__main__":
    sys.stdout = Logger(out_folder+'/log.txt')

# if called directly some feedback and import:
if __name__ == "__main__":
    print color_print.bold( '**********************************************************' )
    print color_print.bold( '** Chains comparison                                    **' )
    print color_print.bold( '**********************************************************' )
    # directory with chains:
    chains_dir = here+'/import_chains_sn.cache'
    # import chains:
    chains     = import_chains(chains_dir=chains_dir)

# chain couples to compare:

# single vs single prior-only
chain_comparison = [
                    [ out_folder+'/single_test_15', '3_Planck2015_chains/1_plc15_EE_prior',    '3_Planck2015_chains/1_plc15_EE'],
                    [ out_folder+'/single_test_15', '3_Planck2015_chains/1_plc15_PP_prior',    '3_Planck2015_chains/1_plc15_PP'],
                    [ out_folder+'/single_test_15', '3_Planck2015_chains/1_plc15_PP_test',     '3_Planck2015_chains/1_plc15_PP'],
                    [ out_folder+'/single_test_15', '3_Planck2015_chains/1_plc15_TE_prior',    '3_Planck2015_chains/1_plc15_TE'],
                    [ out_folder+'/single_test_15', '3_Planck2015_chains/1_plc15_TT_prior',    '3_Planck2015_chains/1_plc15_TT'],
                    [ out_folder+'/single_test_15', '3_Planck2015_chains/1_plc15_lowTEB_prior','3_Planck2015_chains/1_plc15_lowTEB'],
                    ]
chain_comparison = chain_comparison +[
                    [ out_folder+'/single_test_18', '4_Planck_chains/1_plc_EE_prior',    '4_Planck_chains/1_plc_EE'],
                    [ out_folder+'/single_test_18', '4_Planck_chains/1_plc_PP_prior',    '4_Planck_chains/1_plc_PP'],
                    [ out_folder+'/single_test_18', '4_Planck_chains/1_plc_PP_test',     '4_Planck_chains/1_plc_PP'],
                    [ out_folder+'/single_test_18', '4_Planck_chains/1_plc_TE_prior',    '4_Planck_chains/1_plc_TE'],
                    [ out_folder+'/single_test_18', '4_Planck_chains/1_plc_TT_prior',    '4_Planck_chains/1_plc_TT'],
                    [ out_folder+'/single_test_18', '4_Planck_chains/1_plc_lowTEB_prior','4_Planck_chains/1_plc_lowTEB'],
                    ]

# single no-Gaussian-prior prior-only vs single no-Gaussian-prior
chain_comparison = chain_comparison +[
                    [ out_folder+'/single_test_15', '3_Planck2015_chains/2_plc15_EE_noprior_prior',    '3_Planck2015_chains/2_plc15_EE_noprior'],
                    [ out_folder+'/single_test_15', '3_Planck2015_chains/2_plc15_PP_noprior_prior',    '3_Planck2015_chains/2_plc15_PP_noprior'],
                    [ out_folder+'/single_test_15', '3_Planck2015_chains/2_plc15_TE_noprior_prior',    '3_Planck2015_chains/2_plc15_TE_noprior'],
                    [ out_folder+'/single_test_15', '3_Planck2015_chains/2_plc15_TT_noprior_prior',    '3_Planck2015_chains/2_plc15_TT_noprior'],
                    [ out_folder+'/single_test_15', '3_Planck2015_chains/2_plc15_lowTEB_noprior_prior','3_Planck2015_chains/2_plc15_lowTEB_noprior'],
                    ]
chain_comparison = chain_comparison +[
                    [ out_folder+'/single_test_18', '4_Planck_chains/2_plc_EE_noprior_prior',    '4_Planck_chains/2_plc_EE_noprior'],
                    [ out_folder+'/single_test_18', '4_Planck_chains/2_plc_PP_noprior_prior',    '4_Planck_chains/2_plc_PP_noprior'],
                    [ out_folder+'/single_test_18', '4_Planck_chains/2_plc_TE_noprior_prior',    '4_Planck_chains/2_plc_TE_noprior'],
                    [ out_folder+'/single_test_18', '4_Planck_chains/2_plc_TT_noprior_prior',    '4_Planck_chains/2_plc_TT_noprior'],
                    [ out_folder+'/single_test_18', '4_Planck_chains/2_plc_lowTEB_noprior_prior','4_Planck_chains/2_plc_lowTEB_noprior'],
                    ]

# single no-Gaussian-prior vs single
chain_comparison = chain_comparison +[
                    [ out_folder+'/single_test_15', '3_Planck2015_chains/2_plc15_EE_noprior',    '3_Planck2015_chains/1_plc15_EE'],
                    [ out_folder+'/single_test_15', '3_Planck2015_chains/2_plc15_PP_noprior',    '3_Planck2015_chains/1_plc15_PP'],
                    [ out_folder+'/single_test_15', '3_Planck2015_chains/2_plc15_TE_noprior',    '3_Planck2015_chains/1_plc15_TE'],
                    [ out_folder+'/single_test_15', '3_Planck2015_chains/2_plc15_TT_noprior',    '3_Planck2015_chains/1_plc15_TT'],
                    [ out_folder+'/single_test_15', '3_Planck2015_chains/2_plc15_lowTEB_noprior','3_Planck2015_chains/1_plc15_lowTEB'],
                    ]
chain_comparison = chain_comparison +[
                    [ out_folder+'/single_test_18', '4_Planck_chains/2_plc_EE_noprior',    '4_Planck_chains/1_plc_EE'],
                    [ out_folder+'/single_test_18', '4_Planck_chains/2_plc_PP_noprior',    '4_Planck_chains/1_plc_PP'],
                    [ out_folder+'/single_test_18', '4_Planck_chains/2_plc_TE_noprior',    '4_Planck_chains/1_plc_TE'],
                    [ out_folder+'/single_test_18', '4_Planck_chains/2_plc_TT_noprior',    '4_Planck_chains/1_plc_TT'],
                    [ out_folder+'/single_test_18', '4_Planck_chains/2_plc_lowTEB_noprior','4_Planck_chains/1_plc_lowTEB'],
                    ]

# single vs joint
chain_comparison = chain_comparison +[
                    [ out_folder+'/joint_test_15', '3_Planck2015_chains/1_plc15_PP',     '3_Planck2015_chains/1_plc15_EE',     '3_Planck2015_chains/4_plc15_EEPP_joint'],
                    [ out_folder+'/joint_test_15', '3_Planck2015_chains/1_plc15_EE',     '3_Planck2015_chains/1_plc15_TE',     '3_Planck2015_chains/4_plc15_EETE_joint'],
                    [ out_folder+'/joint_test_15', '3_Planck2015_chains/1_plc15_lowTEB', '3_Planck2015_chains/1_plc15_EE',     '3_Planck2015_chains/4_plc15_EElowTEB_joint'],
                    [ out_folder+'/joint_test_15', '3_Planck2015_chains/1_plc15_lowTEB', '3_Planck2015_chains/1_plc15_PP',     '3_Planck2015_chains/4_plc15_PPlowTEB_joint'],
                    [ out_folder+'/joint_test_15', '3_Planck2015_chains/1_plc15_PP',     '3_Planck2015_chains/1_plc15_TE',     '3_Planck2015_chains/4_plc15_TEPP_joint'],
                    [ out_folder+'/joint_test_15', '3_Planck2015_chains/1_plc15_lowTEB', '3_Planck2015_chains/1_plc15_TE',     '3_Planck2015_chains/4_plc15_TElowTEB_joint'],
                    [ out_folder+'/joint_test_15', '3_Planck2015_chains/1_plc15_EE',     '3_Planck2015_chains/1_plc15_TT',     '3_Planck2015_chains/4_plc15_TTEE_joint'],
                    [ out_folder+'/joint_test_15', '3_Planck2015_chains/1_plc15_PP',     '3_Planck2015_chains/1_plc15_TT',     '3_Planck2015_chains/4_plc15_TTPP_joint'],
                    [ out_folder+'/joint_test_15', '3_Planck2015_chains/1_plc15_TE',     '3_Planck2015_chains/1_plc15_TT',     '3_Planck2015_chains/4_plc15_TTTE_joint'],
                    [ out_folder+'/joint_test_15', '3_Planck2015_chains/1_plc15_lowTEB', '3_Planck2015_chains/1_plc15_TT',     '3_Planck2015_chains/4_plc15_TTlowTEB_joint'],
                    ]
chain_comparison = chain_comparison +[
                    [ out_folder+'/joint_test_18', '4_Planck_chains/1_plc_PP',     '4_Planck_chains/1_plc_EE', '4_Planck_chains/4_plc_EEPP_joint'],
                    [ out_folder+'/joint_test_18', '4_Planck_chains/1_plc_EE',     '4_Planck_chains/1_plc_TE', '4_Planck_chains/4_plc_EETE_joint'],
                    [ out_folder+'/joint_test_18', '4_Planck_chains/1_plc_lowTEB', '4_Planck_chains/1_plc_EE', '4_Planck_chains/4_plc_EElowTEB_joint'],
                    [ out_folder+'/joint_test_18', '4_Planck_chains/1_plc_lowTEB', '4_Planck_chains/1_plc_PP', '4_Planck_chains/4_plc_PPlowTEB_joint'],
                    [ out_folder+'/joint_test_18', '4_Planck_chains/1_plc_PP',     '4_Planck_chains/1_plc_TE', '4_Planck_chains/4_plc_TEPP_joint'],
                    [ out_folder+'/joint_test_18', '4_Planck_chains/1_plc_lowTEB', '4_Planck_chains/1_plc_TE', '4_Planck_chains/4_plc_TElowTEB_joint'],
                    [ out_folder+'/joint_test_18', '4_Planck_chains/1_plc_EE',     '4_Planck_chains/1_plc_TT', '4_Planck_chains/4_plc_TTEE_joint'],
                    [ out_folder+'/joint_test_18', '4_Planck_chains/1_plc_PP',     '4_Planck_chains/1_plc_TT', '4_Planck_chains/4_plc_TTPP_joint'],
                    [ out_folder+'/joint_test_18', '4_Planck_chains/1_plc_TE',     '4_Planck_chains/1_plc_TT', '4_Planck_chains/4_plc_TTTE_joint'],
                    [ out_folder+'/joint_test_18', '4_Planck_chains/1_plc_lowTEB', '4_Planck_chains/1_plc_TT', '4_Planck_chains/4_plc_TTlowTEB_joint'],
                    ]

# single vs joint prior-only
chain_comparison = chain_comparison +[
                    [ out_folder+'/joint_prior_test_15', '3_Planck2015_chains/1_plc15_EE_prior',  '3_Planck2015_chains/1_plc15_PP_prior',     '3_Planck2015_chains/4_plc15_EEPP_joint_prior'],
                    [ out_folder+'/joint_prior_test_15', '3_Planck2015_chains/1_plc15_EE_prior',  '3_Planck2015_chains/1_plc15_TE_prior',     '3_Planck2015_chains/4_plc15_EETE_joint_prior'],
                    [ out_folder+'/joint_prior_test_15', '3_Planck2015_chains/1_plc15_EE_prior',  '3_Planck2015_chains/1_plc15_lowTEB_prior', '3_Planck2015_chains/4_plc15_EElowTEB_joint_prior'],
                    [ out_folder+'/joint_prior_test_15', '3_Planck2015_chains/1_plc15_PP_prior',  '3_Planck2015_chains/1_plc15_lowTEB_prior', '3_Planck2015_chains/4_plc15_PPlowTEB_joint_prior'],
                    [ out_folder+'/joint_prior_test_15', '3_Planck2015_chains/1_plc15_TE_prior',  '3_Planck2015_chains/1_plc15_PP_prior',     '3_Planck2015_chains/4_plc15_TEPP_joint_prior'],
                    [ out_folder+'/joint_prior_test_15', '3_Planck2015_chains/1_plc15_TE_prior',  '3_Planck2015_chains/1_plc15_lowTEB_prior', '3_Planck2015_chains/4_plc15_TElowTEB_joint_prior'],
                    [ out_folder+'/joint_prior_test_15', '3_Planck2015_chains/1_plc15_TT_prior',  '3_Planck2015_chains/1_plc15_EE_prior',     '3_Planck2015_chains/4_plc15_TTEE_joint_prior'],
                    [ out_folder+'/joint_prior_test_15', '3_Planck2015_chains/1_plc15_TT_prior',  '3_Planck2015_chains/1_plc15_PP_prior',     '3_Planck2015_chains/4_plc15_TTPP_joint_prior'],
                    [ out_folder+'/joint_prior_test_15', '3_Planck2015_chains/1_plc15_TE_prior',  '3_Planck2015_chains/1_plc15_TE_prior',     '3_Planck2015_chains/4_plc15_TTTE_joint_prior'],
                    [ out_folder+'/joint_prior_test_15', '3_Planck2015_chains/1_plc15_TT_prior',  '3_Planck2015_chains/1_plc15_lowTEB_prior', '3_Planck2015_chains/4_plc15_TTlowTEB_joint_prior'],
                    ]
chain_comparison = chain_comparison +[
                    [ out_folder+'/joint_prior_test_18', '4_Planck_chains/1_plc_EE_prior',  '4_Planck_chains/1_plc_PP_prior',     '4_Planck_chains/4_plc_EEPP_joint_prior'],
                    [ out_folder+'/joint_prior_test_18', '4_Planck_chains/1_plc_EE_prior',  '4_Planck_chains/1_plc_TE_prior',     '4_Planck_chains/4_plc_EETE_joint_prior'],
                    [ out_folder+'/joint_prior_test_18', '4_Planck_chains/1_plc_EE_prior',  '4_Planck_chains/1_plc_lowTEB_prior', '4_Planck_chains/4_plc_EElowTEB_joint_prior'],
                    [ out_folder+'/joint_prior_test_18', '4_Planck_chains/1_plc_PP_prior',  '4_Planck_chains/1_plc_lowTEB_prior', '4_Planck_chains/4_plc_PPlowTEB_joint_prior'],
                    [ out_folder+'/joint_prior_test_18', '4_Planck_chains/1_plc_TE_prior',  '4_Planck_chains/1_plc_PP_prior',     '4_Planck_chains/4_plc_TEPP_joint_prior'],
                    [ out_folder+'/joint_prior_test_18', '4_Planck_chains/1_plc_TE_prior',  '4_Planck_chains/1_plc_lowTEB_prior', '4_Planck_chains/4_plc_TElowTEB_joint_prior'],
                    [ out_folder+'/joint_prior_test_18', '4_Planck_chains/1_plc_TT_prior',  '4_Planck_chains/1_plc_EE_prior',     '4_Planck_chains/4_plc_TTEE_joint_prior'],
                    [ out_folder+'/joint_prior_test_18', '4_Planck_chains/1_plc_TT_prior',  '4_Planck_chains/1_plc_PP_prior',     '4_Planck_chains/4_plc_TTPP_joint_prior'],
                    [ out_folder+'/joint_prior_test_18', '4_Planck_chains/1_plc_TE_prior',  '4_Planck_chains/1_plc_TE_prior',     '4_Planck_chains/4_plc_TTTE_joint_prior'],
                    [ out_folder+'/joint_prior_test_18', '4_Planck_chains/1_plc_TT_prior',  '4_Planck_chains/1_plc_lowTEB_prior', '4_Planck_chains/4_plc_TTlowTEB_joint_prior'],
                    ]

# joint prior-only vs joint
chain_comparison = chain_comparison +[
                    [ out_folder+'/joint_test_15', '3_Planck2015_chains/4_plc15_EEPP_joint_prior'    ,'3_Planck2015_chains/4_plc15_EEPP_joint'],
                    [ out_folder+'/joint_test_15', '3_Planck2015_chains/4_plc15_EETE_joint_prior'    ,'3_Planck2015_chains/4_plc15_EETE_joint'],
                    [ out_folder+'/joint_test_15', '3_Planck2015_chains/4_plc15_EElowTEB_joint_prior','3_Planck2015_chains/4_plc15_EElowTEB_joint'],
                    [ out_folder+'/joint_test_15', '3_Planck2015_chains/4_plc15_PPlowTEB_joint_prior','3_Planck2015_chains/4_plc15_PPlowTEB_joint'],
                    [ out_folder+'/joint_test_15', '3_Planck2015_chains/4_plc15_TEPP_joint_prior'    ,'3_Planck2015_chains/4_plc15_TEPP_joint'],
                    [ out_folder+'/joint_test_15', '3_Planck2015_chains/4_plc15_TElowTEB_joint_prior','3_Planck2015_chains/4_plc15_TElowTEB_joint'],
                    [ out_folder+'/joint_test_15', '3_Planck2015_chains/4_plc15_TTEE_joint_prior'    ,'3_Planck2015_chains/4_plc15_TTEE_joint'],
                    [ out_folder+'/joint_test_15', '3_Planck2015_chains/4_plc15_TTPP_joint_prior'    ,'3_Planck2015_chains/4_plc15_TTPP_joint'],
                    [ out_folder+'/joint_test_15', '3_Planck2015_chains/4_plc15_TTTE_joint_prior'    ,'3_Planck2015_chains/4_plc15_TTTE_joint'],
                    [ out_folder+'/joint_test_15', '3_Planck2015_chains/4_plc15_TTlowTEB_joint_prior','3_Planck2015_chains/4_plc15_TTlowTEB_joint'],
                    ]
chain_comparison = chain_comparison +[
                    [ out_folder+'/joint_test_18', '4_Planck_chains/4_plc_EEPP_joint_prior'    ,'4_Planck_chains/4_plc_EEPP_joint'],
                    [ out_folder+'/joint_test_18', '4_Planck_chains/4_plc_EETE_joint_prior'    ,'4_Planck_chains/4_plc_EETE_joint'],
                    [ out_folder+'/joint_test_18', '4_Planck_chains/4_plc_EElowTEB_joint_prior','4_Planck_chains/4_plc_EElowTEB_joint'],
                    [ out_folder+'/joint_test_18', '4_Planck_chains/4_plc_PPlowTEB_joint_prior','4_Planck_chains/4_plc_PPlowTEB_joint'],
                    [ out_folder+'/joint_test_18', '4_Planck_chains/4_plc_TEPP_joint_prior'    ,'4_Planck_chains/4_plc_TEPP_joint'],
                    [ out_folder+'/joint_test_18', '4_Planck_chains/4_plc_TElowTEB_joint_prior','4_Planck_chains/4_plc_TElowTEB_joint'],
                    [ out_folder+'/joint_test_18', '4_Planck_chains/4_plc_TTEE_joint_prior'    ,'4_Planck_chains/4_plc_TTEE_joint'],
                    [ out_folder+'/joint_test_18', '4_Planck_chains/4_plc_TTPP_joint_prior'    ,'4_Planck_chains/4_plc_TTPP_joint'],
                    [ out_folder+'/joint_test_18', '4_Planck_chains/4_plc_TTTE_joint_prior'    ,'4_Planck_chains/4_plc_TTTE_joint'],
                    [ out_folder+'/joint_test_18', '4_Planck_chains/4_plc_TTlowTEB_joint_prior','4_Planck_chains/4_plc_TTlowTEB_joint'],
                    ]

# test copies:
chain_comparison = chain_comparison +[
                    [ out_folder+'/copy_test_15', '3_Planck2015_chains/0_prior_1p',                   '3_Planck2015_chains/0_prior_2p'],
                    [ out_folder+'/copy_test_15', '3_Planck2015_chains/3_plc15_EEPP_1copy',           '3_Planck2015_chains/1_plc15_EE',       '3_Planck2015_chains/1_plc15_PP', ],
                    [ out_folder+'/copy_test_15', '3_Planck2015_chains/3_plc15_EETE_1copy',           '3_Planck2015_chains/1_plc15_EE',       '3_Planck2015_chains/1_plc15_TE', ],
                    [ out_folder+'/copy_test_15', '3_Planck2015_chains/3_plc15_EElowTEB_1copy',       '3_Planck2015_chains/1_plc15_EE',       '3_Planck2015_chains/1_plc15_lowTEB', ],
                    [ out_folder+'/copy_test_15', '3_Planck2015_chains/3_plc15_PPlowTEB_1copy',       '3_Planck2015_chains/1_plc15_PP',       '3_Planck2015_chains/1_plc15_lowTEB', ],
                    [ out_folder+'/copy_test_15', '3_Planck2015_chains/3_plc15_TEPP_1copy',           '3_Planck2015_chains/1_plc15_TE',       '3_Planck2015_chains/1_plc15_PP', ],
                    [ out_folder+'/copy_test_15', '3_Planck2015_chains/3_plc15_TElowTEB_1copy',       '3_Planck2015_chains/1_plc15_TE',       '3_Planck2015_chains/1_plc15_lowTEB', ],
                    [ out_folder+'/copy_test_15', '3_Planck2015_chains/3_plc15_TTEE_1copy',           '3_Planck2015_chains/1_plc15_TT',       '3_Planck2015_chains/1_plc15_EE', ],
                    [ out_folder+'/copy_test_15', '3_Planck2015_chains/3_plc15_TTPP_1copy',           '3_Planck2015_chains/1_plc15_TT',       '3_Planck2015_chains/1_plc15_PP', ],
                    [ out_folder+'/copy_test_15', '3_Planck2015_chains/3_plc15_TTTE_1copy',           '3_Planck2015_chains/1_plc15_TT',       '3_Planck2015_chains/1_plc15_TE', ],
                    [ out_folder+'/copy_test_15', '3_Planck2015_chains/3_plc15_TTlowTEB_1copy',       '3_Planck2015_chains/1_plc15_TT',       '3_Planck2015_chains/1_plc15_lowTEB', ],
                    [ out_folder+'/copy_test_15', '3_Planck2015_chains/3_plc15_EEPP_1copy_prior',     '3_Planck2015_chains/1_plc15_EE_prior', '3_Planck2015_chains/1_plc15_PP_prior', ],
                    [ out_folder+'/copy_test_15', '3_Planck2015_chains/3_plc15_EETE_1copy_prior',     '3_Planck2015_chains/1_plc15_EE_prior', '3_Planck2015_chains/1_plc15_TE_prior', ],
                    [ out_folder+'/copy_test_15', '3_Planck2015_chains/3_plc15_EElowTEB_1copy_prior', '3_Planck2015_chains/1_plc15_EE_prior', '3_Planck2015_chains/1_plc15_lowTEB_prior', ],
                    [ out_folder+'/copy_test_15', '3_Planck2015_chains/3_plc15_PPlowTEB_1copy_prior', '3_Planck2015_chains/1_plc15_PP_prior', '3_Planck2015_chains/1_plc15_lowTEB_prior', ],
                    [ out_folder+'/copy_test_15', '3_Planck2015_chains/3_plc15_TEPP_1copy_prior',     '3_Planck2015_chains/1_plc15_TE_prior', '3_Planck2015_chains/1_plc15_PP_prior', ],
                    [ out_folder+'/copy_test_15', '3_Planck2015_chains/3_plc15_TElowTEB_1copy_prior', '3_Planck2015_chains/1_plc15_TE_prior', '3_Planck2015_chains/1_plc15_lowTEB_prior', ],
                    [ out_folder+'/copy_test_15', '3_Planck2015_chains/3_plc15_TTEE_1copy_prior',     '3_Planck2015_chains/1_plc15_TT_prior', '3_Planck2015_chains/1_plc15_EE_prior', ],
                    [ out_folder+'/copy_test_15', '3_Planck2015_chains/3_plc15_TTPP_1copy_prior',     '3_Planck2015_chains/1_plc15_TT_prior', '3_Planck2015_chains/1_plc15_PP_prior', ],
                    [ out_folder+'/copy_test_15', '3_Planck2015_chains/3_plc15_TTTE_1copy_prior',     '3_Planck2015_chains/1_plc15_TT_prior', '3_Planck2015_chains/1_plc15_TE_prior', ],
                    [ out_folder+'/copy_test_15', '3_Planck2015_chains/3_plc15_TTlowTEB_1copy_prior', '3_Planck2015_chains/1_plc15_TT_prior', '3_Planck2015_chains/1_plc15_lowTEB_prior', ],
                    ]
chain_comparison = chain_comparison +[
                    [ out_folder+'/copy_test_18', '4_Planck_chains/3_plc_EEPP_1copy',           '4_Planck_chains/1_plc_EE',       '4_Planck_chains/1_plc_PP', ],
                    [ out_folder+'/copy_test_18', '4_Planck_chains/3_plc_EETE_1copy',           '4_Planck_chains/1_plc_EE',       '4_Planck_chains/1_plc_TE', ],
                    [ out_folder+'/copy_test_18', '4_Planck_chains/3_plc_EElowTEB_1copy',       '4_Planck_chains/1_plc_EE',       '4_Planck_chains/1_plc_lowTEB', ],
                    [ out_folder+'/copy_test_18', '4_Planck_chains/3_plc_PPlowTEB_1copy',       '4_Planck_chains/1_plc_PP',       '4_Planck_chains/1_plc_lowTEB', ],
                    [ out_folder+'/copy_test_18', '4_Planck_chains/3_plc_TEPP_1copy',           '4_Planck_chains/1_plc_TE',       '4_Planck_chains/1_plc_PP', ],
                    [ out_folder+'/copy_test_18', '4_Planck_chains/3_plc_TElowTEB_1copy',       '4_Planck_chains/1_plc_TE',       '4_Planck_chains/1_plc_lowTEB', ],
                    [ out_folder+'/copy_test_18', '4_Planck_chains/3_plc_TTEE_1copy',           '4_Planck_chains/1_plc_TT',       '4_Planck_chains/1_plc_EE', ],
                    [ out_folder+'/copy_test_18', '4_Planck_chains/3_plc_TTPP_1copy',           '4_Planck_chains/1_plc_TT',       '4_Planck_chains/1_plc_PP', ],
                    [ out_folder+'/copy_test_18', '4_Planck_chains/3_plc_TTTE_1copy',           '4_Planck_chains/1_plc_TT',       '4_Planck_chains/1_plc_TE', ],
                    [ out_folder+'/copy_test_18', '4_Planck_chains/3_plc_TTlowTEB_1copy',       '4_Planck_chains/1_plc_TT',       '4_Planck_chains/1_plc_lowTEB', ],
                    [ out_folder+'/copy_test_18', '4_Planck_chains/3_plc_EEPP_1copy_prior',     '4_Planck_chains/1_plc_EE_prior', '4_Planck_chains/1_plc_PP_prior', ],
                    [ out_folder+'/copy_test_18', '4_Planck_chains/3_plc_EETE_1copy_prior',     '4_Planck_chains/1_plc_EE_prior', '4_Planck_chains/1_plc_TE_prior', ],
                    [ out_folder+'/copy_test_18', '4_Planck_chains/3_plc_EElowTEB_1copy_prior', '4_Planck_chains/1_plc_EE_prior', '4_Planck_chains/1_plc_lowTEB_prior', ],
                    [ out_folder+'/copy_test_18', '4_Planck_chains/3_plc_PPlowTEB_1copy_prior', '4_Planck_chains/1_plc_PP_prior', '4_Planck_chains/1_plc_lowTEB_prior', ],
                    [ out_folder+'/copy_test_18', '4_Planck_chains/3_plc_TEPP_1copy_prior',     '4_Planck_chains/1_plc_TE_prior', '4_Planck_chains/1_plc_PP_prior', ],
                    [ out_folder+'/copy_test_18', '4_Planck_chains/3_plc_TElowTEB_1copy_prior', '4_Planck_chains/1_plc_TE_prior', '4_Planck_chains/1_plc_lowTEB_prior', ],
                    [ out_folder+'/copy_test_18', '4_Planck_chains/3_plc_TTEE_1copy_prior',     '4_Planck_chains/1_plc_TT_prior', '4_Planck_chains/1_plc_EE_prior', ],
                    [ out_folder+'/copy_test_18', '4_Planck_chains/3_plc_TTPP_1copy_prior',     '4_Planck_chains/1_plc_TT_prior', '4_Planck_chains/1_plc_PP_prior', ],
                    [ out_folder+'/copy_test_18', '4_Planck_chains/3_plc_TTTE_1copy_prior',     '4_Planck_chains/1_plc_TT_prior', '4_Planck_chains/1_plc_TE_prior', ],
                    [ out_folder+'/copy_test_18', '4_Planck_chains/3_plc_TTlowTEB_1copy_prior', '4_Planck_chains/1_plc_TT_prior', '4_Planck_chains/1_plc_lowTEB_prior', ],
                    ]
# 15 vs 18 comparison:
chain_comparison = chain_comparison +[
                    [ out_folder+'/comparison_15_18', '3_Planck2015_chains/1_plc15_EE',    '4_Planck_chains/1_plc_EE'],
                    [ out_folder+'/comparison_15_18', '3_Planck2015_chains/1_plc15_PP',    '4_Planck_chains/1_plc_PP'],
                    [ out_folder+'/comparison_15_18', '3_Planck2015_chains/1_plc15_TE',    '4_Planck_chains/1_plc_TE'],
                    [ out_folder+'/comparison_15_18', '3_Planck2015_chains/1_plc15_TT',    '4_Planck_chains/1_plc_TT'],
                    [ out_folder+'/comparison_15_18', '3_Planck2015_chains/1_plc15_lowTEB','4_Planck_chains/1_plc_lowTEB'],
                    ]

#
chain_comparison = chain_comparison +[
                    [ out_folder+'/SN_split', '5_SN_chains/0_prior_1p_abs'       , '5_SN_chains/0_prior_1p_noabs'  ],
                    [ out_folder+'/SN_split', '5_SN_chains/0_prior_2p_abs'       , '5_SN_chains/0_prior_2p_noabs'  ],
                    [ out_folder+'/SN_split', '5_SN_chains/0_prior_1p_abs'       , '5_SN_chains/0_prior_2p_abs'    ],
                    [ out_folder+'/SN_split', '5_SN_chains/0_prior_1p_noabs'     , '5_SN_chains/0_prior_2p_noabs'  ],
                    [ out_folder+'/SN_split', '5_SN_chains/2p2_SNC_zcut0p3_abs'  , '5_SN_chains/1p2_SN1_zcut0p3_abs'  , '5_SN_chains/1p2_SN2_zcut0p3_abs'  , '5_SN_chains/3_SNJ_abs'   ],
                    [ out_folder+'/SN_split', '5_SN_chains/2p2_SNC_zcut0p7_abs'  , '5_SN_chains/1p2_SN1_zcut0p7_abs'  , '5_SN_chains/1p2_SN2_zcut0p7_abs'  , '5_SN_chains/3_SNJ_abs'   ],
                    ]

# parameters for triangle plots:
triangle_paramnames = [ 'omegabh2',
                        'omegach2',
                        'thetastar',
                        'tau',
                        'logA',
                        'ns',
                        'H0',
                        'omegam',
                        'sigma8',
                        'rdrag',
                        'kd',
                        'M_JLA',
                        'w',
                        'omegak' ]

# define the comparison utility:
def plotter_comparison( _out_folder, _chains, triangle_paramnames=triangle_paramnames ):
    # get number of chains:
    _num_chains = len(_chains)
    # test:
    if _num_chains<=0:
        raise( ValueError, 'No input chains' )
    # check that the folder exists and in case create it:
    if not os.path.exists(_out_folder): os.mkdir(_out_folder)
    # some feedback:
    _msg_print  = 'Doing: '+_chains[0].identifier
    for i in range(1,_num_chains):
        _msg_print += ' vs ' + _chains[i].identifier
    print color_print.bold( _msg_print )
    # get the samples:
    _plot_list = [ _chains[i].samples for i in range(_num_chains) ]
    ############################################################################
    # Do the 1D plot:
    ############################################################################
    g = gplot.getSubplotPlotter()
    g.plots_1d( _plot_list );
    # export:
    _fig_1D_name = '/'
    for i in range(_num_chains):
        if i == 0:
            _fig_1D_name += _chains[i].name
        else:
            _fig_1D_name += '_'+_chains[i].name
    g.export( _out_folder+_fig_1D_name+'_1D.pdf' )
    # close:
    plt.close('all')
    ############################################################################
    # Do the triangular plot:
    ############################################################################
    # get the parameter names to plot filtering out the excluded ones:
    parameter_names = [ _name for _name in _chains[0].samples.getParamNames().list() if _name in triangle_paramnames ]
    # do the plot:
    g    = gplot.getSubplotPlotter();
    plot = g.triangle_plot( _plot_list, params=parameter_names, filled=True )
    # export:
    _fig_tri_name = '/'
    for i in range(_num_chains):
        if i == 0:
            _fig_tri_name += _chains[i].name
        else:
            _fig_tri_name += '_'+_chains[i].name
    g.export( _out_folder+_fig_tri_name+'_tri.pdf' )
    # close:
    plt.close('all')
    ############################################################################
    # Final feedback:
    ############################################################################
    print '       Saved plots in '+_out_folder

# If the file is directly called do all plots:
if __name__ == "__main__":
    # loop over the groups of chains to compare:
    for _chains_to_compare in chain_comparison:
        # get all chains in "couple" for comparison
        _num_chains = len(_chains_to_compare)-1
        _out_root   = _chains_to_compare[0]
        _reference_chains = []
        for i in range(1,_num_chains+1):
            try:
                _reference_chains.append(chains[_chains_to_compare[i]])
            except:
                print color_print.fail( 'WARNING chain not found: '+_chains_to_compare[i] )
        # try to separate copies:
        _chains_to_plot = []
        for _chain in _reference_chains:
            for _temp in split_copies( _chain ):
                _chains_to_plot.append(_temp)
        # plot:
        try:
            plotter_comparison( _out_root, _chains_to_plot )
        except Exception,e:
            print color_print.fail( 'WARNING' )
            print e
    #
    exit()
 
