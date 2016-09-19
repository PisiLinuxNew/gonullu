import os
from setuptools import setup, Command


class CleanCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info /tmp/gonullu/* /tmp/varpisi/*')


setup(name='Gonullu',
      version='0.6',
      description='Pisi Linux gonullu paket derleme uygulamasi',
      url='https://github.com/PisiLinuxNew/gonullu',
      author='Ilker Manap',
      author_email='ilkermanap@gmail.com',
      maintainer='Muhammet Dilmaç',
      maintainer_email='iletisim@muhammetdilmac.com.tr',
      license='MIT',
      packages=['gonullu'],
      install_requires=[
          'argparse', 'requests', 'docker-py', 'psutil', 'colorama', 'pyaml'
      ],
      scripts=['bin/gonullu'],
      include_package_data=True,
      package_data={
          'gonullu': ['config/*.yml']
      },
      zip_safe=False,
      cmdclass={
          'clean': CleanCommand,
      })
