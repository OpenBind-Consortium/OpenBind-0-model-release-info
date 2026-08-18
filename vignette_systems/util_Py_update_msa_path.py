import os
import json
import argparse

parser = argparse.ArgumentParser(description='Update an of3 query json file so that the MSA paths match the provided --msa_db. Code only works for monomeric and homomeric proteins')

parser.add_argument('--job_json', '-j', help='An of3 query json, with specified inputs for cofolding')
parser.add_argument('--msa_db', '-m', help='Directory with MSA a3m file(s) for the protein in --job_json')
parser.add_argument('--outfile', '-o', help='The name of an updated of3 query json, with corrected msa paths')

args = parser.parse_args()


def main():
    with open(args.job_json) as f:
        data = json.load(f)
    
    for target in data["queries"]:
        print(target)

        for ch in data['queries'][target]["chains"]:
            if ch["molecule_type"] == "protein":
                ch["main_msa_file_paths"] = os.path.abspath(args.msa_db)

    with open(args.outfile, 'w') as fo:
        json.dump(data, fo, indent=4)

if __name__=='__main__':
    main()
