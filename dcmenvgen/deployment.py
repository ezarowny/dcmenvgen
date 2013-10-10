import config
import glob
import os
import random
import subprocess


def check_directories(deploy_dir):
    config_file = os.path.join(deploy_dir, 'dcmqrscp.cfg')
    if not os.path.isfile(config_file):
        return False
    for ae in config.archives['ae_titles'] + config.workstations['ae_titles']:
        ae_dir = os.path.join(deploy_dir, ae)
        if not os.path.isdir(ae_dir):
            return False
    return True


def setup_directories(deploy_dir):
    for ae in config.archives['ae_titles'] + config.workstations['ae_titles']:
        os.makedirs(os.path.join(deploy_dir, ae))


def create_ae_config(deploy_dir):
    config_file = os.path.join(deploy_dir, 'dcmqrscp.cfg')
    with open(config_file, 'w') as f:
        f.write('{}{}\n'.format('#', '=' * 71))
        f.write('#\n')
        f.write('# dcmenvgen generated configuration file for dcmqrdb\n')
        f.write('#\n')
        f.write('{}{}\n'.format('#', '=' * 71))
        f.write('\n')
        f.write('NetworkTCPPort  = {}\n'.format(config.archives['port']))
        f.write('MaxPDUSize      = 16384\n')
        f.write('MaxAssociations = 16\n')
        f.write('\n')
        f.write('AETable BEGIN\n')
        for ae in (config.archives['ae_titles'] +
                   config.workstations['ae_titles']):
            ae_dir = '{}/{}'.format(deploy_dir, ae)
            f.write('{}\t\t{}\t\tRW\t(500, 4096mb)\tANY\n'.format(ae, ae_dir))
        f.write('AETable END\n')


def distribute_images(dicom_dir, deploy_dir):
    # For some reason dcmqridx doesn't like subprocess passing in a path
    # with *'s even thought it works on the command line just fine. Instead,
    # we run the subprocess call for each image.
    for patient_dir in os.listdir(dicom_dir):
        patient_dir_path = os.path.join(dicom_dir, patient_dir)
        if os.path.isdir(patient_dir_path):
            for study_dir in os.listdir(patient_dir_path):
                study_images = glob.glob(os.path.join(patient_dir_path,
                                                      study_dir, '*', '*.dcm'))
                archive = random.choice(config.archives['ae_titles'])
                archive_dir = os.path.join(deploy_dir, archive)
                for image in study_images:
                    subprocess.call(['dcmqridx', archive_dir, image])


def launch(deploy_dir):
    config_file = os.path.join(deploy_dir, 'dcmqrscp.cfg')
    print 'Launching dcmqrscp...'
    try:
        subprocess.call(['dcmqrscp', '-c', '{}'.format(config_file)])
    except KeyboardInterrupt:
        print 'Quitting...'
