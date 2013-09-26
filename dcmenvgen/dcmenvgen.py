import argparse
import hierarchy


def generate(args):
    patients = hierarchy.generate_patients(args.num_patients)
    print_history(patients)


def populate(args):
    print 'populate'


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
    parser_gen.set_defaults(func=generate)

    # create the parser for the "populate" command
    parser_gen = subparsers.add_parser('populate', help='populate dicom files')
    parser_gen.set_defaults(func=populate)

    # create the parser for the "deploy" command
    parser_gen = subparsers.add_parser('deploy',
                                       help='deploy workstations and archives')
    parser_gen.set_defaults(func=deploy)

    # call the function indicated by the selected subparser
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
