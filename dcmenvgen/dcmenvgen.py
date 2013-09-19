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
    args = parser.parse_args()
    return args


def generate_history(args):
    patients = hierarchy.generate_patients(args.num_patients, args.id_length,
                                           args.extra_pid_chars)
    # for patient in patients:
    #     patient.studies = patient.generate_studies()
    #     for study in patient.studies:
    #         study.series = study.generate_series()
    #         for series in study.series:
    #             series.images = series.generate_images()
    return patients


def print_history(patients):
    for p in patients:
        print '=' * 50
        print '{0} {1}'.format(p.first_name, p.last_name)
        print 'Sex: {0}'.format(p.sex)
        print 'Patient ID: {0}'.format(p.id)
        print 'Birth Date: {0}'.format(p.birth_date.date().isoformat())
    print '=' * 50


def main():
    args = get_args()
    patients = generate_history(args)
    print_history(patients)


if __name__ == "__main__":
    main()
