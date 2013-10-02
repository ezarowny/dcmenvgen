import config
import datetime
import dicom
import names
import random
import utils


class Image:

    """ Description

    Instance Variables:
    sop_class_uid       -- sop class uid of the image

    Public Methods:

    """

    def __init__(self):
        self.sop_instance_uid = dicom.UID.generate_uid()


class Series:

    """ Description

    Instance Variables:
    modality            -- the modality of the series
    series_datetime     -- the date and time the series was performed
    series_instance_uid -- uniquely identifies the series
    images              -- the series' images

    Public Methods:
    generate_images     -- generates images for the series

    """

    def __init__(self, from_date, modality):
        self.modality = modality
        self.series_datetime = datetime.datetime.combine(
            from_date, datetime.datetime.now().time())
        self.series_instance_uid = dicom.UID.generate_uid()
        num_images = random.randint(config.min_images, config.max_images)
        self.images = self.generate_images(num_images)

    def generate_images(self, num_images):
        images = []
        for i in xrange(num_images):
            images.append(Image())
        return images


class Study:

    """ Description

    Instance Variables:
    study_datetime      -- the date and time the study was performed
    accession_number    -- the accession number for the study
    study_description   -- the description of the study
    study_instance_uid  -- uniquely identifies the study
    series              -- the study's series

    Public Methods:
    generate_series     -- generates series for the study

    """

    def __init__(self, from_date):
        self.study_datetime = utils.random_date_between(
            from_date, datetime.datetime.now())
        accession_length = random.randint(
            config.min_accn_length, config.max_accn_length)
        self.accession_number = utils.random_string(accession_length)
        modality = config.sample_data.random_modality()
        self.study_description = config.sample_data.random_study_description(
            modality)
        self.study_instance_uid = dicom.UID.generate_uid()
        num_series = random.randint(config.min_series, config.max_series)
        self.series = self.generate_series(
            num_series, self.study_datetime.date(), modality)

    def generate_series(self, num_series, study_date, modality):
        series = []
        for i in xrange(num_series):
            series.append(Series(study_date, modality))
        if config.gen_sr:
            if random.random() < config.gen_sr_chance:
                series.append(Series(study_date, 'SR'))
        return series


class Patient:

    """Represents a DICOM patient.

    Instance Variables:
    id          -- the patient's id
    sex         -- the patient's sex
    first_name  -- the patient's first name
    last_name   -- the patient's last name
    birth_date  -- the patient's birth date
    aliases     -- the patient's information permutations
    studies     -- the patient's studies

    Public Methods:
    generate_alias      -- makes a permutation of the patient's information
    generate_studies    -- generates studies for the patient

    """

    def __init__(self):
        id_length = random.randint(config.min_id_length, config.max_id_length)
        self.id = utils.random_string(id_length)
        self.sex = random.choice('MF')

        if self.sex == 'M':
            self.first_name = names.get_first_name('male')
        else:
            self.first_name = names.get_first_name('female')
        self.last_name = names.get_last_name()

        start = datetime.datetime(1900, 1, 1)
        end = datetime.datetime.now()
        self.birth_date = utils.random_date_between(start, end)

        self.studies = self.generate_studies(self.birth_date)

    def generate_alias(self):
        pass

    def generate_studies(self, start_datetime):
        studies = []
        last_datetime = start_datetime
        num_studies = random.randint(config.min_studies, config.max_studies)
        for i in xrange(num_studies):
            study = Study(last_datetime)
            studies.append(study)
            last_datetime = study.study_datetime
        return studies


def generate_patients(num_patients):
    patients = []
    for i in xrange(num_patients):
        patients.append(Patient())
    return patients
