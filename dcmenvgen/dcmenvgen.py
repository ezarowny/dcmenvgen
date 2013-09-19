import argparse
import hierarchy


def get_args():
    parser = argparse.ArgumentParser(description='DICOM environment generator',
                                     prog='dcmenvgen')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    parser.add_argument('num_patients', type=int, metavar='N',
                        help='number of patients to generate')
    parser.add_argument('-il', '--id_length', type=int,
                        metavar=('<min>', '<max>'), nargs=2, default=[8, 16],
                        help='[range] length of patient id (default: 8 16)')
    parser.add_argument('-epc', '--extra_pid_chars', action='store_true',
                        help='use space and underscore in patient ID' +
                        'generation')
    parser.add_argument('-ns', '--num_studies', type=int,
                        metavar=('<min>', '<max>'), nargs=2, default=[5, 10],
                        help='[range] number of studies to generate per' +
                        'patient (default: 5 10)')
    parser.add_argument('-ne', '--num_series', type=int,
                        metavar=('<min>', '<max>'), nargs=2, default=[1, 3],
                        help='[range] number of series to generate per' +
                        'study (default: 1 3)')
    parser.add_argument('-ni', '--num_images', type=int,
                        metavar=('<min>', '<max>'), nargs=2, default=[3, 20],
                        help='[range] number of images to generate per' +
                        'series (default: 3 20)')
    args = parser.parse_args()
    return args


def generate_history(args):
    patients = hierarchy.generate_patients(args.num_patients, args.id_length,
                                           args.extra_pid_chars)
    for patient in patients:
        patient.generate_studies(args.num_studies, patient.birth_date)
        for study in patient.studies:
            study.generate_series(args.num_series, study.study_date)
    #         for series in study.series:
    #             series.generate_images()
    return patients


def print_history(patients):
    for p in patients:
        print '=' * 50
        print '{0} {1}'.format(p.first_name, p.last_name)
        print 'Sex: {0}'.format(p.sex)
        print 'Patient ID: {0}'.format(p.id)
        print 'Birth Date: {0}'.format(p.birth_date.date().isoformat())

        for s in p.studies:
            print '\t=== STUDY ==='
            print '\tStudy UID: {0}'.format(s.study_instance_uid)
            print '\tStudy Description: {0}'.format(s.study_description)
            print '\tStudy Date: {0}'.format(s.study_date)
            print '\tStudy Time: {0}'.format(s.study_time)
            print '\tAccession Number: {0}'.format(s.accession_number)

            for e in s.series:
                print '\t\t=== SERIES ==='
                print '\t\tSeries UID: {0}'.format(e.series_instance_uid)
                print '\t\tModality: {0}'.format(e.modality)
                print '\t\tSeries Date: {0}'.format(e.series_date)
                print '\t\tSeries Time: {0}'.format(e.series_time)
    print '=' * 50


def main():
    args = get_args()
    patients = generate_history(args)
    print_history(patients)


if __name__ == "__main__":
    main()
