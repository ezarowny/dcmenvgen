import datetime
import dicom
import os
import random
import string


def random_string(size, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def random_date_between(start, end):
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))


def create_dicom_file(patient, study, series, image, image_path):
    original_path = os.path.join(os.path.dirname(dicom.__file__), 'testfiles/CT_small.dcm')
    original = dicom.read_file(original_path)
    ds = original

    # change meta header
    # file_meta = dicom.dataset.Dataset()
    ds.file_meta.MediaStorageSOPClassUID = image.sop_class_uid
    ds.file_meta.MediaStorageSOPInstanceUID = image.sop_instance_uid
    ds.file_meta.ImplementationClassUID = dicom.UID.pydicom_UIDs.keys()[0]

    # create DICOM dataset
    # ds = dicom.dataset.FileDataset(image_path, {}, file_meta=file_meta, preamble="\0" * 128)

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
    ds.Modality = series.modality
    ds.SeriesInstanceUID = series.series_instance_uid
    ds.SeriesDate = series.series_datetime.date().strftime('%Y%m%d')
    ds.SeriesTime = series.series_datetime.time().strftime('%H%M%S')

    # add image information
    ds.SOPInstanceUID = image.sop_instance_uid
    ds.SOPClassUID = image.sop_class_uid

    # save file with dicom extension
    ds.save_as(image_path + '.dcm')
