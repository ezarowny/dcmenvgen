import argparse
import cPickle
import hierarchy
import os
import shutil
import sys
import utils


def generate(args):
    patients = hierarchy.generate_patients(args.num_patients)
    if args.verbose:
        print_history(patients)
    if os.path.isfile(args.output_file):
        overwrite = raw_input('{0} already exists, overwrite? [y/n]: '.format(
            args.output_file))
        if overwrite == 'n':
            sys.exit()
    with open(args.output_file, 'wb') as out_file:
        cPickle.dump(patients, out_file, 2)


def populate(args):
    with open(args.patients_file, 'rb') as in_file:
        patients = cPickle.load(in_file)

    if os.path.isfile(args.output_directory):
        print '{0} already exists'.format(args.output_directory)
        sys.exit()
    if os.path.isdir(args.output_directory):
        overwrite = raw_input('{0} already exists, overwrite? [y/n]: '.format(
            args.output_directory))
        if overwrite == 'n':
            sys.exit()
        else:
            shutil.rmtree(args.output_directory)
    os.makedirs(args.output_directory)

    for patient in patients:
        patient_dir = os.path.join(args.output_directory, patient.id)
        os.makedirs(patient_dir)
        for study in patient.studies:
            study_dir = os.path.join(patient_dir, study.study_instance_uid)
            os.makedirs(study_dir)
            for series in study.series:
                series_dir = os.path.join(study_dir, series.series_instance_uid)
                os.makedirs(series_dir)
                for image in series.images:
                    image_path = os.path.join(series_dir, image.sop_instance_uid)
                    utils.create_dicom_file(patient, study, series, image, image_path)


def deploy(args):
    print 'deploy'


def print_history(patients):
    for patient in patients:
        print '=' * 50
        print '{0} {1}'.format(patient.first_name, patient.last_name)
        print 'Sex: {0}'.format(patient.sex)
        print 'Patient ID: {0}'.format(patient.id)
        print 'Birth Date: {0}'.format(patient.birth_date.date().isoformat())

        for study in patient.studies:
            print '\t=== STUDY ==='
            print '\tStudy UID: {0}'.format(study.study_instance_uid)
            print '\tStudy Description: {0}'.format(study.study_description)
            print '\tStudy Date: {0}'.format(study.study_datetime.date())
            print '\tStudy Time: {0}'.format(study.study_datetime.time())
            print '\tAccession Number: {0}'.format(study.accession_number)

            for series in study.series:
                print '\t\t=== SERIES ==='
                print '\t\tSeries UID: {0}'.format(series.series_instance_uid)
                print '\t\tModality: {0}'.format(series.modality)
                print '\t\tSeries Date: {0}'.format(
                    series.series_datetime.date())
                print '\t\tSeries Time: {0}'.format(
                    series.series_datetime.time())

                for image in series.images:
                    print '\t\t\t=== IMAGE ==='
                    print '\t\t\tImage UID: {0}'.format(image.sop_instance_uid)
                    print '\t\t\tSOP Class UID: {0}'.format(
                        image.sop_class_uid)
    print '=' * 50


def main():
    parser = argparse.ArgumentParser(description='DICOM environment generator',
                                     prog='dcmenvgen')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    subparsers = parser.add_subparsers(title='commands', metavar='<command>')

    # create the parser for the "generate" command
    parser_gen = subparsers.add_parser('generate', help='generate patients')
    parser_gen.add_argument('num_patients', type=int,
                            help='number of patients to generate')
    parser_gen.add_argument('-o', '--output_file', default='patients.pkl',
                            help='file to output patients to')
    parser_gen.add_argument('-v', '--verbose', action='store_true',
                            help='verbose output')
    parser_gen.set_defaults(func=generate)

    # create the parser for the "populate" command
    parser_pop = subparsers.add_parser('populate', help='populate dicom files')
    parser_pop.add_argument('patients_file',
                            help='patients file generated by dcmenvgen')
    parser_pop.add_argument('-o', '--output_directory', default='dicom',
                            help='directory to place populated DICOM files')
    parser_pop.set_defaults(func=populate)

    # create the parser for the "deploy" command
    parser_dep = subparsers.add_parser('deploy',
                                       help='deploy workstations and archives')
    parser_dep.set_defaults(func=deploy)

    # call the function indicated by the selected subparser
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
