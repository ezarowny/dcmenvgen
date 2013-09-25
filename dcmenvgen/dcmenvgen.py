import argparse
import hierarchy


def get_args():
    parser = argparse.ArgumentParser(description='DICOM environment generator',
                                     prog='dcmenvgen')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    parser.add_argument('num_patients', type=int, metavar='N',
                        help='number of patients to generate')
    args = parser.parse_args()
    return args


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
    args = get_args()
    patients = hierarchy.generate_patients(args.num_patients)
    print_history(patients)


if __name__ == "__main__":
    main()
