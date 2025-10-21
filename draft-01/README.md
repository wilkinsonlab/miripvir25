# MIRIPVIR25 

## Contents

- **compute**: Scripts for computational tasks:
    - `compute.cooccurrence-network-properties.R`: Co-occurrence network property calculations.
    - `compute.coocurrence.R`: Co-occurrence computations.
    - `compute.diversity-correlations.R`: Diversity correlation computations.

- **prep/**: Data preparation notebooks:
    - `prep.cooccurrence.ipynb`: Preparing co-occurrence data.
    - `prep.metadata.ipynb`: Preparing metadata.
    - `prep.motus.ipynb`: Preparing MOTUs data.
    - `prep.virus.ipynb`: Preparing virus data.

- **analysis**: Jupyter notebooks for various analyses:
    - `analysis.detection-statistics-virus.ipynb`: Detection statistics for viruses.
    - `analysis.detection-statistics.ipynb`: General detection statistics.
    - `analysis.coocurrence.ipynb`: General co-occurrence analysis.
    - `analysis.coocurrence-habitat.ipynb`: Co-occurrence analysis by habitat.
    - `analysis.diversity.ipynb`: General diversity analysis.
    - `analysis.diversity-correlations.ipynb`: Diversity correlation analysis.
    - `analysis.host-range.ipynb`: Host range analysis.
    - `analysis.organism-range.ipynb`: Organism range analysis.
    - `analysis.network-properties.ipynb`: Host-organism network property analysis.
    - `analysis.modules.ipynb`: Analysis of network modules.
    - `analysis.Q&A.ipynb`: Questions and answers related to the analysis.
    - `analysis.wide-taxonomic-profiling.ipynb`: Wide taxonomic profiling.

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