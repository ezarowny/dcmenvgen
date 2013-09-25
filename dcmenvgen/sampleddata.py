import csv
import random


class SampledData:

    """Description

    Instance Variables:
    study_data  -- a dictionary containing study descriptions keyed by modality
    sop_data    -- a dictionary containing SOP class UID's keyed by modality

    Public Methods:
    random_modality             -- get a random modality
    random_study_description    -- get a random study description
    random_sop_class_uid        -- get a random SOP class UID

    """

    def __init__(self):
        self.study_data = {}
        with open('studydata.txt') as data:
            reader = csv.reader(data)
            for row in reader:
                modality = row[0]
                study_description = row[1]
                if modality not in self.study_data:
                    self.study_data[modality] = []
                self.study_data[modality].append(study_description)

        # self.sop_data = {}
        # with open('sopdata.txt') as data:
        #     reader = csv.reader(data)
        #     for row in reader:
        #         modality = row[0]
        #         sop_class_uid = row[1]
        #         if modality not in self.sop_data:
        #             self.sop_data[modality] = []
        #         self.sop_data[modality].append(sop_class_uid)

    # Modality will come from study_data and not sop_data because sop_data
    # contains all possible modalities and study_data may not.
    def random_modality(self):
        modality = random.choice(self.study_data.keys())
        return modality

    def random_study_description(self, modality):
        study_description = random.choice(self.study_data[modality])
        return study_description

    def random_sop_class_uid(self, modality):
        # sop_class_uid = random.choice(self.sop_data[modality])
        # return sop_class_uid
        return '1.2.3.4'
