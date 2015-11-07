from setuptools import setup

setup(name='Pisi Gonullu',
      version='0.1',
      description='Pisi Linux gonullu paket derleme uygulamasi',
      url='#',
      author='Ilker Manap',
      author_email='ilkermanap@gmail.com',
      license='MIT',
      packages=['pisiclient'],
      install_requires=[
          'argparse',   'requests'
      ],
      scripts=['bin/ciftlik-gonullu'],
      include_package_data=True,
      zip_safe=False)
