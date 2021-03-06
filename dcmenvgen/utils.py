import config
import datetime
import dicom
import os
import random
import shutil
import string
import subprocess
import sys
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
    time.sleep(0.001)
    return uid


def send_dicom_files(files_to_send, ae_title, ip, port):
    subprocess.call(['storescu', ip, port, '-aec', ae_title, '+sd', '+r',
                     files_to_send])


def create_dicom_files(patients, output_directory, skip_patient_dir=False):
    if os.path.isfile(output_directory):
        print '{} already exists'.format(output_directory)
        sys.exit()
    if os.path.isdir(output_directory):
        overwrite = raw_input('{} already exists, overwrite? [y/n]: '.format(
            output_directory))
        if overwrite == 'n':
            sys.exit()
        else:
            shutil.rmtree(output_directory)
    os.makedirs(output_directory)

    for patient in patients:
        if skip_patient_dir:
            patient_dir = output_directory
        else:
            patient_dir = os.path.join(output_directory, patient.id)
            os.makedirs(patient_dir)
        for count, study in enumerate(patient.studies):
            temp = ('', '')
            if ((count + 1) % config.gen_alias_req) == 0 and patient.aliases:
                alias = patient.aliases.pop()
                temp = (alias[0], getattr(patient, alias[0]))
                setattr(patient, alias[0], alias[1])
            study_dir = os.path.join(patient_dir, study.study_instance_uid)
            os.makedirs(study_dir)
            for series in study.series:
                series_dir = os.path.join(study_dir,
                                          series.series_instance_uid)
                os.makedirs(series_dir)
                for image in series.images:
                    image_path = os.path.join(series_dir,
                                              image.sop_instance_uid)
                    create_dicom_file(patient, study, series, image,
                                      image_path)
            if temp != ('', ''):
                setattr(patient, temp[0], temp[1])


def create_dicom_file(patient, study, series, image, image_path):
    path = os.path.join(os.path.dirname(__file__), 'images',
                        '{}.dcm'.format(series.modality))
    original = dicom.read_file(path)
    ds = original

    # change meta header
    ds.file_meta.MediaStorageSOPInstanceUID = image.sop_instance_uid
    ds.file_meta.ImplementationClassUID = dicom.UID.pydicom_UIDs.keys()[0]

    # add patient information
    ds.PatientID = patient.id
    ds.PatientSex = patient.sex
    ds.PatientName = '{}^{}'.format(patient.last_name, patient.first_name)
    if patient.middle_name:
        ds.PatientName += '^{}'.format(patient.middle_name)
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
    ds.AcquisitionDate = image.instance_datetime.date().strftime('%Y%m%d')
    ds.AcquisitionTime = image.instance_datetime.time().strftime('%H%M%S')
    ds.ContentDate = image.instance_datetime.date().strftime('%Y%m%d')
    ds.ContentTime = image.instance_datetime.time().strftime('%H%M%S')
    ds.SOPInstanceUID = image.sop_instance_uid

    # save file with dicom extension
    ds.save_as(image_path + '.dcm')


def print_history(patients, verbose=False):
    for patient in patients:
        print '=' * 50
        if patient.middle_name:
            print '{} {} {}'.format(patient.first_name, patient.middle_name,
                                    patient.last_name)
        else:
            print '{} {}'.format(patient.first_name, patient.last_name)
        print 'Sex: {}'.format(patient.sex)
        print 'Patient ID: {}'.format(patient.id)
        print 'Birth Date: {}'.format(patient.birth_date.date().isoformat())
        print 'Aliases: {}'.format(patient.aliases)

        for study in patient.studies:
            print '\t=== STUDY ==='
            print '\tStudy UID: {}'.format(study.study_instance_uid)
            print '\tStudy Description: {}'.format(study.study_description)
            print '\tStudy Date: {}'.format(study.study_datetime.date())
            print '\tStudy Time: {}'.format(study.study_datetime.time())
            print '\tAccession Number: {}'.format(study.accession_number)

            if verbose:
                for series in study.series:
                    print '\t\t=== SERIES ==='
                    print '\t\tSeries UID: {}'.format(
                        series.series_instance_uid)
                    print '\t\tModality: {}'.format(series.modality)
                    print '\t\tSeries Date: {}'.format(
                        series.series_datetime.date())
                    print '\t\tSeries Time: {}'.format(
                        series.series_datetime.time())

                    for image in series.images:
                        print '\t\t\t=== IMAGE ==='
                        print '\t\t\tImage UID: {}'.format(
                            image.sop_instance_uid)
                        print '\t\tImage Date: {}'.format(
                            image.instance_datetime.date())
                        print '\t\tImage Time: {}'.format(
                            image.instance_datetime.time())
    print '=' * 50
