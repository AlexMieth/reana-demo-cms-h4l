import glob

#Get pathnames to all the .txt index files from within the datasets directory
datasets = glob.glob('datasets/*.txt', recursive=True)

#Read in the default format for the python configuration files
with open('code/HiggsExample20112012/Level4/default_cfg.py', 'r') as default_cfg:
    default_content = default_cfg.read()

N = 10
count = 0
#Iterate through each of these files
for filename in datasets:
    with open(filename,"r") as fi:

        lines = fi.read().splitlines()

        for i in range(0, len(lines), N):
            #Create list of N root files
            N_rootfiles = lines[i:i+N]

            #Turn this list of N root files into one long string
            new_input_filenames = ' '.join(N_rootfiles)

            count += 1
            new_filename = 'code/HiggsExample20112012/Level4/cfg_files/demoanalyzer_cfg' + str(count) + '.py'
            new_output_filename = 'output' + str(count) + '.root'

            new_content = default_content

            new_content = new_content.replace('OUTPUT_FILE_STR', new_output_filename)
            new_content = new_content.replace('INPUT_FILES_STR', new_input_filenames)



            with open(new_filename,"w") as new_cfg:
                new_cfg.write(new_content)







