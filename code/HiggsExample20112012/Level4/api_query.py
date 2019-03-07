import requests

# **********************************************************************
# Starting at the "Higgs-to-four-lepton analysis example using         * 
#    2011-2012 data" which is identified as record 5500.               *
# **********************************************************************
record_5500 = requests.get('http://opendata.cern.ch/api/records/5500')

# **********************************************************************
# Get the list of datasets that are linked on this page to be used for * 
#    this example. Each element of this list is a single item          *
#    dictionary with the key 'recid' paired with the record number of  *
#    the dataset as the value.                                         *
# **********************************************************************
dataset_links = record_5500.json()["metadata"]["use_with"]["links"]

# **********************************************************************
# Convert this list of single item dictionaries into a list that just  * 
#    contains the record number for each dataset.                      *
#    If the same dataset id appears twice within datset_links, the     *
#    duplicates are skipped and the dataset id is only included once.  *
# **********************************************************************
dataset_ids =[]
for dataset_dict in dataset_links:
    rec_id = dataset_dict["recid"]
    if rec_id in dataset_ids:
        print("Warning: The dataset for record " + rec_id + " is listed more than once. Skipping duplicate...")
    else:
        dataset_ids.append(rec_id)

# **********************************************************************
# For each dataset id number, get the opendata record page json file.  * 
#    Get the list of index files that are listed on this record page.  *
#    Each item in this list is a dicitonary containing information on  *
#    index file. It is important to note that each index file is       *
#    listed twice, once as a json file and once as as a txt file. We   *
#    are only interested in downloading the txt files.                 *
#                                                                      *
#    For each index file, use the url listed in its dicitonary to get  *
#    the txt file and write/save a copy of it in the inputs directory  *
# **********************************************************************
for record_num in dataset_ids:

    record_url = 'http://opendata.cern.ch/record/' + record_num + '/export/json'
    record = requests.get(record_url)
    index_files = record.json()["metadata"]["index_files"]

    for index_file in index_files:
        filename = index_file['filename']
        if '.txt' in filename:
            txt_file = requests.get(index_file['uri_http'])
            filepath = '../../../datasets/'+filename
            with open(filepath, 'wb') as fi:
                fi.write(txt_file.content)
