# Preparation 

## Summary

The results from MIRIPVIR are obtained from different sources:
- The results from the previous article (McLeish2024)
- The results from the MOTUS characterization

Additionally, the `cooccurrence` analysis is key for the rest of the analysis, 
and it requires certain preparation of the input and output of such analysis.

## Content

- `prep-00.metadata`: It converts the sampling data to a table that includes each site, it habitat, host, etc
- `prep-00.virus`: It converts the virus detected in the previous article into a table that can be employed in the analysis.
- `prep-00.motus`: It converts the MOTUS-g1 results into a table that can be employed in the analysis.
- `prep-01.cooccurrences`: It generates the `cooccur` input from the output of `prep-00.virus` and `prep-00.motus`.
- `prep-01.tableS1`: 
- `prep-01.tableS2`: 
- `prep-02.post-cooccurrence`: It process the output to generate a cooccurrence-by-library. 
- `prep-03.tableS3`: 
- `prep-04.tableS4`: 
