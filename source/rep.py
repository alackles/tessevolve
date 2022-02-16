#
#  @note This file is part of MABE, https://github.com/mercere99/MABE2
#  @copyright Copyright (C) Michigan State University, MIT Software license; see doc/LICENSE.md
#  @date 2021
#
#  @file  rep.py
#  @brief Quick & dirty way to run multiple replicates in MABE and save the data.
#

import os
from pathlib import Path 

buildpath = "./third-party/MABE2/build/"
runpath = buildpath + "MABE"
reppath = "../data/reps/"
datpath = "./third-party/MABE2/source/tools/DataGECCO/"

genfile = "./third-party/MABE2/settings/GECCO.gen"
mabefile = "./third-party/MABE2/settings/GECCO.mabe"

firstrep = 0
lastrep = 10
fcns = {
  "Shubert": (-5, 5), 
  "Vincent": (0.25, 10.25), 
  "CF3": (-5, 5), 
  "CF4": (-5, 5)
  }
tournament_sizes = [2, 4, 8, 16]
mutrates = [0.1, 0.01, 0.001, 0.0001]
dims = [2, 3]
#digs = len(str(lastrep-firstrep))
digs = 2

# clean build of MABE
#os.system("cd " + buildpath + "&& make clean && make && cd ../../../")

for fcn, minmax in fcns.items():
  minval = minmax[0]
  maxval = minmax[1]
  for tourny in tournament_sizes: 
    tournystr = str(tourny).rjust(2, '0')
    for mut in mutrates:
      mutstr = str(mut).replace(".","")
      for dim in dims:
        dimstr = str(dim)
        for rep in range(firstrep, lastrep): 
            # random seeds and folder creation
            randseed = rep
            dirname = reppath + "SEED_" + str(randseed).rjust(digs, '0') + "__F_" + fcn + "__D_" + dimstr + "__MUT_" + mutstr + "__T_" + tournystr + "/" 
            print(dirname)
            Path(dirname).mkdir(parents=True, exist_ok=True)

            #variables 
            fcn_var = 'eval_gecco.fcn_name=\\"' + fcn + '\\"'
            dim_var = 'eval_gecco.dims=\\"' + str(dim) + '\\"'
            vals_var = 'vals_org.N=\\"' + str(dim) + '\\"'
            min_var = 'vals_org.min_value=\\"' + str(minval) + '\\"'
            max_var = 'vals_org.max_value=\\"' + str(maxval) + '\\"'

            mut_rate = 'vals_org.mut_prob=\\"' + str(1) + '\\"'
            mut_var = 'vals_org.mut_size=\\"' + str(mut) + '\\"'
            tourney_var = 'select_tourny.tournament_size=\\"' + str(tourny) + '\\"'

            randseed_var = "random_seed=" + str(randseed)
            datpath_var = 'eval_gecco.dat_path=\\"' + datpath + '\\"'

            outpath_var = 'output.filename=\\"' + dirname + 'output.csv\\"'
            genpath_var = 'eval_gecco.genome_file=\\"' + dirname + 'genome.csv\\"'
            phylopath_var = 'sys.snapshot_file_root_name=\\"' + dirname + 'phylogeny\\"'
            phylodatapath_var = 'sys.data_file_name=\\"' + dirname + 'phylogenetic_data.csv\\"'


            settings = fcn_var + "\;" + dim_var + "\;" + vals_var + "\;" + min_var + "\;" + max_var + "\;" + mut_rate + "\;" + mut_var + "\;" + tourney_var +"\;" + randseed_var + "\;" + datpath_var + "\;" + outpath_var + "\;" + genpath_var + "\;" + phylopath_var + "\;" + phylodatapath_var 
            print(settings)
            os.system(runpath + " -f " + mabefile + " -s " + settings)
