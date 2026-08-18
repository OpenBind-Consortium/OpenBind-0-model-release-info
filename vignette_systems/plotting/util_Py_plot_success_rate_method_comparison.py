import sys
import json
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle

parser = argparse.ArgumentParser()

parser.add_argument('--metrics', '-m', help='Combined performance metrics for all methods')
parser.add_argument('--outfile', '-o', help='Output png')
parser.add_argument('--exclude_jsons', '-ej', help='Path to train and val jsons with names of cases to be excluded', nargs='+', default=None)
parser.add_argument('--finetune', '-ft', help='Enable to plot OB1 and OF3p fine tune comparisons', default=False, action='store_true')

args = parser.parse_args()

COLORS_DICT = {
    "of3p2" : "#FF0000",
    "of3p2ft": "#8B0000",
    "ob0": "#FFA500",
    "ob0ft": "#FF4500",
    "opendde": "#FFD700",
    "boltz-2": "#008000",
    "esm2": "#00FFFF",
    "af3": "#0000FF",
    "protenix": "#800080"
}

LABEL_DICT = {
    "of3p2" : "OpenFold3-p2",
    "of3p2ft": "OpenFold3-p2-ft",
    "ob0": "OpenBind-0",
    "ob0ft": "OpenBind-0-ft",
    "opendde": "OpenDDE",
    "boltz-2": "Boltz-2",
    "esm2": "ESMFold2",
    "af3": "AlphaFold3",
    "protenix": "Protenix-v1-20250630"
}


def parse_metric_df(m_df, exclude_l=[]):
    succ_data = {'top 1': 0, 'top 25': 0}
    
    tmp = list(set(list(m_df['target'])))
    
    case_l = []
    for case in tmp:
        if case.lower() in exclude_l:
            continue
        else:
            case_l.append(case)
    
    print(f'{len(case_l)} cases')
    for i, target in enumerate(case_l):
        if target.lower() in exclude_l:
            continue
        

        s_df = m_df[m_df['target'] == target]
        s_df = s_df[s_df['is_proper'] == True]
        
        if s_df['pair_iptm'].dropna().empty:
            print(f'\tDrop {target}')
            continue
        #print(case, s_df['is_succ'])
        
        #print(target)
        #for i, val in enumerate(s_df['seed']):
            #lig_rmsd	lddt_pli
        #    print('\t', val, i, s_df['lig_rmsd'].iloc[i], s_df['lddt_pli'].iloc[i], s_df['is_succ'].iloc[i], s_df['lig_id'].iloc[i])
        
        max_iptm = max(s_df['pair_iptm'])

        top1_df = s_df.loc[s_df['pair_iptm'].idxmax()]

        top1_succ = False
        if (top1_df['is_succ'] == True) and (top1_df['pb_valid'] == True):
        #if (top1_df['is_succ'] == True):
            top1_succ = True
        #if top1 == True:
            #s_df = s_df[s_df['sample'] == 1]
        #    s_df = s_df.loc[s_df['pair_iptm'].idxmax()]
            #max_row = df.loc[df["column_name"].idxmax()]

        #print(target, s_df['pair_iptm'], max_iptm)

        is_succ = False
        for j, val in enumerate(s_df['seed']):
            if (s_df['is_succ'].iloc[j] == True) and (s_df['pb_valid'].iloc[j] == True):
            #if (s_df['is_succ'].iloc[j] == True):
                is_succ = True
                break

        #print(target, top1_succ, is_succ)
        if top1_succ:
            succ_data['top 1'] += 1

        if is_succ:
            succ_data['top 25'] += 1

    # Print success rates
    print(succ_data)
    top1_succ_rate = succ_data["top 1"]*100/len(case_l)
    top25_succ_rate = succ_data["top 25"]*100/len(case_l)
    print(f'\tSuccess rate from {len(case_l)} test cases')
    print(f'\tTop 1 Success Rate: {top1_succ_rate:.1f}%')
    print(f'\tTop 25 Success Rate: {top25_succ_rate:.1f}%')
    

    return top1_succ_rate, top25_succ_rate

