# OpenBind-0-model-release-info
Scripts and files associated with the OpenBind-0 model release

## Benchmark set (Zenodo)

The protein-ligand benchmark set used for the OpenBind-0 release is archived on Zenodo:
**https://zenodo.org/records/22037460**

It contains 462 systems, each with a ground-truth structure and a model input query, together with the
multiple sequence alignments (MSAs) the queries were built from. This is a preview, Runs N' Poses style
set built from an updated PLINDER database that had not yet been officially released; please check
whether the official updated PLINDER benchmark is out and use that instead of this preview if so.

## Contents

- `vignette_systems/` — metrics, MSA inputs, training-set similarity data, and plotting code for the four
  vignette systems (see [vignette_systems/README.md](vignette_systems/README.md)).
- `benchmarking_results/` — per-interface metrics for the nine-arm comparison on the benchmark set above
  (see [benchmarking_results/README.md](benchmarking_results/README.md)).
