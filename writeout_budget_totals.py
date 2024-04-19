# so script will run without X
import matplotlib as mpl
mpl.use('Agg')

# use modules
import sys as sys
sys.path.append('../modules/')

from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import netCDF4
#from mpl_toolkits.basemap import Basemap, shiftgrid, cm
import csv
import sys
import os


JASMIN=True
jobid=sys.argv[1] 
disk=sys.argv[2]

if JASMIN: 
  geovols='/gws/nopw/j04/ukca_vol2/ptg21/geovols/geovol_192x144x85.nc'
  outdir='/home/users/ptg21/output/'+jobid+'/'

if not os.path.exists(outdir):
      os.makedirs(outdir)

volfile  = netCDF4.Dataset(geovols)
lat      = volfile.variables['latitude'][:]
vol      = volfile.variables['vol_theta'][:] # m3
vol      = vol*1E6   # cm-3

filename=disk+jobid+'_trop_mask.nc'
print(filename)
ncfiletm      = netCDF4.Dataset(filename)
tropmask = ncfiletm.variables['trop_mask']
lons         = ncfiletm.variables['longitude']
lats         = ncfiletm.variables['latitude']
hybrid_ht   = ncfiletm.variables['level_height']
try:
    times2       = ncfiletm.variables['t']
except:
    times2       = ncfiletm.variables['time']
nyears = len(times2)

filename=disk+jobid+'_o3.nc'
ncfileo3      = netCDF4.Dataset(filename)
o3 = ncfileo3.variables['o3'][:]

#
# prod
#

filename=disk+jobid+'_ox_prod.nc'
print(filename)
ncfile2      = netCDF4.Dataset(filename)

ho2no = ncfile2.variables['ox_prod_ho2_no']
nmonths,nlevs,nlats,nlons = np.shape(ho2no)
meo2no = ncfile2.variables['ox_prod_meoo_no']
ro2no = ncfile2.variables['ox_prod_no_ro2']
ohrcooh = ncfile2.variables['ox_prod_oh_inorgacid']
ohrono2 = ncfile2.variables['ox_prod_oh_orgnitrate']
hvrono2 = ncfile2.variables['ox_prod_orgnitrate_photol']
ohpan = ncfile2.variables['ox_prod_oh_panrxns']
jo2 = ncfile2.variables['jo2']

print("trop prod")
p1 = ho2no[:] * tropmask[:]  
p2 = meo2no[:] *  tropmask[:]
p3 = ro2no[:]  * tropmask[:]
p4 = ohrcooh[:] * tropmask[:]
p5 = ohrono2[:] * tropmask[:]
p6 = hvrono2[:] * tropmask[:]
p7 = ohpan[:] * tropmask[:]
p8 = jo2[:] * tropmask[:]

ho2no_tot   = np.sum(p1*0.048*360.*3600.*24.,axis=(1,2,3))
meo2no_tot  = np.sum(p2*0.048*360.*3600.*24.,axis=(1,2,3))
ro2no_tot   = np.sum(p3*0.048*360.*3600.*24.,axis=(1,2,3))
ohrcooh_tot = np.sum(p4*0.048*360.*3600.*24.,axis=(1,2,3))
ohrono2_tot = np.sum(p5*0.048*360.*3600.*24.,axis=(1,2,3))
hvrono2_tot = np.sum(p6*0.048*360.*3600.*24.,axis=(1,2,3))
ohpan_tot   = np.sum(p7*0.048*360.*3600.*24.,axis=(1,2,3))
jo2_tot     = np.sum(p8*0.048*360.*3600.*24.,axis=(1,2,3))
netp = p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8

#
# loss
#

filename=disk+jobid+'_ox_loss.nc'
print(filename)
ncfile3     = netCDF4.Dataset(filename)

print("trop loss")
o1dh2o = ncfile3.variables['ox_loss_o1d_h2o'][:]
mlr    = ncfile3.variables['ox_loss_minor_rxns'][:]
ho2o3  = ncfile3.variables['ox_loss_ho2_o3'][:]
oho3   = ncfile3.variables['ox_loss_oh_o3'][:]
o3alk  = ncfile3.variables['ox_loss_o3_alkene'][:]
n2o5h2o= ncfile3.variables['ox_loss_n2o5_h2o'][:]
no3loss= ncfile3.variables['ox_loss_no3_chemloss'][:]

l1 = o1dh2o*tropmask
l2 = mlr*tropmask
l3 = ho2o3*tropmask
l4 = oho3*tropmask
l5 = o3alk*tropmask
l6 = n2o5h2o*tropmask
l7 = no3loss*tropmask

o1d_tot     = np.sum(l1*0.048*360*3600.*24.,axis=(1,2,3))
mlr_tot     = np.sum(l2*0.048*360*3600.*24.,axis=(1,2,3))
ho2o3_tot   = np.sum(l3*0.048*360*3600.*24.,axis=(1,2,3))
oho3_tot    = np.sum(l4*0.048*360*3600.*24.,axis=(1,2,3))
o3alk_tot   = np.sum(l5*0.048*360*3600.*24.,axis=(1,2,3))
n2o5h2o_tot = np.sum(l6*0.048*360*3600.*24.,axis=(1,2,3))
no3loss_tot = np.sum(l7*0.048*360*3600.*24.,axis=(1,2,3))
netl = l1 + l2 + l3 + l4 + l5 + l6 + l7

o3loss_tot  = np.sum(netl*0.048*360.*3600.*24.,axis=(1,2,3))
o3prod_tot  = np.sum(netp*0.048*360.*3600.*24.,axis=(1,2,3))


burden =  np.zeros(nyears)
filename = disk+jobid+'_trop_air_mass.nc'
ncfileam     = netCDF4.Dataset(filename)
airmass = ncfileam.variables['aimass_trop']
burden = o3[:]*tropmask[:]*airmass[:]

import pylab as plt2
bdn_tmp = np.sum(burden[:,:,:,:], axis=(1,2,3))/1e9
plt2.savetxt(outdir+jobid+'_bdn.csv',bdn_tmp)

csvfile = outdir+jobid+"_o3_budget"+".csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(["PROD", "LOSS", "BURDEN"])
    for iyear in range(0, nyears):
        writer.writerow([o3prod_tot[iyear], o3loss_tot[iyear], bdn_tmp[iyear]])

csvfile = outdir+jobid+"_o3_budget_terms"+".csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(["TOT_L","O1D_H2O", "MLR", "HO2_O3","OH_O3","O3_ALK","N2O5_H2O","NO3_LOSS","TOT_P","HO2_NO","MeO2_NO","RO2_NO","OH_RCOOH","OH_RONO2","NIT_PHOT","OH_PAN","JO2"])
    for imonth in range(0, nmonths):
        writer.writerow([
          o3loss_tot[imonth], o1d_tot [imonth],  mlr_tot[imonth],     ho2o3_tot[imonth], oho3_tot[imonth],    o3alk_tot[imonth],   n2o5h2o_tot[imonth], no3loss_tot[imonth],
          o3prod_tot[imonth], ho2no_tot[imonth], meo2no_tot[imonth], ro2no_tot[imonth], ohrcooh_tot[imonth], ohrono2_tot[imonth], hvrono2_tot[imonth], ohpan_tot[imonth], jo2_tot[imonth]])
