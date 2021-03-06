import calendar
import config
import datetime
import names
import random
import string
import utils


class Image:

    """Represents a DICOM image.

    Instance Variables:
    instance_datetime   -- date and time the image was captured
    sop_class_uid       -- sop class uid of the image

    """

    def __init__(self, from_date):
        self.instance_datetime = datetime.datetime.combine(
            from_date, datetime.datetime.now().time())
        self.sop_instance_uid = utils.generate_uid_with_delay()


class Series:

    """Represents a DICOM series.

    Instance Variables:
    modality            -- the modality of the series
    series_datetime     -- the date and time the series was performed
    series_instance_uid -- uniquely identifies the series
    images              -- the series' images

    Public Methods:
    generate_images     -- generates images for the series

    """

    def __init__(self, from_datetime, modality):
        self.modality = modality
        self.series_datetime = from_datetime
        self.series_instance_uid = utils.generate_uid_with_delay()
        num_images = random.randint(config.min_images, config.max_images)
        self.images = self.generate_images(num_images, self.series_datetime)

    def generate_images(self, num_images, series_datetime):
        images = []
        for i in xrange(num_images):
            images.append(Image(series_datetime))
        return images


class Study:

    """Represents a DICOM study.

    Instance Variables:
    study_datetime      -- the date and time the study was performed
    accession_number    -- the accession number for the study
    study_description   -- the description of the study
    study_instance_uid  -- uniquely identifies the study
    series              -- the study's series

    Public Methods:
    generate_series     -- generates series for the study

    """

    def __init__(self, from_datetime):
        self.study_datetime = utils.random_date_between(
            from_datetime, datetime.datetime.now())
        accession_length = random.randint(
            config.min_accn_length, config.max_accn_length)
        self.accession_number = utils.random_string(accession_length)
        modality = config.sample_data.random_modality(
            config.enabled_modalities)
        self.study_description = config.sample_data.random_study_description(
            modality)
        self.study_instance_uid = utils.generate_uid_with_delay()
        num_series = random.randint(config.min_series, config.max_series)
        self.series = self.generate_series(
            num_series, self.study_datetime, modality)

    def generate_series(self, num_series, study_datetime, modality):
        series = []
        # TODO: increment the time here logically
        for i in xrange(num_series):
            series.append(Series(study_datetime, modality))
        if config.gen_sr:
            if random.random() < config.gen_sr_chance:
                series.append(Series(study_datetime, 'SR'))
        return series


class Patient:

    """Represents a DICOM patient.

    Instance Variables:
    id          -- the patient's id
    sex         -- the patient's sex
    first_name  -- the patient's first name
    middle_name -- the patient's middle name
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

        sex = random.choice(['male', 'female'])
        if sex == 'male':
            self.sex = 'M'
        else:
            self.sex = 'F'

        self.first_name = names.get_first_name(sex)
        self.last_name = names.get_last_name()
        self.middle_name = ''
        if config.gen_mid_name:
            if random.random() < config.gen_mid_name_chance:
                if random.randint(0, 1):
                    self.middle_name = names.get_first_name(sex)
                else:
                    self.middle_name = names.get_first_name(sex)[0]

        start = datetime.datetime(1900, 1, 1)
        end = datetime.datetime.now()
        self.birth_date = utils.random_date_between(start, end)

        self.aliases = []
        if config.gen_alias:
            for i in xrange(config.gen_alias_max):
                if random.random() < config.gen_alias_chance:
                    self.aliases.append(self.generate_alias())

        self.studies = self.generate_studies(self.birth_date)

    def generate_alias(self):
        change = random.choice(config.enabled_alias_changes)
        if change == 'patient_id':
            id_length = random.randint(config.min_id_length,
                                       config.max_id_length)
            alias = ('id', utils.random_string(id_length))
        elif change == 'first_name':
            alias = (change, self.first_name[0])
        elif change == 'middle_name':
            if len(self.middle_name) > 1:
                if random.randint(0, 1):
                    alias = (change, self.middle_name[0])
                else:
                    alias = (change, '')
            elif len(self.middle_name) == 1:
                alias = (change, '')
            elif len(self.middle_name) == 0:
                alias = (change,
                         utils.random_string(1, string.ascii_uppercase))
        elif change == 'last_name':
            alias = (change, names.get_last_name())
        elif change == 'sex':
            if random.randint(0, 1):
                alias = (change, 'O')
            else:
                alias = (change, '')
        elif change == 'birth_date':
            part = random.choice(['day', 'month', 'year'])
            num_days = calendar.monthrange(self.birth_date.year,
                                           self.birth_date.month)
            if (self.birth_date.day == 1 or self.birth_date.month == 1 or
                    self.birth_date == 1900):
                amount = 1
            elif (self.birth_date.day == num_days[1] or
                  self.birth_date.month == 12):
                amount = -1
            else:
                amount = random.choice([-1, 1])
            if part == 'day':
                delta = self.birth_date.day + amount
                alias = (change, self.birth_date.replace(day=delta))
            if part == 'month':
                delta = self.birth_date.month + amount
                alias = (change, self.birth_date.replace(month=delta))
            else:
                delta = self.birth_date.year + amount
                alias = (change, self.birth_date.replace(year=delta))
        return alias

    def generate_studies(self, start_datetime):
        studies = []
        num_studies = random.randint(config.min_studies, config.max_studies)
        for i in xrange(num_studies):
            study = Study(self.birth_date)
            studies.append(study)
        return sorted(studies, key=lambda x: x.study_datetime)


def generate_patients(num_patients):
    patients = []
    for i in xrange(num_patients):
        patients.append(Patient())
    return patients
