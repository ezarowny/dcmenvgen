import datetime
import dicom
import random
import string
import time


def random_string(size, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def random_date_between(start, end):
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))


def generate_uid_with_delay():
    # This delay is necessary because PyDICOM UIDs include the time but the
    # smallest resoultion is microseconds, leaving us with non-unique id's
    # on faster systems.
    uid = dicom.UID.generate_uid()
    time.wait(0.001)
    return uid


def create_dicom_file(patient, study, series, image, image_path):
    original = dicom.read_file('images/{0}.dcm'.format(series.modality))
    ds = original

    # change meta header
    ds.file_meta.MediaStorageSOPInstanceUID = image.sop_instance_uid
    ds.file_meta.ImplementationClassUID = dicom.UID.pydicom_UIDs.keys()[0]

    # add patient information
    ds.PatientID = patient.id
    ds.PatientSex = patient.sex
    ds.PatientName = '{0}^{1}'.format(patient.last_name, patient.first_name)
    ds.PatientBirthDate = patient.birth_date.date().strftime('%Y%m%d')

    # add study information
    ds.StudyInstanceUID = study.study_instance_uid
    ds.StudyDescription = study.study_description
    ds.AccessionNumber = study.accession_number
    ds.StudyDate = study.study_datetime.date().strftime('%Y%m%d')
    ds.StudyTime = study.study_datetime.time().strftime('%H%M%S')

    # add series information
    ds.SeriesInstanceUID = series.series_instance_uid
    ds.SeriesDate = series.series_datetime.date().strftime('%Y%m%d')
    ds.SeriesTime = series.series_datetime.time().strftime('%H%M%S')

    # add image information
    ds.SOPInstanceUID = image.sop_instance_uid

    # save file with dicom extension
    ds.save_as(image_path + '.dcm')
