# Performance metrics, similarity data, and cofolding inputs, for the four systems used to benchmark OpenBind0

### File structure
For each system, we include the following data:

```
system_name/
  metrics_{system_name}_OB0_eval.tsv

  all_metrics/
    metrics_{system_name}_OB0_all.tsv  

  msa_inputs/
    sequence.fasta
    msa_{CHAIN}/
      cfdb_hits.a3m

  train_val_cache/
    train_cache.json
    val_cache.json
```

Files include the following info:

`metrics_{system_name}_OB0_eval.tsv`: performance metrics for the test/evaluation set for each system

`all_metrics/metrics_{system_name}_OB0_all.tsv`: performance metrics for test, validation, and train set systems

`msa_inputs/sequence.fasta`: fasta file with the sequence of the system

`msa_inputs/msa_{CHAIN}/`: directory containing the MSA used for cofolding

`train_val_cache/`: directory containing information for the train/val splits used for fine-tuning


### Update MSA info for your installation

If you wish to run cofolding predictions yourself, update OF3 query jsons with paths to the MSAs in your own installation:
```
python3 util_Py_update_msa_path.py -j=EV71_2A_Protease/job_of3_EV71-2A-Protease_inputs.json -m=EV71_2A_Protease/msa_inputs/msa_A/ -o=job_of3_EV71-2A-Protease_inputs_updated.json
```

