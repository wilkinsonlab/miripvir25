# MIRIPVIR25 

## Contents

- **compute**: Scripts for computational tasks:
    - `compute.cooccurrence-network-properties.R`: Co-occurrence network property calculations.
    - `compute.coocurrence.R`: Co-occurrence computations.
    - `compute.diversity-correlations.R`: Diversity correlation computations.

- **prep/**: Data preparation notebooks:
    - `prep-00.metadata.ipynb`: Preparation of site data (e.g. habitat, etc).
    - `prep-00.motus.ipynb`: Preparation of MOTUs data.
    - `prep-00.virus.ipynb`: Preparation of virus data.
    - `prep-01.cooccurrence.ipynb`: Preparation of co-occurrence calculation.
    - `prep-02.post-cooccurrence.ipynb`: Preparation of cooccurrence output.
    - `prep-03.tableDivBySite.ipynb`: Preparation of diversity by site table.
    - `prep-04.tableDivByHabitat.ipynb`: Preparation of diversity by habitat table.

- **analysis**: Jupyter notebooks for various analyses:
    - `analysis-00.detection-statistics-virus.ipynb`: Detection statistics for viruses.
    - `analysis-00.detection-statistics-bacteria.ipynb`: General detection statistics for bacteria and PABs.
    - `analysis-00.simulations.ipynb`: Benchmark of taxonomy detection in meta-transcriptomic data.
    - `analysis-01.cooccurrence.ipynb`: General co-occurrence analysis.
    - `analysis-01.diversity.ipynb`: General diversity analysis.
    - `analysis-01.wide-taxonomic-profiling.ipynb`: Wide taxonomic profiling (first figure, panel C)
    - `analysis-02.cooccurrence-habitat.ipynb`: Co-occurrence analysis by site and habitat.
    - `analysis-02.host-range.ipynb`: Host range analysis.
    - `analysis-02.organism-range.ipynb`: Organism range analysis.
    - `analysis-03.network-properties.ipynb`: Host-organism network property analysis.
    - `analysis-04.modules.ipynb`: Analysis of network modules.
    - `analysis-05.Q&A.ipynb`: Questions and answers related to the analysis.

- **visualization/**: Visualization notebooks:
    - `visualization.network-bacteria_virus.ipynb`: Bacteria-virus-host network visualization.
    - `visualization.network-bacteria.ipynb`: Bacteria-host network visualization.
    - `visualization.network-virus.ipynb`: Virus-host network visualization.
    - `visualization.terrain.ipynb`: Terrain visualization.
- **conf.yaml**: Configuration file.


- **figures/**: Directory for generated figures.
- **input/**: Input data files:
    - `hits.plant.csv`: Plant hit data.
    - `mapping_genomes`: 
    - `mapping-otus-curated.csv`: Curated OTU mappings.
    - `McLeish_etal_Spatial_Dryad.csv`: Spatial data from McLeish et al.
    - `mcleish24-TableS1.csv`, `mcleish24.TableS1.csv`, `mcleish24.TableS2.csv`, `mcleish24.TableS4.csv`: Supplementary tables from McLeish 2024.
    - `network.mcleish24.links.csv`: Network links from McLeish 2024.
    - `network.mcleish24.nodes.csv`: Network nodes from McLeish 2024.
    - `sanchis21.tableS1.csv`, `sanchis21.TableS1.csv`: Supplementary tables from Sanchis 2021.
    - `val_158_otu_host_df.csv`: OTU-host mapping data.
    - `motus-g1/`: MOTUs data directories.
- **scratch/**: Temporary files and intermediate results:
    - `adjmat.bact.weighted.csv`: Weighted adjacency matrix for bacteria.
- **README.md**: Project documentation.