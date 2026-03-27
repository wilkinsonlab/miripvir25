# Meta-transcriptomic benchmark

## Description

Most taxonomic classification profiling/classification methods have been developed to target metagenomic data. In the case of this study, the data is highly different because of two factors:

1. The sequencing reads are the result of RNA sequencing instead of genomic DNA sequencing. That means that factors such as genetic expression affect the composition of the read pool.
2. The sequencing reads are obtained by from host material. This means that the largest part of the reads belong to the host organism, which in most cases is not a model organism. 

For these reasons, **we decided to benchmark the ability of the different taxonomy classication/profiling methods** in simulated set-ups that simulate the conditions of our data. 

## Protocol

1. Create collections of organisms to be downloaded from NCBI. In our case, we used a combination of PAB and random organisms pooled from the GTDB collection. Store the taxon IDs of those organisms in a file without headers.
2. Run the corresponding ploomber pipeline to carry out the download of the CDs of those organisms. `ploomber build -f -e simulate-metatranscriptomic-reads/pipeline-download.yaml`. This will generate sets json files with sequence information.
3. Simulate abundances using the `scripts/abundance.py`
4. Run `iss`
5. Run `python3 ~/dev/miripvir25/scripts/miripvir_tools.py report-abundances ${library}_R1.fastq ${library}_R2.fastq ${library}.report.csv`

The result of the pipeline is a set of FASTQ files to be benchmarked, and files containing the abundances of each taxon in the dataset. 

**NOTE**: Keep in mind that many methods generate taxonomy profiles at species level, while this pipeline allows to generate reports at strain level. If these details are not taken into account when evaluating the benchmark, this can lead to poor metrics.


Example of the CSV file.

```
000047917
000000550
000000294
001138189
001736323
001124983
001735690
000684949
001761874
001268072
```

Example of iss run

```
srun iss generate --model HiSeq \
    --genomes "${fasta}" \
    --n_reads 10M -p 20 \
    --abundance_file ${abundance} \
    -o "${library}"

sed -i 's/\/1$//g' "${library}_R1.fastq"
sed -i 's/\/2$//g' "${library}_R2.fastq"

echo "${library_name}, completed"
```