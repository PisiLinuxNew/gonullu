from setuptools import setup

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
      zip_safe=False)
