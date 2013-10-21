# Settings for dcmenvgen

import sampledata

# sampled modality, study description and SOP class UID
sample_data = sampledata.SampleData()

# extra characters to include in patient id generation
extra_pid_chars = ' _'

# the length of generated patient ID's
min_id_length = 8
max_id_length = 16

# the length of generated accession numbers
min_accn_length = 8
max_accn_length = 16

# how many studies to generate per patient
min_studies = 0
max_studies = 10

# how many series to generate per study
min_series = 1
max_series = 3

# how many images to generate per series
min_images = 3
max_images = 20

# whether or not to generate structured reports
gen_sr = True

# how often to generate structured reports
gen_sr_chance = 0.25

# whether or not to generate patient aliases
gen_alias = True

# how often to generate patient aliases
gen_alias_chance = 0.125

# maximum number of times aliases will be generated for a patient
gen_alias_max = 2

# number of studies required before applying an alias
gen_alias_req = 4

# changes for alias generation
enabled_alias_changes = ['patient_id', 'first_initial', 'middle_initial',
                         'gender', 'birth_date']

# Mmdalities for which sample data exists in the image directory
enabled_modalities = ['CR', 'CT', 'DX', 'MG', 'MR',
                      'NM', 'RG', 'US']

# workstations to deploy
workstations = {
    'port': 11113,
    'ae_titles': ['WK1', 'WK2', 'WK3']
}

# archives to deploy
archives = {
    'port': 4006,
    'ae_titles': ['AR1', 'AR2', 'AR3']
}
