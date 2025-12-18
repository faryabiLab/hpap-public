#!/usr/bin/env python3

"""
This script reads Elisabetta's JSON file and creates a new JSON file
that will be used by both front-end and back-end.
"""

import json


input_filename = "original_dna_methylome_bigwigs.json"
output_filename = "dna_methylome.json"
url_prefix = "https://faryabi16.pmacs.upenn.edu/wugb/"

# Static data:
output_data = {
    "General": {
        "Tissue_type": "None",
        "Platform": "Illumina",
        "Institution": "University of Pennsylvania",
        "dbGAP_url": "https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs002465.v2.p1"
    },
}


with open(input_filename) as ifo, open(output_filename, 'w') as ofo:
    input_list = json.load(ifo)

    for x in input_list:
        donor_id = x['name'][0:8]

        # Confirm that donor ID is valid.
        if not donor_id.startswith('HPAP-'):
            print(f"ERROR: invalid donor ID ({donor_id})")

        cell_type = x['metadata']['cell_type']
        assay_value = x['metadata']['assay']
        donor_dict = output_data.setdefault(donor_id, {})

        # Confirm that different cell types of a donor always have same
        # "assay" value.
        if 'assay' in donor_dict and donor_dict['assay'] != assay_value:
            print(f"ERROR: different assy in {x['name']}")

        donor_dict.setdefault('assay', assay_value)

        cell_data = donor_dict.setdefault(cell_type, {})
        cell_data['status'] = 'Available'

        # Update bigwig data
        path = x['url'].removeprefix(url_prefix)
        x['path'] = path
        del x['url']
        del x['showOnHubLoad']
        del x['metadata']['donor']
        del x['metadata']['cell_type']
        del x['metadata']['assay']

        wugb_files = cell_data.setdefault('wugb_files', [])
        wugb_files.append(x)

    # Save output_data:
    json.dump(output_data, ofo, indent=2)
