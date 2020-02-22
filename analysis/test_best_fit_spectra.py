# -*- coding: utf-8 -*-

"""
Creates the parameters files to run the mean and the maximum likelihood search
"""
from settings  import *
from utilities import *
from mpl_toolkits.axes_grid1 import make_axes_locatable
from log_lin_scale import *

# some feedback:
print color_print.bold( '**********************************************************' )
print color_print.bold( '** Best fit spectra                                     **' )
print color_print.bold( '**********************************************************' )

# define data directory:
data_dir = here+'/data_plot'
spectra_dir = here+'/gdmcamb_best_fit/results/spectra_results'

# define output directory:
out_dir = here+'/results/best_fit_spectra'
if not os.path.exists(out_dir): os.mkdir(out_dir)

# load Planck CMB data:
_data_TT = np.loadtxt(data_dir+'/COM_PowerSpect_CMB-TT-hiL-binned_R2.02.txt')
_data_TT_lowl = np.loadtxt(data_dir+'/COM_PowerSpect_CMB-TT-loL-full_R2.02.txt')
_data_EE = np.loadtxt(data_dir+'/COM_PowerSpect_CMB-EE-hiL-binned_R2.02.txt')
_data_EE_lowl = np.loadtxt(data_dir+'/COM_PowerSpect_CMB-EE-loL-full_R2.02.txt')
_data_TE = np.loadtxt(data_dir+'/COM_PowerSpect_CMB-TE-hiL-binned_R2.02.txt')
_data_TE_lowl = np.loadtxt(data_dir+'/COM_PowerSpect_CMB-TE-loL-full_R2.02.txt')
_data_LL = np.loadtxt(data_dir+'/smica_g30_ftl_full_pp_bandpowers.dat')
# load SPT CMB data:
_data_SPT_TT = np.loadtxt(data_dir+'/spt_sz.dat')
# load SN data:
with open(data_dir+'/pantheon_SN_binned.txt') as f:
    ncols = len(f.readline()[1:].split())
_sn_data       = np.loadtxt(data_dir+'/pantheon_SN_binned.txt', usecols=xrange(1,ncols-1) )

# for testing purposes:
root_ref = '1_lcdm'
root_comp = '2_lambda_5p'

