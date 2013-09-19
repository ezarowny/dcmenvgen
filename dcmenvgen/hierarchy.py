import datetime
import dicom
import names
import random
import utils


class Image:

    """ Description

    Instance Variables:
    sop_class_uid       --
    sop_instance_uid    -- uniquely identifies the image

    Public Methods:

    """


class Series:

    """ Description

    Instance Variables:
    modality            -- the modality of the series
    series_date         -- the date the series was performed
    series_time         -- the time the series was performed
    series_instance_uid -- uniquely identifies the series
    images              -- the series' images

    Public Methods:

    """

    def generate_images(self, num_images):
        self.images = []
        for i in xrange(random.randint(num_images[0], num_images[1])):
            image = Image()

            image.sop_class_uid = 'FILL'
            image.sop_instance_uid = dicom.UID.generate_uid()

            self.images.append(image)


class Study:

    """ Description

    Instance Variables:
    study_date          -- the date the study was performed
    study_time          -- the time the study was performed
    accession_number    -- the accession number for the study
    study_description   -- the description of the study
    study_instance_uid  -- uniquely identifies the study
    series              -- the study's series

    Public Methods:

    """

    def generate_series(self, num_series, study_date):
        self.series = []
        for i in xrange(random.randint(num_series[0], num_series[1])):
            series = Series()

            series.series_date = study_date
            series.series_time = datetime.datetime.now().time()

            series.series_instance_uid = dicom.UID.generate_uid()
            series.modality = 'XX'

            self.series.append(series)


class Patient:

    """ Description

    Instance Variables:
    id          -- the patient's id
    first_name  -- the patient's first name
    last_name   -- the patient's last name
    gender      -- the patient's gender
    birth_date  -- the patient's birth date
    aliases     -- the patient's information permutations
    studies     -- the patient's studies

    Public Methods:
    generate_alias  -- makes a permutation of the patient's information

    """

    def generate_alias(self):
        print "hello alias"

    def generate_studies(self, num_studies, patient_birth_date):
        self.studies = []
        last_used_date = patient_birth_date
        for i in xrange(random.randint(num_studies[0], num_studies[1])):
            study = Study()

            study_datetime = utils.random_date_between(last_used_date,
                                                       datetime.datetime.now())
            study.study_date = study_datetime.date()
            study.study_time = study_datetime.time()
            last_used_date = study_datetime

            study.accession_number = utils.random_string([8, 16], False)
            study.study_description = 'FILL'
            study.study_instance_uid = dicom.UID.generate_uid()
            self.studies.append(study)


def generate_patients(num_patients, id_length, extra_chars):
    patients = []
    for i in xrange(num_patients):
        patient = Patient()

        sex = random.randint(0, 1)
        if sex == 0:
            patient.first_name = names.get_first_name('female')
            patient.sex = 'F'
        else:
            patient.first_name = names.get_full_name('male')
            patient.sex = 'M'

        patient.last_name = names.get_last_name()

        # generate patient id
        patient.id = utils.random_string(id_length, extra_chars)

        # generate patient birthday
        start = datetime.datetime(1900, 1, 1)
        end = datetime.datetime.now()
        patient.birth_date = utils.random_date_between(start, end)

        patients.append(patient)
    return patients
