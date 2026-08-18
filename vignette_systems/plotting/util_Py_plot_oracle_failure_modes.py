import os
import json
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

COLOR_DICT = {
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

parser = argparse.ArgumentParser()
parser.add_argument('--metric_tsv', '-i')
parser.add_argument('--outfile', '-o', help='Output png with each failure mode')
parser.add_argument('--pocket_recall', '-pr', help='(Optional) The minimum pocket recall for a pocket_failure (default = 0.35)', default=0.35, type=float)
parser.add_argument('--lddt_lp', '-lp', help='(Optional) The lddt-lp for a conf_failure (default = 0.80)', default=0.80, type=float)
parser.add_argument('--lddt_pli', '-lpli', help='(Optional) The lddt-pli for a success (default = 0.80)', default=0.80, type=float)
parser.add_argument('--lrmsd', '-rmsd', help='(Optional) The ligand rmsd for a success (default = 2.00)', default=2.00, type=float)
parser.add_argument('--exclude_jsons', '-ej', help='Path to train and val jsons with names of cases to be excluded', nargs='+', default=None)

args = parser.parse_args()

# Create a plot for failure modes per method
# Can customize method_l to specify what should be plotted
def plot_failure_modes(failure_data, mode_l, outfile, method_l=['of3p2', 'ob0', 'af3', 'protenix']):
    
    print(mode_l)
    # Format data for plotting
    plot_data = {}
    for method in method_l:
        plot_data[method] = {'succ': [], 'fail': []}
        for mode in mode_l:
            plot_data[method]['succ'].append(len(failure_data[method]['modes'][mode]['succ']))
            plot_data[method]['fail'].append(len(failure_data[method]['modes'][mode]['fail']))
        
        print(method, plot_data[method], np.sum(plot_data[method]['succ']) + np.sum(plot_data[method]['fail']) )

    # Create a bar chart 
    fig, ax = plt.subplots(tight_layout=True, figsize=(10,5), dpi=300)

    width = 0.10
    x_pos = np.arange(len(mode_l))
    #xlabel_pos = x_pos + (width*3)
    xlabel_pos = x_pos + (width*2)

    for i, m in enumerate(plot_data):
        color = COLOR_DICT[m]
        offset = width*i
        
        succ_rates = []
        for i, val in enumerate(plot_data[m]['succ']):
            try:
                sr = val*100/(plot_data[m]['succ'][i] + plot_data[m]['fail'][i])
                print('\t', m, i, mode_l[i], sr)
                sr = int(sr)
            except:
                sr = ''
                print('\t', m, i, mode_l[i], sr)

            succ_rates.append(str(sr))

        pf = ax.bar(x_pos+offset, plot_data[m]['succ'], color=color, edgecolor=color, label=LABEL_DICT[m], width=width)
        ps = ax.bar(x_pos+offset, plot_data[m]['fail'], color='white', edgecolor=color, hatch='///', bottom=np.array(plot_data[m]['succ']), width=width) 

        #p = ax.bar(x_pos+offset, fail_plot, color=COLOR_DICT[m], edgecolor=COLOR_DICT[m], label=m, width=width)
        #p = ax.bar(x_pos+offset, succ_plot, color='white', edgecolor=COLOR_DICT[m], hatch='///', bottom=np.array(fail_plot), width=width)
    
    ax.set_ylabel('Num. Binding Events')

    ax.set_xticks(xlabel_pos)
    ax.set_xticklabels(mode_l)
    
    # Try legend outside of box
    #box = ax.get_position()
    #ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    
    #leg1 = ax.legend(loc='upper left')
    leg1 = ax.legend(loc='upper left', bbox_to_anchor=(0.0, 1.0))
    ax.add_artist(leg1)

    hatched_patch = Rectangle(
        (0, 0), 1, 1, facecolor="white", hatch="///", edgecolor="black"
    )
    solid_patch = Rectangle((0, 0), 1, 1, facecolor="gray", edgecolor="black")

    all_handles = [hatched_patch,
                   solid_patch]

    all_labels = ['Failed Prediction',
                  'Successful Prediction']

    #leg2 = ax.legend(all_handles, all_labels, loc='upper center', frameon=False)
    leg2 = ax.legend(all_handles, all_labels, loc='upper left', frameon=False, bbox_to_anchor=(0.0, 0.8))
    ax.add_artist(leg2)

    plt.savefig(f'{outfile}')



def main():
    df = pd.read_csv(args.metric_tsv, delimiter='\t')
        
    exclude_ids = []
    if args.exclude_jsons != None:
        print(args.exclude_jsons)
        
        for ej in args.exclude_jsons:
            with open(ej) as f:
                data = json.load(f)

            for  case in data["structure_data"]:
                #print(ej, case)
                exclude_ids.append(case)
    
    print('Exclude list')
    print(exclude_ids)
    method_l = set(df['method'])

    failure_modes = ['Pocket Not Found\nPocket Conformation Incorrect',
                     'Pocket Not Found\nPocket Conformation Correct',
                     'Pocket Found\nPocket Conformation Incorrect',
                     'Pocket Found\nPocket Conformation Correct'
                    ]

    failure_data = {}
    for m in method_l:
        df_m = df[df['method'] == m]
        df_m = df_m[df_m['is_proper'] == True] # Only ligands of interest

        failure_data[m] = {'succ': 0,
                           'fail': 0,
                           'modes': {}
                          }

        for fm in failure_modes:
            failure_data[m]['modes'][fm] = {'succ': [], 'fail': []} # List of targets

        target_l = list(set(df_m['target']))
        #print(m, len(target_l))

        # Get the "best" model from each target
        for t in target_l:
        #for t in target_l[:10]: # Debug
            if t.lower() in exclude_ids:
                print(f'Skip {t}')
                continue
            
            is_succ = False

            df_t = df_m[df_m['target'] == t]
            

            df_ligrmsd = df_t[df_t['lig_rmsd'].notna()]

            if len(df_ligrmsd) == 0:
                failure_data[m]['fail'] += 1
                continue



            df_succ = df_t[df_t['is_succ'] == True]
            df_succ = df_succ[df_succ['pb_valid'] == True]

            #print('\t', t, len(df_ligrmsd), len(df_succ))

            if len(df_succ) > 0:
                is_succ = True
                #print(df_succ)
                
                # Get the "best" model with lowest ligand RMSD
                #df_best = df_succ.loc[df_succ['lig_rmsd'].idxmin()]
                df_best = df_succ.loc[df_succ['pair_iptm'].idxmax()]
                failure_data[m]['succ'] += 1
            else:
                failure_data[m]['fail'] += 1
                #df_best = df_t.loc[df_t['lig_rmsd'].idxmin()]
                df_best = df_t.loc[df_t['pair_iptm'].idxmax()]
            

            # Check failure modes of the "best" model
            pocket_recall = float(df_best['pocket_recall'])
            lddt_lp = float(df_best['lddt_lp'])
            lig_rmsd = df_best['lig_rmsd']
            lddt_pli = df_best['lddt_pli']
            pair_iptm = df_best['pair_iptm']
            seed = df_best['seed']
            sample = df_best['sample']

            if lddt_lp < args.lddt_lp:
                conf_fail = True
            else:
                conf_fail = False

            if pocket_recall < args.pocket_recall:
                pocket_fail = True
            else:
                pocket_fail = False
                
            
            
            if is_succ:
                k = 'succ'
            else:
                k = 'fail'

            
            fmode = 'None'
            if (pocket_fail) and (conf_fail):
                fmode = 'Pocket Not Found\nPocket Conformation Incorrect'
                failure_data[m]['modes']['Pocket Not Found\nPocket Conformation Incorrect'][k].append(t)
            elif (pocket_fail) and (conf_fail == False):
                fmode = 'Pocket Not Found\nPocket Conformation Correct'
                failure_data[m]['modes']['Pocket Not Found\nPocket Conformation Correct'][k].append(t)
            elif (pocket_fail == False) and (conf_fail == False):
                fmode = 'Pocket Found\nPocket Conformation Correct'
                failure_data[m]['modes']['Pocket Found\nPocket Conformation Correct'][k].append(t)
            elif (pocket_fail == False) and (conf_fail):
                fmode = 'Pocket Found\nPocket Conformation Incorrect'
                failure_data[m]['modes']['Pocket Found\nPocket Conformation Incorrect'][k].append(t)

            
        print(m, failure_data[m]['succ'], failure_data[m]['fail'])
        for mode in failure_data[m]['modes']:
            mode_name = ', '.join(mode.split('\n'))
            print(f'\t{mode_name}:\n\t\tsucc: {len(failure_data[m]["modes"][mode]["succ"])}\n\t\tfail: {len(failure_data[m]["modes"][mode]["fail"])}')


    plot_failure_modes(failure_data, failure_modes, args.outfile)



if __name__=='__main__':
    main()
