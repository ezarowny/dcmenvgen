import config
import os
import subprocess


def setup_directories(deploy_dir):
    for ae in config.archives['ae_titles']:
        os.makedirs(os.path.join(deploy_dir, ae))
    for ae in config.workstations['ae_titles']:
        os.makedirs(os.path.join(deploy_dir, ae))


def create_ae_config(deploy_dir):
    config_file = os.path.join(deploy_dir, 'dcmqrscp.cfg')
    with open(config_file, 'w') as f:
        f.write('{}{}\n'.format('#', '='*71))
        f.write('#\n')
        f.write('# dcmenvgen generated configuration file for dcmqrdb\n')
        f.write('#\n')
        f.write('{}{}\n'.format('#', '='*71))
        f.write('\n')
        f.write('NetworkTCPPort  = {}\n'.format(config.archives['port']))
        f.write('MaxPDUSize      = 16384\n')
        f.write('MaxAssociations = 16\n')
        f.write('\n')
        f.write('AETable BEGIN\n')
        for ae in config.archives['ae_titles']:
            ae_dir = '{}/{}'.format(deploy_dir, ae)
            f.write('{}\t\t{}\t\tRW\t(500, 4096mb)\tANY\n'.format(ae, ae_dir))
        for ae in config.workstations['ae_titles']:
            ae_dir = '{}/{}'.format(deploy_dir, ae)
            f.write('{}\t\t{}\t\tRW\t(500, 4096mb)\tANY\n'.format(ae, ae_dir))
        f.write('AETable END\n')


def launch(deploy_dir):
    config_file = os.path.join(deploy_dir, 'dcmqrscp.cfg')
    subprocess.call(['dcmqrscp', '-c', '{}'.format(config_file)])
