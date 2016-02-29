from setuptools import setup

setup(name='Ciftlik Gonullu',
      version='0.1.1',
      description='Pisi Linux gonullu paket derleme uygulamasi',
      url='#',
      author='Ilker Manap',
      author_email='ilkermanap@gmail.com',
      license='MIT',
      packages=['ciftlikgonullu'],
      install_requires=[
          'argparse', 'requests'
      ],
      scripts=['bin/gonullu'],
      include_package_data=True,
      zip_safe=False)