def plot_ft_results(t1_l, t25_l, label_l, colors, outfile='png-bar_finetune_success_rates.png'):
    
    t1_labels = []
    t25_labels = []

    for v in t1_l:
        if v == 0:
            t1_labels.append('')
        else:
            t1_labels.append(f'{v:.1f}%')

    for v in t25_l:
        t25_labels.append(f'{v:.1f}%')

    bar_width = 1.2
    x_pos = np.arange(0, 1.8*len(label_l), 1.8)
    fig, ax = plt.subplots(tight_layout=True, dpi=300, figsize=(9,6))

    #ax.grid(True, axis='y', linestyle='--', alpha=0.5)

    p_t25 = np.array(t25_l) - np.array(t1_l)
    b1 = ax.bar(x_pos, t1_l, color=colors, edgecolor=colors, width=bar_width)
    ax.bar_label(b1, label_type='center', labels=t1_labels, color='white', fontweight='bold') 

    b2 = ax.bar(x_pos, p_t25, color='white', bottom=t1_l, hatch='//', edgecolor=colors, width=bar_width)
    ax.bar_label(b2, label_type='edge', labels=t25_labels) 

    ax.set_xticks(x_pos)
    ax.set_xticklabels(label_l)#, rotation=90)
    
    ax.set_yticks(np.arange(0,100,10), minor=True)
    ax.set_ylabel('Success Rate (%)')
    ax.set_ylim(0,101)
    
    solid_patch = Rectangle((0, 0), 1, 1, facecolor="gray", edgecolor="black")
    hatched_patch = Rectangle(
        (0, 0), 1, 1, facecolor="white", hatch="///", edgecolor="black"
    )
    all_handles = [
        hatched_patch,
        solid_patch,
    ]
    
    all_labels = [f"Top 25",
                  f"Top 1"]

    leg2 = ax.legend(all_handles, all_labels, loc='upper left', frameon=False)
    ax.add_artist(leg2)


    plt.savefig(outfile)

def main():
    
    exclude_ids = []
    if args.exclude_jsons != None:
        print(args.exclude_jsons)
        
        for ej in args.exclude_jsons:
            with open(ej) as f:
                data = json.load(f)

            for  case in data["structure_data"]:
                print(ej, case)
                exclude_ids.append(case)

    #colors = ['cornflowerblue', 'royalblue', 'mediumorchid', 'purple', 'red', 'green']#, 'royalblue', 'pink', 'purple']
    #labels = ['of3p2', 'of3p2-ft_all', 'of3p2-ft_filtered', 'of3p2-ft_site0', 'of3p2-ft_hs', 'of3p2-ft_x0926a', 'of3p2-ft_x0812a']
    #labels = ['OF3-p2 155k', 'OF3-p2-ft 155k', 'OpenBind 174k', 'OpenBind-ft 174k', 'Alphafold3', 'Protenix-v1 (2025-06-30)'] # 'of3p2-ft_filtered', 'of3p2-ft_site0', 'of3p2-ft_hs', 'of3p2-ft_x0926a', 'of3p2-ft_x0812a']
    p_top1 = []
    p_top25 = []
    p_labels = []
    p_colors = []
    
    df = pd.read_csv(args.metrics, delimiter='\t')
    method_l = list(set(df['method']))
    
    
    if args.finetune == True:
        method_order = ['of3p2', 'of3p2ft', 'ob0', 'ob0ft']
    else:
        method_order = list(LABEL_DICT.keys())

    for m in method_order:
        
        print(m, m in ['of3p2ft', 'ob0ft'], args.finetune)
        if args.finetune == False:
            if m in ['of3p2ft', 'ob0ft']:
                continue

        of3_df = df[df['method'] == m]
        if len(of3_df) == 0:
            continue
        print(m, len(of3_df))
        # Get success rates
        t1_sr, t25_sr = parse_metric_df(of3_df, exclude_ids)
        print('\t', t1_sr, t25_sr)
        #p_labels.append(labels[i])
        p_labels.append(LABEL_DICT[m])
        p_colors.append(COLORS_DICT[m])
        p_top1.append(t1_sr)
        p_top25.append(t25_sr)
        
    print(len(p_top1), p_top1)
    print(len(p_top25), p_top25)
    print(len(p_labels), p_labels)
    print(len(p_colors), p_colors)

    plot_ft_results(p_top1, p_top25, p_labels, p_colors, outfile=args.outfile)        

if __name__=='__main__':
    main()
