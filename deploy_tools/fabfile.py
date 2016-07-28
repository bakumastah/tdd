from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random
import os
import string

REPO_URL = 'git@github.com:bakumastah/tdd.git'


def deploy():
    site_folder = os.path.join('/home', env.user, 'sites', env.host)
    source_folder = os.path.join(site_folder, 'source')
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p {:s}'.format(os.path.join(site_folder, subfolder)))


def _get_latest_source(source_folder):
    print 'exists: ', os.path.join(source_folder + '.git')
    if exists(os.path.join(source_folder, '.git')):
        run('cd {:s} && git fetch'.format(source_folder))
    else:
        run('git clone {:s} {:s}'.format(REPO_URL, source_folder))
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run('cd {:s} && git reset --hard {:s}'.format(source_folder, current_commit))


def _update_settings(source_folder, site_name):
    settings_path = os.path.join(source_folder, 'superlists/settings.py')
    sed(settings_path, 'DEBUG = True', 'DEBUG = False')
    sed(settings_path, 'DOMAIN = \'localhost\'', 'DOMAIN = \'{:s}\''.format(site_name))
    secret_key_file = os.path.join(source_folder, 'superlists/secret_key.py')
    if not exists(secret_key_file):
        chars = string.letters + string.digits
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '{:s}'".format(key))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    virtualenv_folder = os.path.join(source_folder, '../virtualenv')
    pip_path = os.path.join(virtualenv_folder, 'bin/pip')
    if not exists(pip_path):
        run('virtualenv {:s}'.format(virtualenv_folder))
    run('{:s} install -r {:s}'.format(pip_path, os.path.join(source_folder, 'requirements.txt')))


def _update_static_files(source_folder):
     run('cd {:s} && ../virtualenv/bin/python manage.py collectstatic --noinput'.format(source_folder))


def _update_database(source_folder):
     run('cd {:s} && ../virtualenv/bin/python manage.py migrate --noinput'.format(source_folder))

