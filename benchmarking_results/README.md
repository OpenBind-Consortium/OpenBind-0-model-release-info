# Benchmarking results

Per-interface metrics for the nine-arm comparison run on the Runs N' Poses style benchmark set archived
at https://zenodo.org/records/22037460.

## `per_interface_breakdown.parquet`

One row per (arm, system, seed, diffusion sample, protein-ligand interface): 132,048 rows over 454 of the
462 benchmark systems, covering 590 distinct protein-ligand interfaces.

### Key columns

- `name`, `label`, `model` — arm identifier, display label, and the model family used to run/parse it.
- `entry_id`, `chain_id_1`, `id` — benchmark system, ligand chain, and the interface key (`entry_id` + chain).
- `seed`, `sample` — inference seed and diffusion sample index within that seed.
- `lig_rmsd`, `pocket_rmsd`, `lddt`, `lddt_pli`, `has_clash` — accuracy metrics against the ground-truth structure.
- `success` — the pass criterion for that interface: `lig_rmsd < 2 Å` and `lddt_pli > 0.8`.
- `ranker`, `is_top1` — the confidence ranker used for top-1 selection, and whether this row is the
  single sample that ranker picked for its (arm, interface) across all seeds and samples (5,310 rows:
  9 arms x 590 interfaces).
- `ptm`, `iptm`, `chain_pair_iptm`, `ranking_score`, `plddt`, and related columns — model confidence outputs.
  Column availability varies by model family, so some are `NaN` for arms that do not emit them.
- `similarity_25` / `bin_25` / `cutoff_date_25` and `similarity_21` / `bin_21` / `cutoff_date_21` — training-set
  sequence similarity for the two training cutoffs and its binning.
- `has_complete_grid`, `complete_grid_all_members` — whether the full seed x sample grid completed for this
  interface, for that arm and across all nine variants. But this is the intersection over all nine variants, for comparing just the non steered version, you should manually identify that subset since that will give slighly more systems. 
