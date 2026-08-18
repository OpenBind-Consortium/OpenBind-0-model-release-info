import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()

parser.add_argument('--sim_2021', '-s1', help='tsv with similarity data calculated with the 2021-09-30 cutoff')
parser.add_argument('--sim_2025', '-s2', help='tsv with similarity data calculated with the 2025-06-30 cutoff')
parser.add_argument('--outfile', '-o', help='Name of the output png file')

args = parser.parse_args()

def plot_superimposed_hists(sim1, sim2, outfile='png-hist_comparison.png'):
    bins = np.arange(0,105,5)

    fig, ax = plt.subplots(figsize=(9,6), dpi=300, tight_layout=True)

    ax.hist(sim1, bins=bins, color='blue', label='2021-09-30 training cutoff', alpha=0.5, edgecolor='black')
    ax.hist(sim2, bins=bins, color='orange', label='2025-06-30 training cutoff', alpha=0.5, edgecolor='black')

    ax.set_ylabel('Count')
    ax.set_xlabel('Training Set Similarity')

    ax.set_xlim(0,100)
    xtick_pos = np.arange(0, 110, 10)
    ax.set_xticks(xtick_pos)
    
    ax.legend()
    plt.savefig(outfile)

def main():
    df1 = pd.read_csv(args.sim_2021, delimiter='\t')
    df2 = pd.read_csv(args.sim_2025, delimiter='\t')
    
    print('start')
    sim1 = df1['similarity']
    sim2 = df2['similarity']

    plot_superimposed_hists(sim1, sim2, args.outfile)


if __name__=='__main__':
    main()
