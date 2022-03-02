import ALifeStdDev.phylogeny as phylodev
#import networkx as nx
import math
import collections
from decimal import Decimal


# Create an ordered dictionary of a line of descent from the phylogeny
# This allows us to put the LOD in time order
def lod_dict_from_phylo(filepath):
    phylo = phylodev.load_phylogeny_to_networkx(filepath)
    extant_ids = phylodev.get_extant_taxa_ids(phylo, not_destroyed_value=math.inf)
    lod = phylodev.extract_asexual_lineage(phylo,extant_ids[0])
    lod_dict = dict(lod.nodes(data="taxon_info"))
    lod_chrono = collections.OrderedDict(sorted(lod_dict.items()))
    return lod_chrono

# Create the line of descent file
# Columns: ID (generation), values 
def export_lod(lod, dims, lodpath="lod.csv"):
    with open(lodpath, "w") as lod_file:
        if (dims==4):
            lod_file.write("id,x,y,z,k\n")
        elif (dims==3):
            lod_file.write("id,x,y,z\n")
        elif (dims==2):
            lod_file.write("id,x,y\n")
        else:
            print("Dims invalid")
            return 

    for gen, vals in lod.items():
        vals = ",".join(vals.lstrip('[ ').rstrip(' ]').split())
        line = str(gen) + "," + vals + "\n"
        with open(lodpath, "a") as lod_file:
            lod_file.write(line) 

# Turn the line of descent file into a single string for the purposes of creating a "meshline"
# Format is val1, val2, [val3, val4]; val1, val2, val3, val4;
def export_edges(lod, edgepath="edges.csv"):
    edge_list = []
    for vals in lod.values():
        # multiply string values by 10 and convert back to string
        # this helps the spacing visually
        vals = " ".join([str(Decimal(x)*10) for x in vals.lstrip('[ ').rstrip(' ]').split()])
        edge_list.append(vals)
    with open(edgepath, "w") as edge_file:
        edge_file.write(",".join(edge_list))

# Combine the previous functions to repeat over all the replicates 
def lod_gen(dims, first=0, last=10):

    datapath = "./../data/"
    reppath = datapath + "reps/"

    fcns = ["Shubert", "Vincent", "CF1", "CF2"]
    mutrates = ["01", "001", "0001", "00001"]
    tournament_sizes = [2, 4, 8, 16]

    filename = "phylogeny_1000.csv"
    lodname = "lod.csv"
    edgename = "edges.csv"

    # TODO: Change to itertools? 

    for fcn in fcns:
        for mut in mutrates:
            for t in tournament_sizes:
                for rep in range(first, last):
                    dirpath = reppath + "SEED_" + str(rep).rjust(2, '0') + "__F_" + fcn + "__D_" + str(dims) + "__MUT_" + mut + "__T_" + str(t).rjust(2, '0') + "/" 
                    filepath = dirpath + filename
                    lodpath = dirpath + lodname 
                    edgepath = dirpath + edgename

                    lod = lod_dict_from_phylo(filepath)
                    export_lod(lod, dims, lodpath)
                    export_edges(lod, edgepath)

lod_gen(2, last=2)
lod_gen(3, last=2)
lod_gen(4, last=2)