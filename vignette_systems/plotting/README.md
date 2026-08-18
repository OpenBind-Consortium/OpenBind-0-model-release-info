Use the following command to generate a success rate comparison plot:

```
python3 util_Py_plot_success_rate_method_comparison.py -m=../FatA/metrics_FatA_OB0_eval.tsv -o=success_rates/png-bar_FatA_succ_rates.png
```

To compare fine-tuned models to default weights:

```
python3 util_Py_plot_success_rate_method_comparison.py -m=../FatA/metrics_FatA_OB0_eval.tsv -o=success_rates/png-bar_FatA_succ_rates-ft.png -ft
```


Use the following command to generate a failure mode plot:

```
python3 util_Py_plot_oracle_failure_modes.py -i=../FatA/metrics_FatA_OB0_eval.tsv -o=png-bar_failure_modes_FatA.png
```