# define helper functions:
def helper_plotter( root_ref, root_comp ):
    # load the spectra:
    _ref     = np.loadtxt(spectra_dir+'/'+root_ref+'_lensedCls.dat')
    _ref_ll  = np.loadtxt(spectra_dir+'/'+root_ref+'_lenspotentialCls.dat')
    _ref_transfer_1  = np.loadtxt(spectra_dir+'/'+root_ref+'_transfer_out_0p5.dat')
    _ref_transfer_2  = np.loadtxt(spectra_dir+'/'+root_ref+'_transfer_out.dat')
    _ref_transfer_3  = np.loadtxt(spectra_dir+'/'+root_ref+'_transfer_out_1p5.dat')
    _ref_background  = np.loadtxt(spectra_dir+'/'+root_ref+'_background.dat')
    _comp    = np.loadtxt(spectra_dir+'/'+root_comp+'_lensedCls.dat')
    _comp_ll = np.loadtxt(spectra_dir+'/'+root_comp+'_lenspotentialCls.dat')
    _comp_transfer_1 = np.loadtxt(spectra_dir+'/'+root_comp+'_transfer_out_0p5.dat')
    _comp_transfer_2 = np.loadtxt(spectra_dir+'/'+root_comp+'_transfer_out.dat')
    _comp_transfer_3 = np.loadtxt(spectra_dir+'/'+root_comp+'_transfer_out_1p5.dat')
    _comp_background  = np.loadtxt(spectra_dir+'/'+root_comp+'_background.dat')
    # prepare the plot:
    fig = plt.gcf()
    fig.set_size_inches( 2.*x_size/2.54, 4.*y_size/2.54 )
    gs = gridspec.GridSpec(4,2)

    ##############################
    # TT:
    ##############################
    ax1 = plt.subplot(gs[0,0])
    # interpolate theoretical prediction:
    _reference_TT = interp1d( _ref[:,0], _ref[:,1], kind='cubic' )
    # theoretical line:
    _ell = _comp[:,0]
    ax1.plot( _ell, (_comp[:,1]-_reference_TT(_ell))/_ref[:,1]/np.sqrt(2./(2.*_ell+1.)), c=colormap[0], lw=1.2 )
    ax1.axhline( 0., color='k', lw=1., zorder=1 )
    # high-l data:
    _ell = _data_TT[:,0]
    _y   = (_data_TT[:,3]-_reference_TT(_ell))/_reference_TT(_ell)/np.sqrt(2./(2.*_ell+1.))
    _err = _data_TT[:,4]/_reference_TT(_ell)/np.sqrt(2./(2.*_ell+1.))
    ax1.errorbar( _ell, _y, yerr=_err, fmt='.', c=colormap[1], lw=1., zorder=1, label='Planck' )
    # low-l data:
    _ell = _data_TT_lowl[:,0]
    _y   = (_data_TT_lowl[:,1]-_reference_TT(_ell))/_reference_TT(_ell)/np.sqrt(2./(2.*_ell+1.))
    _err_up = _data_TT_lowl[:,2]/_reference_TT(_ell)/np.sqrt(2./(2.*_ell+1.))
    _err_dn = _data_TT_lowl[:,3]/_reference_TT(_ell)/np.sqrt(2./(2.*_ell+1.))
    ax1.errorbar( _ell, _y, yerr=[_err_dn,_err_up], fmt='.', c=colormap[1], lw=1., zorder=1 )
    # SPT data:
    _ell = _data_SPT_TT[:,0]
    _y   = (_data_SPT_TT[:,1]-_reference_TT(_ell))/_reference_TT(_ell)/np.sqrt(2./(2.*_ell+1.))
    _err = _data_SPT_TT[:,2]/_reference_TT(_ell)/np.sqrt(2./(2.*_ell+1.))
    ax1.errorbar( _ell, _y, yerr=_err, fmt='.', c=colormap[2], lw=1., zorder=1, label='SPT' )
    # scale:
    ax1.set_xscale( 'loglin', linthreshx=100.,linscalex=.1 )
    ax1.set_xlim([2,2500])
    ax1.set_ylim([-4,4])
    ax1.set_xlabel('$\\ell$', fontsize=main_fontsize )
    ax1.set_ylabel('$\\Delta C_\\ell^{TT} / \\sigma_{TT}$', fontsize=main_fontsize )
    # label:
    x_labels = [2,10,30,100,1000,2500]
    ax1.set_xticks( x_labels )
    ax1.set_xticklabels(x_labels, horizontalalignment='center', fontsize=0.9*main_fontsize)
    ax1.xaxis.get_majorticklabels()[0].set_horizontalalignment('left')
    ax1.xaxis.get_majorticklabels()[-1].set_horizontalalignment('right')
    y_labels = [-4,-3,-2,-1,0,1,2,3,4]
    ax1.set_yticks( y_labels )
    ax1.set_yticklabels(y_labels, horizontalalignment='right', fontsize=0.9*main_fontsize)
    ax1.yaxis.get_majorticklabels()[0].set_verticalalignment('bottom')
    ax1.yaxis.get_majorticklabels()[-1].set_verticalalignment('top')
    # title:
    ax1.text( 0.01,1.04,'a) CMB temperature spectrum with Planck and SPT data', horizontalalignment='left', transform=ax1.transAxes, fontsize=main_fontsize)
    # legend:
    ax1.legend(framealpha=1.,loc='upper left',fontsize=main_fontsize,fancybox=True,edgecolor='k')

    ##############################
    # EE:
    ##############################
    ax2 = plt.subplot(gs[0,1])
    # interpolate theoretical prediction:
    _reference_EE = interp1d( _ref[:,0], _ref[:,2], kind='cubic' )
    # theoretical line:
    _ell = _comp[:,0]
    ax2.plot( _ell, (_comp[:,2]-_reference_EE(_ell))/_reference_EE(_ell)/np.sqrt(2./(2.*_ell+1.)), c=colormap[0], lw=1.2 )
    ax2.axhline( 0., color='k', lw=1., zorder=1 )
    # high-l data:
    _ell = _data_EE[:,0]
    _y   = (_data_EE[:,3]-_reference_EE(_ell))/_reference_EE(_ell)/np.sqrt(2./(2.*_ell+1.))
    _err = _data_EE[:,4]/_reference_EE(_ell)/np.sqrt(2./(2.*_ell+1.))
    ax2.errorbar( _ell, _y, yerr=_err, fmt='.', c=colormap[1], lw=1., zorder=1 )
    # low-l data:
    _ell = _data_EE_lowl[:,0]
    _y   = (_data_EE_lowl[:,1]-_reference_EE(_ell))/_reference_EE(_ell)/np.sqrt(2./(2.*_ell+1.))
    _err_up = _data_EE_lowl[:,2]/_reference_EE(_ell)/np.sqrt(2./(2.*_ell+1.))
    _err_dn = _data_EE_lowl[:,3]/_reference_EE(_ell)/np.sqrt(2./(2.*_ell+1.))
    ax2.errorbar( _ell, _y, yerr=[_err_dn,_err_up], fmt='.', c=colormap[1], lw=1., zorder=1 )
    # scale:
    ax2.set_xscale( 'loglin', linthreshx=100.,linscalex=.1 )
    ax2.set_xlim([2,2000])
    ax2.set_ylim([-4,4])
    ax2.set_xlabel('$\\ell$', fontsize=main_fontsize)
    ax2.set_ylabel('$\\Delta C_\\ell^{EE} / \\sigma_{EE}$', fontsize=main_fontsize)
    # label:
    x_labels = [2,10,30,100,1000,2000]
    ax2.set_xticks( x_labels )
    ax2.set_xticklabels(x_labels, horizontalalignment='center', fontsize=0.9*main_fontsize)
    ax2.xaxis.get_majorticklabels()[0].set_horizontalalignment('left')
    ax2.xaxis.get_majorticklabels()[-1].set_horizontalalignment('right')
    y_labels = [-4,-3,-2,-1,0,1,2,3,4]
    ax2.set_yticks( y_labels )
    ax2.set_yticklabels(y_labels, horizontalalignment='right', fontsize=0.9*main_fontsize)
    ax2.yaxis.get_majorticklabels()[0].set_verticalalignment('bottom')
    ax2.yaxis.get_majorticklabels()[-1].set_verticalalignment('top')
    # title:
    ax2.text( 0.01,1.04,'b) CMB E-mode polarization spectrum with Planck data', horizontalalignment='left', transform=ax2.transAxes, fontsize=main_fontsize)

    ##############################
    # TE:
    ##############################
    ax3 = plt.subplot(gs[1,0])
    # interpolate theoretical prediction:
    _reference_TE = interp1d( _ref[:,0], _ref[:,4], kind='cubic' )
    # theoretical line:
    _ell = _comp[:,0]
    _sigma_Cl_TE = np.sqrt(2./(2.*_ell+1.))*np.sqrt( _reference_TT(_ell)*_reference_EE(_ell) +_reference_TE(_ell)**2 )
    ax3.plot( _ell, (_comp[:,4]-_reference_TE(_ell))/_sigma_Cl_TE, c=colormap[0], lw=1.2 )
    ax3.axhline( 0., color='k', lw=1., zorder=1 )
    # high-l data:
    _ell = _data_TE[:,0]
    _sigma_Cl_TE = np.sqrt(2./(2.*_ell+1.))*np.sqrt( _reference_TT(_ell)*_reference_EE(_ell) +_reference_TE(_ell)**2 )
    _y   = (_data_TE[:,3]-_reference_TE(_ell))/_sigma_Cl_TE
    _err = _data_TE[:,4]/_sigma_Cl_TE
    ax3.errorbar( _ell, _y, yerr=_err, fmt='.', c=colormap[1], lw=1., zorder=1 )
    # low-l data:
    _ell = _data_TE_lowl[:,0]
    _sigma_Cl_TE = np.sqrt(2./(2.*_ell+1.))*np.sqrt( _reference_TT(_ell)*_reference_EE(_ell) +_reference_TE(_ell)**2 )
    _y   = (_data_TE_lowl[:,1]-_reference_TE(_ell))/_sigma_Cl_TE
    _err = _data_TE_lowl[:,2]/_sigma_Cl_TE
    ax3.errorbar( _ell, _y, yerr=_err, fmt='.', c=colormap[1], lw=1., zorder=1 )
    # scale:
    ax3.set_xscale( 'loglin', linthreshx=100.,linscalex=.1 )
    ax3.set_xlim([2,2000])
    ax3.set_ylim([-4,4])
    ax3.set_xlabel('$\\ell$', fontsize=main_fontsize)
    ax3.set_ylabel('$\\Delta C_\\ell^{TE} / \\sigma_{TE}$', fontsize=main_fontsize)
    # label:
    x_labels = [2,10,30,100,1000,2000]
    ax3.set_xticks( x_labels )
    ax3.set_xticklabels(x_labels, horizontalalignment='center', fontsize=0.9*main_fontsize)
    ax3.xaxis.get_majorticklabels()[0].set_horizontalalignment('left')
    ax3.xaxis.get_majorticklabels()[-1].set_horizontalalignment('right')
    y_labels = [-4,-3,-2,-1,0,1,2,3,4]
    ax3.set_yticks( y_labels )
    ax3.set_yticklabels(y_labels, horizontalalignment='right', fontsize=0.9*main_fontsize)
    ax3.yaxis.get_majorticklabels()[0].set_verticalalignment('bottom')
    ax3.yaxis.get_majorticklabels()[-1].set_verticalalignment('top')
    # title:
    ax3.text( 0.01,1.04,'c) CMB TE cross correlation spectrum with Planck data', horizontalalignment='left', transform=ax3.transAxes, fontsize=main_fontsize)

    ##############################
    # LL:
    ##############################
    ax4 = plt.subplot(gs[1,1])
    # interpolate theoretical prediction:
    _reference_LL = interp1d( _ref_ll[:,0], _ref_ll[:,5], kind='cubic' )
    # theoretical line:
    _ell = _comp_ll[:,0]
    ax4.plot( _ell, (_comp_ll[:,5]-_reference_LL(_ell))/_reference_LL(_ell), c=colormap[0], lw=1.2 )
    ax4.axhline( 0., color='k', lw=1., zorder=1 )
    # data:
    _ell = _data_LL[:,3]
    _y   = (_data_LL[:,4]-_reference_LL(_ell))/_reference_LL(_ell)
    _err = _data_LL[:,5]/_reference_LL(_ell)
    ax4.errorbar( _ell, _y, yerr=_err, fmt='.', c=colormap[1], lw=1., zorder=1 )
    # scale:
    ax4.set_xlim([0,500])
    ax4.set_ylim([-0.5,0.5])
    ax4.set_xlabel('$\\ell$', fontsize=main_fontsize)
    ax4.set_ylabel('$\\Delta C_\\ell^{\\phi\\phi} / C_\\ell^{\\phi\\phi}$', fontsize=main_fontsize)
    # label:
    x_labels = [0,100,200,300,400,500]
    ax4.set_xticks( x_labels )
    ax4.set_xticklabels(x_labels, horizontalalignment='center', fontsize=0.9*main_fontsize)
    ax4.xaxis.get_majorticklabels()[0].set_horizontalalignment('left')
    ax4.xaxis.get_majorticklabels()[-1].set_horizontalalignment('right')
    y_labels = [-0.5,-0.4,-0.3,-0.2,-0.1,0.0,0.1,0.2,0.3,0.4,0.5]
    ax4.set_yticks( y_labels )
    ax4.set_yticklabels(y_labels, horizontalalignment='right', fontsize=0.9*main_fontsize)
    ax4.yaxis.get_majorticklabels()[0].set_verticalalignment('bottom')
    ax4.yaxis.get_majorticklabels()[-1].set_verticalalignment('top')
    # title:
    ax4.text( 0.01,1.04,'d) CMB lensing reconstruction spectrum with Planck data', horizontalalignment='left', transform=ax4.transAxes, fontsize=main_fontsize)

    ##############################
    # Supernovae:
    ##############################
    ax = plt.subplot(gs[2,0])
    # rescale the SN by the reference frame:
    z_hel = _sn_data[:,1]
    z_cmb = _sn_data[:,0]
    # get the data (corrected for Heliocentric motion):
    mb    = _sn_data[:,3]-np.mean(_sn_data[:,3])-5.0*np.log10( (1.0+z_hel)*(1.0+z_cmb) )
    # get the error bar:
    dmb   = _sn_data[:,4]
    # get the interpolations:
    _reference_DL = interp1d( _ref_background[:-1,1], 5.*np.log10(_ref_background[:-1,4]), kind='cubic' )
    _reference_DA = interp1d( _ref_background[:-1,1], 5.*np.log10(_ref_background[:-1,5]), kind='cubic' )
    _comp_DL = interp1d( _comp_background[:-1,1], 5.*np.log10(_comp_background[:-1,4]), kind='cubic' )
    _comp_DA = interp1d( _comp_background[:-1,1], 5.*np.log10(_comp_background[:-1,5]), kind='cubic' )
    # plot the residual:
    mb_reference = _reference_DA(z_cmb)-np.mean(_reference_DL(z_cmb))
    ax.errorbar( z_cmb, (mb-mb_reference), yerr=dmb, fmt='.', c=colormap[1], lw=1., zorder=1 )
    # plot the prediction:
    _z = np.linspace( 0.001, 8., 1000 )
    theory_mb_reference = _reference_DA(_z)-np.mean(_reference_DL(z_cmb))
    theory_mb_comp      = _comp_DA(_z)-np.mean(_comp_DL(z_cmb))
    ax.plot( _z, (theory_mb_comp-theory_mb_reference), c=colormap[0], lw=1.2 )
    ax.axhline( 0., color='k', lw=1., zorder=1 )
    # scale:
    ax.set_xscale('log')
    ax.set_xlim([ 0.001, 8. ])
    #ax.set_ylim([-1.,1.])
    ax.set_ylim([-0.2,0.2])
    ax.set_xlabel('$z$', fontsize=main_fontsize)
    ax.set_ylabel('magnitude residual', fontsize=main_fontsize)
    # label:
    x_labels = [0.001,0.01, 0.1, 1, 2.5, 8.]
    ax.set_xticks( x_labels )
    ax.set_xticklabels(x_labels, horizontalalignment='center', fontsize=0.9*main_fontsize)
    ax.xaxis.get_majorticklabels()[0].set_horizontalalignment('left')
    ax.xaxis.get_majorticklabels()[-1].set_horizontalalignment('right')
    #y_labels = [-1.,-0.75,-0.5,-0.25,0.0,0.25,0.5,0.75,1.]
    y_labels = [-0.2,-0.1,0.0,0.1,0.2]
    ax.set_yticks( y_labels )
    ax.set_yticklabels(y_labels, horizontalalignment='right', fontsize=0.9*main_fontsize)
    ax.yaxis.get_majorticklabels()[0].set_verticalalignment('bottom')
    ax.yaxis.get_majorticklabels()[-1].set_verticalalignment('top')
    # title:
    ax.text( 0.01,1.04,'e) SN Hubble diagram with Pantheon data', horizontalalignment='left', transform=ax.transAxes, fontsize=main_fontsize)

    ##############################
    # BAO:
    ##############################
    ax = plt.subplot(gs[2,1])
    # interpolate theory prediction:
    _reference_DVoRs = interp1d( _ref_background[:-1,1] , _ref_background[:-1,6], kind='cubic' )
    _comp_DVoRs      = interp1d( _comp_background[:-1,1], _comp_background[:-1,6], kind='cubic' )
    _reference_DMoRs = interp1d( _ref_background[:-1,1] , _ref_background[:-1,7], kind='cubic' )
    _comp_DMoRs      = interp1d( _comp_background[:-1,1], _comp_background[:-1,7], kind='cubic' )
    _reference_HoRs  = interp1d( _ref_background[:-1,1] , _ref_background[:-1,8], kind='cubic' )
    _comp_HoRs       = interp1d( _comp_background[:-1,1], _comp_background[:-1,8], kind='cubic' )
    # get the BAO data DV/rs:
    data_z = [0.106,0.15]
    data   = [1./(0.336/1.027369826), 4.465666]
    ddata  = [0.015/(0.336/1.02736982)**2,0.1681350]
    # plot the theoretical prediction:
    z = np.linspace( 0.01, 0.2, 1000 )
    ax.plot(z, (_comp_DVoRs(z)-_reference_DVoRs(z))/_reference_DVoRs(z), c=colormap[4], lw=1.2, label='$D_V/r_s$')
    # plot the residual:
    ax.errorbar( data_z, (data-_reference_DVoRs(data_z))/_reference_DVoRs(data_z), yerr=ddata/_reference_DVoRs(data_z), fmt='.', c=colormap[6], lw=1., zorder=1, label='$D_V/r_s$' )
    # get the BAO data DM/rs:
    _r_fid = 147.78
    data_z = [0.38,0.51,0.61]
    data   = [1512.39/_r_fid,1975.22/_r_fid,2306.68/_r_fid]
    ddata  = [np.sqrt(22.**2+11.**2)/_r_fid,np.sqrt(27.**2+14.**2)/_r_fid,np.sqrt(33.**2+17.**2)/_r_fid]
    # plot the theoretical prediction:
    z = np.linspace( 0.2, 2., 1000 )
    ax.plot(z, (_comp_DMoRs(z)-_reference_DMoRs(z))/_reference_DMoRs(z), c=colormap[0], lw=1., label='$D_M/r_s$')
    # plot the residual:
    ax.errorbar( data_z, (data-_reference_DMoRs(data_z))/_reference_DMoRs(data_z), yerr=ddata/_reference_DMoRs(data_z), fmt='.', c=colormap[1], lw=1., zorder=1, label='$D_M/r_s$' )
    # get the BAO data H/rs:
    _r_fid = 147.78
    data_z = np.array([0.38,0.51,0.61])
    data   = np.array([81.2*_r_fid,90.9*_r_fid,99.0*_r_fid])
    ddata  = np.array([np.sqrt(2.2**2+1.0**2)*_r_fid,np.sqrt(2.1**2+1.1**2)*_r_fid,np.sqrt(2.2**2+1.2**2)*_r_fid])
    # plot the theoretical prediction:
    z = np.linspace( 0.2, 2., 1000 )
    ax.plot(z, (_comp_HoRs(z)-_reference_HoRs(z))/_reference_HoRs(z), c=colormap[2], lw=1., label='$H r_s$')
    # plot the residual:
    ax.errorbar( data_z+0.01, (data-_reference_HoRs(data_z))/_reference_HoRs(data_z), yerr=ddata/_reference_HoRs(data_z), fmt='.', c=colormap[3], lw=1., zorder=1, label='$H r_s$' )
    # cut:
    ax.axvline(0.2,color='k',lw=1.)
    ax.axhline(0.0,color='k',lw=1.)
    # scale:
    ax.set_xscale('log')
    ax.set_xlim([ 0.01, 2. ])
    ax.set_ylim([-0.1,0.1])
    ax.set_xlabel('$z$', fontsize=main_fontsize)
    ax.set_ylabel('$\\Delta (D/r_s) / (D/r_s)$', fontsize=main_fontsize)
    # label:
    x_labels = [0.01, 0.1, 1, 2.]
    ax.set_xticks( x_labels )
    ax.set_xticklabels(x_labels, horizontalalignment='center', fontsize=0.9*main_fontsize)
    ax.xaxis.get_majorticklabels()[0].set_horizontalalignment('left')
    ax.xaxis.get_majorticklabels()[-1].set_horizontalalignment('right')
    y_labels = [-0.1,-0.075,-0.05, -0.025, 0.0, 0.025, 0.05, 0.075, 0.1]
    ax.set_yticks( y_labels )
    ax.set_yticklabels(y_labels, horizontalalignment='right', fontsize=0.9*main_fontsize)
    ax.yaxis.get_majorticklabels()[0].set_verticalalignment('bottom')
    ax.yaxis.get_majorticklabels()[-1].set_verticalalignment('top')
    # title:
    ax.text( 0.01,1.04,'f) BAO distance ladder with SDSS BOSS DR12, MGS and 6DF data', horizontalalignment='left', transform=ax.transAxes, fontsize=main_fontsize)
    # legend:
    ax.legend(framealpha=1.,loc='upper left',fontsize=main_fontsize,fancybox=True,edgecolor='k', ncol=2)

    ##############################
    # WEYL potential:
    ##############################
    ax = plt.subplot(gs[3,0])
    _reference_weyl_1 = interp1d( _ref_transfer_1[:,0], _ref_transfer_1[:,9], bounds_error=False, kind='cubic' )
    _comp_weyl_1      = interp1d( _comp_transfer_1[:,0], _comp_transfer_1[:,9], bounds_error=False, kind='cubic' )
    _reference_weyl_2 = interp1d( _ref_transfer_2[:,0], _ref_transfer_2[:,9], bounds_error=False, kind='cubic' )
    _comp_weyl_2      = interp1d( _comp_transfer_2[:,0], _comp_transfer_2[:,9], bounds_error=False, kind='cubic' )
    _reference_weyl_3 = interp1d( _ref_transfer_3[:,0], _ref_transfer_3[:,9], bounds_error=False, kind='cubic' )
    _comp_weyl_3      = interp1d( _comp_transfer_3[:,0], _comp_transfer_3[:,9], bounds_error=False, kind='cubic' )

    _k = np.logspace(
                     np.log10(max(np.amin(_comp_transfer_2[:,0]), np.amin(_ref_transfer_2[:,0]))),
                     np.log10(min(np.amax(_comp_transfer_2[:,0]), np.amax(_ref_transfer_2[:,0]),1.)), 1000 )
    ax.plot( _k, (_comp_weyl_1(_k)-_reference_weyl_1(_k))/_reference_weyl_1(_k), c=colormap[0], label='z=0.5', lw=1.2 )
    ax.plot( _k, (_comp_weyl_2(_k)-_reference_weyl_2(_k))/_reference_weyl_2(_k), c=colormap[1], label='z=1.0', lw=1.2 )
    ax.plot( _k, (_comp_weyl_3(_k)-_reference_weyl_3(_k))/_reference_weyl_3(_k), c=colormap[2], label='z=1.5', lw=1.2 )
    ax.axhline( 0., color='k', lw=1., zorder=1 )
    # scale:
    ax.set_xlim([ 1.e-5, 0.1 ])
    ax.set_xscale('log')
    ax.set_xlabel('$k$')
    ax.set_ylabel('$\\Delta W(k) / W(k)$')
    # label:
    x_labels = [1.e-5,1.e-4,1.e-3,1.e-2,1.e-1]
    ax.set_xticks( x_labels )
    ax.set_xticklabels(x_labels, horizontalalignment='center', fontsize=0.9*main_fontsize)
    ax.xaxis.get_majorticklabels()[0].set_horizontalalignment('left')
    ax.xaxis.get_majorticklabels()[-1].set_horizontalalignment('right')
    # legend:
    ax.legend(framealpha=1.,fontsize=main_fontsize,fancybox=True,edgecolor='k')
    # title:
    ax.text( 0.01,1.04,'g) Weyl potential', horizontalalignment='left', transform=ax.transAxes, fontsize=main_fontsize)

    ##############################
    # Matter power spectrum:
    ##############################
    ax = plt.subplot(gs[3,1])
    _reference_delta_1 = interp1d( _ref_transfer_1[:,0], _ref_transfer_1[:,6], bounds_error=False, kind='cubic' )
    _comp_delta_1      = interp1d( _comp_transfer_1[:,0], _comp_transfer_1[:,6], bounds_error=False, kind='cubic' )
    _reference_delta_2 = interp1d( _ref_transfer_2[:,0], _ref_transfer_2[:,6], bounds_error=False, kind='cubic' )
    _comp_delta_2      = interp1d( _comp_transfer_2[:,0], _comp_transfer_2[:,6], bounds_error=False, kind='cubic' )
    _reference_delta_3 = interp1d( _ref_transfer_3[:,0], _ref_transfer_3[:,6], bounds_error=False, kind='cubic' )
    _comp_delta_3      = interp1d( _comp_transfer_3[:,0], _comp_transfer_3[:,6], bounds_error=False, kind='cubic' )
    _k = np.logspace(
                     np.log10(max(np.amin(_comp_transfer_2[:,0]), np.amin(_ref_transfer_2[:,0]))),
                     np.log10(min(np.amax(_comp_transfer_2[:,0]), np.amax(_ref_transfer_2[:,0]),1.)), 1000 )
    ax.plot( _k, (_comp_delta_1(_k)-_reference_delta_1(_k))/_reference_delta_1(_k), c=colormap[0], label='z=0.5', lw=1.2 )
    ax.plot( _k, (_comp_delta_2(_k)-_reference_delta_2(_k))/_reference_delta_2(_k), c=colormap[1], label='z=1.0', lw=1.2 )
    ax.plot( _k, (_comp_delta_3(_k)-_reference_delta_3(_k))/_reference_delta_3(_k), c=colormap[2], label='z=1.5', lw=1.2 )
    ax.axhline( 0., color='k', lw=1., zorder=1 )
    # scale:
    ax.set_xlim([ 1.e-5, 0.1 ])
    ax.set_xscale('log')
    ax.set_xlabel('$k$')
    ax.set_ylabel('$\\Delta P(k) / P(k)$')
    # label:
    x_labels = [1.e-5,1.e-4,1.e-3,1.e-2,1.e-1]
    ax.set_xticks( x_labels )
    ax.set_xticklabels(x_labels, horizontalalignment='center', fontsize=0.9*main_fontsize)
    ax.xaxis.get_majorticklabels()[0].set_horizontalalignment('left')
    ax.xaxis.get_majorticklabels()[-1].set_horizontalalignment('right')
    # legend:
    ax.legend(framealpha=1.,fontsize=main_fontsize,fancybox=True,edgecolor='k')
    # title:
    ax.text( 0.01,1.04,'h) Matter power spectrum', horizontalalignment='left', transform=ax.transAxes, fontsize=main_fontsize)
    # update dimensions:
    bottom=0.03; top=0.98; left=0.06; right=0.99; wspace=0.2; hspace=0.2
    gs.update( bottom=bottom, top=top, left=left, right=right, wspace=wspace, hspace=hspace )
    # save figure:
    plt.savefig(out_dir+'/'+root_ref+'_vs_'+root_comp+'.pdf')
    # close:
    plt.clf()

#########################
# cycle and do the plots:

# all of them against a single root:
if False:
    reference = '1_lcdm'
    roots     = sorted( [ _name.replace('_params.ini','') for _name in os.listdir(spectra_dir) if '_params.ini' in _name ] )
    for _r in roots:
        if _r!=reference:
            print color_print.bold('Doing: '+_r)
            helper_plotter( root_ref=reference, root_comp=_r )
else:
    test_roots = []
    for _ref,_test in test_roots:
        print color_print.bold('Doing: '+_ref+' vs '+_test)
        helper_plotter( root_ref=_ref, root_comp=_test )

pass
