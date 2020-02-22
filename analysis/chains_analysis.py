# -*- coding: utf-8 -*-

"""
Perform all sort of tests on a single chain
"""

# import global settings:
from settings import *
from utilities import *
from import_chains import *

# some feedback:
print color_print.bold( '**********************************************************' )
print color_print.bold( '** Chains analysis                                      **' )
print color_print.bold( '**********************************************************' )

# output file:
out_dir = results_dir+'/chains_analysis'
if not os.path.exists(out_dir): os.mkdir(out_dir)

# set up feedback:
if __name__ == "__main__":
    sys.stdout = Logger(out_dir+'/log.txt')

# parameters for triangle plots:
triangle_paramnames = [ 'omegabh2', 'omegach2', 'thetastar', 'tau', 'logA', 'ns', 'H0', 'omegam', 'sigma8', 'rdrag', 'kd',
                        'omegabh2_1', 'omegach2_1', 'thetastar_1', 'tau_1', 'logA_1', 'ns_1', 'H0_1', 'omegam_1', 'sigma8_1', 'rdrag_1', 'kd_1',
                        'omegabh2_2', 'omegach2_2', 'thetastar_2', 'tau_2', 'logA_2', 'ns_2', 'H0_2', 'omegam_2', 'sigma8_2', 'rdrag_2', 'kd_2',]

