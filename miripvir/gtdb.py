import pandas as pd

class GTDB_taxonomy:

    def __init__(self, names, nodes):
        
        nodes = pd.read_csv(nodes, sep="\t\|\t", header=None, names=['taxid', 'parent', 'rank', '_'])[['taxid', 'parent', 'rank']]
        names = pd.read_csv(names, sep="\t\|\t", header=None, names=['taxid', 'scientific_name', '_', '__'])[['taxid', 'scientific_name']]
        self.nodes = pd.merge(nodes, names, on='taxid')
        self.parents = self.build_lineages_dict(nodes)

    @staticmethod
    def build_lineages_dict(nodes):
        parent_dict = dict()
        for _, node in nodes.iterrows():
            parent_dict[node.taxid] = node.parent

    def lineage(self, taxid):
        lineage = []
        nodes = self.nodes.set_index('taxid').copy()
        while lineage[-1]['taxid'] != 1:
            parent = nodes.loc[self.parents[taxid]].to_dict()
            lineage.append(parent)
