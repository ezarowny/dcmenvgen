# Settings for dcmenvgen

import sampleddata

# sampled modality, study description and SOP class UID
sampled_data = sampleddata.SampledData()

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
