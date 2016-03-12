import os
from setuptools import setup, Command


class CleanCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


setup(name='Gonullu',
      version='0.4',
      description='Pisi Linux gonullu paket derleme uygulamasi',
      url='#',
      author='Ilker Manap',
      author_email='ilkermanap@gmail.com',
      contributor='Muhammet Dilmaç',
      contributor_email='m.dilmac1994@gmail.com',
      license='MIT',
      packages=['gonullu'],
      install_requires=[
          'argparse', 'requests', 'docker-py', 'psutil', 'colorama'
      ],
      scripts=['bin/gonullu'],
      include_package_data=True,
      zip_safe=False,
      cmdclass={
        'clean': CleanCommand,
    })
