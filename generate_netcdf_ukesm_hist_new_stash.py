#!/usr/local/shared/ubuntu-12.04/x86_64/python2.7/bin/python
# Only use for files with more than one timestep as iris does not output that dimension if only one step in it. 
import iris
import definitions_STASH_ukesm as def_STASH
from stash_list_ukesm_o3_eval import lst
import os
import numpy as np
import sys
jobid=sys.argv[1] 
disk=sys.argv[2] 

outputdir=disk+jobid+'/netcdf_trop_ox_budget/'
inputdir= '/gws/nopw/j04/htap2/ptg21/'+jobid+'/pp_files_ox_eval_py/'
if not os.path.exists(outputdir):
    os.makedirs(outputdir)

#################################################################### 
# Which STASH numbers to take for the netCDF file
#################################################################### 
name = []
stash_list = []
for i in lst:
    name.append(i[0])
    stash_list.append(i[1])
#################################################################### 
# loop over decades and years
#################################################################### 

def ret_stash_string(i):
  isec=i//1000
  sec="{:02d}".format(isec)
  it="{:03d}".format(i-(1000*isec))
  return 'm01s'+sec+'i'+it
 
print ('\n'+jobid+'\npm')
# prepare STASH codes
path_to_files=inputdir+'/'+jobid+'a.pm'
for z in range(0,len(stash_list)):
  for decade in np.arange(202,204):
   decade = str(decade) 
   stash=[]
   field_constr=[]
   for i in stash_list[z]:
       stashdir = inputdir+'/'
       stash.append(ret_stash_string(i))
       field_constr.append(iris.AttributeConstraint(STASH=ret_stash_string(i)))
       print ('stash : ')
       print (stashdir)
   # load pp files and output netCDF
   outfile=outputdir+jobid+'_'+decade+'0'+name[z]+'.nc'
   print(outfile)
   field=iris.load(stashdir+'*'+decade+'*.pp',field_constr,callback=def_STASH.UKCA_callback)
   print (field)
   iris.save(field, outfile)
 
