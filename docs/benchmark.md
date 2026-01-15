# Benchmark

## What?

We are benchmarking the metrics of our taxonomy detection methods. 

## Why?

There are at least three reasons to benchmark our taxonomy detections:

1. There are lots of methods for prokaryote taxonomic detection. It is not clear which one to use.
2. None of them have been benchmarked in a meta-transcriptomic benchmark, so we don't know a priori which method is best in this specific case.
3. We don't know whether our data (meta-transcriptomics) enables plant-associated bacteria detection. 

## How?

### Benchmark pipeline

The benchmark pipeline consisted on 

1. Sampling PABs and random bacteria from the GTDB.
2. Downloading the CDs of the sampled bacteria and index them in a database.
3. Assign abundances using log-normal distributions over species and specific genes.
4. Simulate the corresponging transcriptomic sequences using ´insilicseq´
5. Mix with an *Arabidopsis thaliana* transcriptome.

This pipeline has five groups of parameters:
- Number of PABs and random bacteria.
- Host-abundance
- Library size
- Log-normal parameters for the organism distribution.
- Log-normal parameters for the CDs distributions

The pipeline can be found at [this link]()

## Benchmark evaluation

To evaluate the benchmark, we used the code contained in `analysis/prep-00.benchmark.ipynb`, which requires the data to be placed in `results/2025-06-23.benchmark-test7`. Modules from `miripvir25` must be installed to be able to run the notebook. 

## Metrics

### Sensitivity

Defined as 

$$ 
S = \frac{TP}{TP + FN} 
$$

### Precision

$$ P = \frac{TP}{TP + FP} $$

### F1-score

$$ P = \frac{2 \dot TP}{TP + FP + FN} $$


## Statistics

We use multiple *Dunnet* tests to measure the performance of each method against all other methods. We repeat this test considering each method as control, and we adjust the p-values using the Bonferroni correction.