# do the analysis only if called directly:
if __name__ == "__main__":
    # directory with chains:
    chains_dir = here+'/import_chains_sn.cache'
    # import chains:
    chains     = import_chains(chains_dir=chains_dir)
    # run basic analysis:
    for name in sorted( chains ):
        chain = chains[name]
        # feedback:
        print color_print.green( 'Doing chain: '+chain.identifier )
        #
        try:
            # compute the covariance:
            try:
                chain.samples.writeCovMatrix()
            except Exception,e:
                print '\033[93m'+'WARNING'+'\033[0m'
                print e
            # compute the correlation:
            try:
                chain.samples.writeCorrelationMatrix()
            except Exception,e:
                print '\033[93m'+'WARNING'+'\033[0m'
                print e
            # check output folder:
            out_folder = out_dir+'/'+chain.dirname
            if not os.path.exists(out_folder): os.mkdir(out_folder)
            ########################################################################
            # Statistical analysis
            ########################################################################
            # write marginal statistics:
            chain.samples.getMargeStats().saveAsText( out_folder+'/'+chain.name+'.margestats' )
            # write global likelihood stats:
            chain.samples.getLikeStats().saveAsText( out_folder+'/'+chain.name+'.likestats')
            # convergence:
            chain.samples.getConvergeTests( what=['MeanVar', 'GelmanRubin','SplitTest','CorrLengths'],
                                            writeDataToFile=True, filename=out_folder+'/'+chain.name+'.converge_stats' );
            print color_print.bold( '  R-1 = '+str('{}'.format(nice_number( chain.samples.GelmanRubin, digits=2 )) ) )
            ########################################################################
            # Plot with confidence intervals
            ########################################################################
            # plot the 1D with all parameters:
            g    = gplot.getSubplotPlotter();
            plot = g.plots_1d( chain.samples, share_y=True, colors=[nice_colors(0)], lws=[1.5] );
            # plot sigma intervals and best fit / mean / sample best fit:
            marge_stats = chain.samples.getMargeStats(include_bestfit=False)
            like_stats  = chain.samples.getLikeStats()
            for num,par in enumerate(chain.samples.getParamNames().list()):
                # get the subplot:
                ax = g.subplots[ num//g.plot_col, num % g.plot_col]
                # get low and upper bounds and plot shade:
                ax.axvspan( marge_stats.parWithName(par).limits[1].lower,
                            marge_stats.parWithName(par).limits[1].upper, alpha=0.1, color=nice_colors(1) )
                ax.axvspan( marge_stats.parWithName(par).limits[0].lower,
                            marge_stats.parWithName(par).limits[0].upper, alpha=0.2, color=nice_colors(1) )
                ax.axvline( x=marge_stats.parWithName(par).mean, color=nice_colors(1), ls='-' )
                ax.axvline( x=like_stats.parWithName(par).bestfit_sample, color=nice_colors(2), ls='--' )
                if chain.minimum is not None:
                    try:
                        ax.axvline( x=chain.minimum.parWithName(par).best_fit, color=nice_colors(3), ls='-.' )
                    except Exception,e:
                        print '\033[93m'+'WARNING could not find best fit parameter '+par+'\033[0m'
                        print e
            # the legend:
            loc    = 'lower center'
            names  = ['1D', 'best gaussian approximation','mean','sample best-fit','prior']
            colors = [nice_colors(0), nice_colors(0), nice_colors(1), nice_colors(2),'k']
            if chain.minimum is not None:
                names.append('best-fit')
                colors.append(nice_colors(3))
            leg_handlers = [ plt.Line2D((0,1),(0,0), color=col ) for col in colors ]
            leg = g.fig.legend( handles  = leg_handlers, labels   = names, frameon   = True, fancybox  = False,
                                edgecolor = 'k', ncol      = len(names), borderaxespad = 0.0, columnspacing = 4.0,
                                handlelength = 1.5, loc = loc, title=chain.name.replace('_',' ') )

            # export:
            g.export( out_folder+'/'+chain.name+'_1D.pdf' )
            # close:
            plt.close('all')
            ########################################################################
            # Triangle plot:
            ########################################################################
            # get the parameter names to plot:
            parameter_names = [ _name for _name in chain.samples.getParamNames().list() if _name in triangle_paramnames ]
            # do the plot:
            g    = gplot.getSubplotPlotter();
            plot = g.triangle_plot( chain.samples, params=parameter_names, filled=True )
            # export:
            g.export( out_folder+'/'+chain.name+'_tri.pdf' )
            # close:
            plt.close('all')
            ########################################################################
            # Plot with different chains for convergence
            ########################################################################
            # plot the 1D with all parameters:
            g    = gplot.getSubplotPlotter();
            # get the names of parameters:
            param_names = chain.samples.getParamNames()
            param_names = param_names.parsWithNames(param_names.list())
            _label      = [ _name.label for _name in param_names ]
            _name       = [ _name.name for _name in param_names ]
            _ranges     = {}
            for _n in _name:
                _ranges[_n] = [chain.samples.ranges.lower[_n],chain.samples.ranges.upper[_n]]
            # separate the chains:
            separate_chains     = chain.samples.getSeparateChains()
            num_separate_chains = len(separate_chains)
            _separate_chains = []
            for _samps in separate_chains:
                _separate_chains.append( gsamp.MCSamples( samples=_samps.samples, weights=_samps.weights,
                                                          loglikes=_samps.loglikes, names=_name, labels=_label,
                                                          settings=analysis_settings, ranges=_ranges ) )
            #
            num_chains = len(_separate_chains)
            # plot:
            _plot_chains = _separate_chains+[chain.samples]
            _line_ws     = [1. for _ in xrange(num_chains) ]+[2.]
            _labels      = ['chain '+str(_+1) for _ in xrange(num_chains) ]+[chain.name.replace('_',' ')]
            plot = g.plots_1d( _plot_chains, share_y=True, lws=_line_ws, legend_labels=_labels, legend_ncol=4 );
            # best fit and mean:
            like_stats  = chain.samples.getLikeStats()
            for num,par in enumerate(chain.samples.getParamNames().list()):
                # get the subplot:
                ax = g.subplots[ num//g.plot_col, num % g.plot_col]
                # get low and upper bounds and plot shade:
                ax.axvline( x=marge_stats.parWithName(par).mean, color=nice_colors(1), ls='-' )
                ax.axvline( x=like_stats.parWithName(par).bestfit_sample, color=nice_colors(2), ls='--' )
                if chain.minimum is not None:
                    try:
                        ax.axvline( x=chain.minimum.parWithName(par).best_fit, color=nice_colors(3), ls='-.' )
                    except Exception,e:
                        print '\033[93m'+'WARNING could not find best fit parameter '+par+'\033[0m'
                        print e
            # the legend:
            loc    = 'lower center'
            names  = ['mean','sample best-fit']
            colors = [nice_colors(1), nice_colors(2)]
            if chain.minimum is not None:
                names.append('best-fit')
                colors.append(nice_colors(3))
            leg_handlers = [ plt.Line2D((0,1),(0,0), color=col ) for col in colors ]
            leg = g.fig.legend( handles  = leg_handlers, labels   = names, frameon   = True, fancybox  = False,
                                edgecolor = 'k', ncol      = len(names), borderaxespad = 0.0, columnspacing = 4.0,
                                handlelength = 1.5, loc = loc, title=chain.name.replace('_',' ') )
            # export:
            g.export( out_folder+'/'+chain.name+'_convergence_1D.pdf' )
            # close:
            plt.close('all')

        except Exception,e:
            print '\033[93m'+'WARNING'+'\033[0m'
            print e
