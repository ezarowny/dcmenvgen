import csv
import random
import os


class SampleData:

    """Contains sampled field data of modality and study description pairings.

    Instance Variables:
    study_data  -- a dictionary containing study descriptions keyed by modality

    Public Methods:
    random_modality             -- get a random modality
    random_study_description    -- get a random study description
    random_sop_class_uid        -- get a random SOP class UID

    """

    def __init__(self):
        path = os.path.dirname(__file__)
        self.study_descriptions = {}
        with open(os.path.join(path, 'sampledata/descriptions.csv')) as data:
            reader = csv.reader(data)
            for row in reader:
                modality = row[0]
                study_description = row[1]
                if modality not in self.study_descriptions:
                    self.study_descriptions[modality] = []
                self.study_descriptions[modality].append(study_description)

    def random_modality(self, modalities):
        modality = random.choice(modalities)
        return modality

    def random_study_description(self, modality):
        study_description = random.choice(self.study_descriptions[modality])
        return study_description
