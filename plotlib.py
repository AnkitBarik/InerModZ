#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.colors as colors

def get_grid2D(theta, phi):

    nphi  = len(phi)
    ntheta = len(theta)
    p2D  = np.zeros([nphi, ntheta])
    th2D = np.zeros([nphi, ntheta])

    for i in range(nphi):
        p2D[i,:] = phi[i]

    for j in range(ntheta):
        th2D[:, j] = theta[j]

    return p2D, th2D


def radContour(theta, phi, data, idxPlot, grid, levels, cm, proj):

    data = data[..., idxPlot]

    p2D, th2D = get_grid2D(theta, phi)

    p2D = p2D - np.pi
    th2D= np.pi/2 - th2D

    lon = p2D * 180./np.pi
    lat = th2D * 180./np.pi

    if proj == "ortho":
        fig = plt.figure(figsize=(10, 10))
        plotcrs = ccrs.Orthographic(0, 40)
    elif proj == "moll":
        fig = plt.figure(figsize=(12, 10))
        plotcrs = ccrs.Mollweide()

    ax = fig.add_subplot(1, 1, 1, projection=plotcrs)

    datMax = (np.abs(data)).max()
    divnorm = colors.TwoSlopeNorm(vmin=-datMax, vcenter=0, vmax=datMax)

    if grid:
        ax.gridlines(linewidth=1, color='gray', alpha=0.5, linestyle=':')

    if proj == "ortho":
        cont = ax.pcolormesh(lon, lat, data, \
                           transform=ccrs.PlateCarree(), cmap=cm, \
                           norm=divnorm)
    elif proj == "moll":
        cont = ax.contourf(lon, lat, data, levels, \
                           transform=ccrs.PlateCarree(), cmap=cm, \
                           norm=divnorm)


        for c in cont.collections:
            c.set_edgecolor("face")

#        if vec:
#            ut = self.U.Us*cos(self.grid.th3D) - self.U.Uz*sin(self.grid.th3D)
#            ut = ut[::vecStride,::vecStride,idxPlot]
#            up = self.U.Up[::vecStride,::vecStride,idxPlot]
#            lon = lon[::vecStride,::vecStride]
#            lat = lat[::vecStride,::vecStride]
#            #ax.quiver(lon,lat,up,ut,transform=plotcrs,width=vecWidth,scale=vecScale,regrid_shape=20)
#            ax.quiver(lon,lat,up,ut,transform=plotcrs)#,regrid_shape=regrid_shape)

    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()

def merContour(r, theta, data, levels, cm):

    rr, tth = np.meshgrid(r, theta)

    xx = rr*np.sin(tth)
    yy = rr*np.cos(tth)

    plt.figure(figsize=(5, 10))

    datMax = (np.abs(data)).max()
    divnorm = colors.TwoSlopeNorm(vmin=-datMax, vcenter=0, vmax=datMax)

    cont = plt.contourf(xx, yy, data, levels, cmap=cm, norm=divnorm)

    plt.plot(r[0]*np.sin(theta), r[0]*np.cos(theta), 'k', lw=1)
    plt.plot(r[-1]*np.sin(theta), r[-1]*np.cos(theta), 'k', lw=1)
    plt.plot([0, 0], [ r.min(), r.max() ], 'k', lw=1)
    plt.plot([0, 0], [ -r.max(), -r.min() ], 'k', lw=1)

    for c in cont.collections:
        c.set_edgecolor("face")

    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()

def eqContour(r, phi, data, levels, cm):

    phi2D, r2D = np.meshgrid(phi, r, indexing='ij')
    xx = r2D * np.cos(phi2D)
    yy = r2D * np.sin(phi2D)

    plt.figure(figsize=(10, 10))

    datMax = (np.abs(data)).max()
    divnorm = colors.TwoSlopeNorm(vmin=-datMax, vcenter=0, vmax=datMax)
    cont = plt.contourf(xx, yy, data, levels, cmap=cm, norm=divnorm)

    plt.plot(r[0]*np.cos(phi), r[0]*np.sin(phi), 'k', lw=1)
    plt.plot(r[-1]*np.cos(phi), r[-1]*np.sin(phi), 'k', lw=1)

    for c in cont.collections:
        c.set_edgecolor("face")

    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()

def surface3D(x,y,z,idx,ux,uy,uz,dat,cm='seismic',quiv=True,fac=0.01,col=True):

    from mayavi import mlab

    lut=eval('plt.cm.'+cm+'(np.linspace(0,1,255))*255')
   
    if col: 
        col = (0.43, 0.43, 0.43)
    else:
        col = None
    mlab.figure(size=(800, 800))
    mesh_handle = mlab.mesh(x[..., idx], y[..., idx], z[..., idx], scalars=dat[..., idx])
    mesh_handle.module_manager.scalar_lut_manager.lut.table = lut
#    mesh_handle.module_manager.scalar_lut_manager.reverse_lut = True
    if quiv:
        mlab.quiver3d(x, y, z, ux, uy, uz, color=col, scale_mode='vector', mode='arrow', mask_points=4, scale_factor=fac)
    #mlab.show()
    mlab.draw()
