# -*- coding: utf-8 -*-

" Preliminary setup "

import numpy as np
import sys
import os

import platform
import six
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning, module='.*/IPython/.*')

import camb
import getdist.paramnames as gpnames

class tension_plots(object):

    def __init__(self):

        return

    " Analysis "
    def load_param_names(self, filename):
        """
        Load the list of parameter names
        """
        import getdist.paramnames as gpnames
        gnames = gpnames.ParamNames(fileName=filename)
        return gnames.list()

    def param_indices(self, num_copies):
        """
        Determine the number of parameter copies,
        so that the parameter indices cen be properly accounted for
        """
        if (num_copies==0 or num_copies==1):
            return []
        else:
            return np.arange(1,num_copies+1)

    def number_of_copies(self, filename):
        """
        Determine the number of parameter copies from a .paramnames file
        """
        gnames = gpnames.ParamNames(fileName=filename)

        copies=False
        if gnames.list()[0][-2:]=='_1': copies=True
        # calculate number of copies in the file
        num=0
        if copies:
            j=0
            for i in range(len(gnames.list())):
                inew = gnames.list()[i][-1]
                if inew>j:
                    num += 1
                    j = inew
                else:
                    break
        return num

    def rename_params(self, file_in, file_out, rename_indx):
        """
        Renames parameter copy ending in index "rename_indx"
        - file_in is the original .paramnames file with all copies,
        - file_out is the final .paramnames file without the indices "rename_indx"
        """
        if file_in.endswith(".paramnames"):
            file_read = file_in
            gnames = gpnames.ParamNames(fileName=file_read)
        elif file_in.endswith(".ranges"):
            length = len(file_in) - len('ranges')
            file_read = file_in[:length]+'paramnames'
            gnames = gpnames.ParamNames(fileName=file_read)

        with open(file_in, "rt") as fin:
            with open(file_out, "wt") as fout:
                i=0
                for line in fin:
                    pname = gnames.list()[i]
                    if ( line[:len(pname)]==pname and
                         line[:len(pname)][-2:]=='_'+str(rename_indx) ):
                        newline = line.replace(line[:len(pname)], line[:len(pname)-2])
                        fout.write(newline)
                    else:
                        fout.write(line)
                    i+=1
        return

    def load_and_split_paramnames(self, chain_dir=None, root=None):
        """
        Load the .paramnames files and generate more directories by
        splitting the parameter copies and renaming them (i.e. removing indices)
        """
        from shutil import copyfile

        # path to chains and chain names
        if chain_dir[-1] is not '/': chain_dir+='/'
        filename = chain_dir+root

        # load .paramnames file
        gnames = gpnames.ParamNames(fileName=filename)
        # get number of copies
        Ncopies = self.number_of_copies(filename+'.paramnames')
        # now get the indices
        indx = self.param_indices(Ncopies)

        # check if we need to create new folders,
        # then check if the folders already exist,
        # and, if not, create them
        new_dirs = []; new_chains_txt = []
        if Ncopies>1:
            for i in range(Ncopies):
                new_folder = chain_dir+root+'_copy'+str(indx[i])+'/'
                new_dirs.append(new_folder)
                new_chains_txt.append(root+str(indx[i]))
                if not os.path.exists(new_folder):
                    os.makedirs(new_folder)
                for roots, dirs, files in os.walk(chain_dir):
                    l=0
                    for file in files:
                        # copy chain files
                        if (file.startswith(root) and file.endswith(".txt")):
                            l+=1
                            length = len(root)
                            new_txt = new_folder+file[:length]+str(indx[i])+'_'+str(l)+'.txt'
                            if not os.path.isfile(new_txt):
                                copyfile(chain_dir+file, new_txt)
                        # files with re-named parameters
                        elif ( file.startswith(root) and file.endswith(".paramnames") ):
                            length = len(root)
                            new_paramnames = file[:length]+str(indx[i])+'.paramnames'
                            if not os.path.isfile(new_folder+new_paramnames):
                                self.rename_params(chain_dir+file, new_folder+new_paramnames, indx[i])
                        elif (file.startswith(root) and file.endswith(".ranges")):
                            length = len(root)
                            new_ranges = file[:length]+str(indx[i])+'.ranges'
                            if not os.path.isfile(new_folder+new_ranges):
                                self.rename_params(chain_dir+file, new_folder+new_ranges, indx[i])
        return new_dirs, new_chains_txt

    def plot_triangles(self, chain_dir, roots, paramnames_full=None, analysis_settings=None, settings=None, param_3d=None, params='all',
                       filled=True, shaded=False, subplot_size_inch=2, fig_width_inch=None, Np=5,
                       solid_colors=['b','g','r'], axis_marker_lw=2.5, alpha_filled_add=0.8,
                       ignore_rows=0.5, smooth_scale_1D=0.5, smooth_scale_2D=0.5,
                       savedir=None, root_plot_name=None, params_remove=None):
        """
        Generate the triangle plots
        """
        import getdist.plots as gplot

        if settings is None:
            settings = gplot.GetDistPlotSettings(subplot_size_inch=subplot_size_inch, fig_width_inch=fig_width_inch)
            settings.solid_colors = solid_colors
            settings.axis_marker_lw = axis_marker_lw
            settings.alpha_filled_add = alpha_filled_add
            settings.alpha_factor_contour_lines = 0.5
            settings.figure_legend_frame = False
            settings.figure_legend_loc = 'Best'
            # settings.colormap = cm.viridis

        if analysis_settings is None:
            analysis_settings={'ignore_rows':ignore_rows, "smooth_scale_1D":smooth_scale_1D, "smooth_scale_2D":smooth_scale_2D}

        g = gplot.getSubplotPlotter(chain_dir=chain_dir, analysis_settings=analysis_settings, settings=settings)

        roots = roots
        if params == 'all':
            # get params without indices
            #---------------------------
            # path to chains and chain names
            if paramnames_full is None:
                if chain_dir[0][-1] is not '/': chain_dir[0]+='/'
                filename = chain_dir[0]+roots[0]+'.paramnames'
            else:
                filename = paramnames_full
            # load .paramnames file
            gnames = gpnames.ParamNames(fileName=filename)
            # get number of copies
            Ncopies = self.number_of_copies(filename)
            # now get the indices
            indx = self.param_indices(Ncopies)

            # fixed parameters, not for plotting
            if params_remove==None:
                params_remove = ['omeganuh2','w','omegal']

            # now, remove any indices, if present
            par = []
            if Ncopies>1:
                for i, name in enumerate(gnames.list()):
                    if name[:-2] not in params_remove:
                        if name[-2] == '_':
                            if name[-1] == str(1):
                                par.append(name[:-2])
                        else:
                            par.append(name)
            else:
                for i, name in enumerate(gnames.list()):
                    if name not in params_remove:
                        par.append(name)

            # only theory parameters
            params_theory = par[0:6]
            th_indx = 6

            # now, split all other parameters
            # in groups of Np
            j=th_indx
            Np_remain = len(par)-len(params_theory)
            mod = Np_remain%Np
            Ngroup = Np_remain/Np
            parlist = [params_theory]
            for i in range(Ngroup):
                parlist.append(par[j:j+Np])
                j+=Np
            # add any remaining parameters to list
            if mod is not 0:
                parlist.append(par[j:Np_remain])

        # now do the plotting
        if root_plot_name is None:
            root_plot_name='img'

        for i in range(len(parlist)):
            params = parlist[i]
            if i==0:
                savename = root_plot_name+'_theory'
                g.triangle_plot(roots, params, plot_3d_with_param=param_3d, filled=filled, shaded=shaded)
                g.export(fname=savename, adir=savedir)
            else:
                savename = root_plot_name+'_'+str(i)
                g.triangle_plot(roots, params, plot_3d_with_param=param_3d, filled=filled, shaded=shaded)
                g.export(fname=savename, adir=savedir)
        return

    def plot_compare_copies(self, chain_dir_split, root_split,
                            paramnames_full=None, analysis_settings=None, settings=None, param_3d=None, params='all',
                            filled=True, shaded=False, subplot_size_inch=2, fig_width_inch=None, Np=5,
                            solid_colors = ['b','g','r'], axis_marker_lw=2.5, alpha_filled_add=0.8,
                            ignore_rows=0.5, smooth_scale_1D=0.5, smooth_scale_2D=0.5,
                            savedir=None, root_plot_name=None, params_remove=None):
        """
        Plots copies from same run together to compare them
        """
        # split chains into copies
        new_dirs, new_txts = self.load_and_split_paramnames(chain_dir=chain_dir_split, root=root_split)

        # this is needed to be given to the routine that calculates
        # the number of copies in order to work properly
        filename_split = chain_dir_split+root_split+'.paramnames'

        # get number of copies
        Ncopies = self.number_of_copies(filename_split)

        # use new directories for plotting
        chain_dir=new_dirs
        roots = new_txts

        if analysis_settings is None:
            analysis_settings={'ignore_rows':ignore_rows, "smooth_scale_1D":smooth_scale_1D, "smooth_scale_2D":smooth_scale_2D}

        self.plot_triangles(chain_dir, roots, analysis_settings=analysis_settings, settings=settings, paramnames_full=filename_split,
                               param_3d=param_3d, params=params,
                               filled=filled, shaded=shaded, subplot_size_inch=subplot_size_inch, fig_width_inch=fig_width_inch, Np=Np,
                               solid_colors=solid_colors, axis_marker_lw=axis_marker_lw, alpha_filled_add=alpha_filled_add,
                               ignore_rows=ignore_rows, smooth_scale_1D=smooth_scale_1D, smooth_scale_2D=smooth_scale_2D,
                               savedir=savedir, root_plot_name=root_plot_name, params_remove=params_remove)
        return
