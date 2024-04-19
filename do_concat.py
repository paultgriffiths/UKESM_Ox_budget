import xarray as xr
import sys
jobid=sys.argv[1] 
disk=sys.argv[2]
for var in ['o3', 'air_mass', 'trop_air_mass', 'o3-STE' , 'ox_loss','ox_prod','o3_dry_dep_3d','noy_wet_dep_3d', 'noy_dry_dep_3d', 'trop_mask']:
  print(var)
  print('open')
  data = xr.open_mfdataset(disk+jobid+'/netcdf_trop_ox_budget/'+jobid+'_*_'+var+'.nc')
  print('save')
  data.to_netcdf(disk+jobid+'_'+var+'.nc')
