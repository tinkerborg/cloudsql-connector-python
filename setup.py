from setuptools import setup

setup(name='cloudsql',
      version='0.1',
      description='Python connector for Google Cloud SQL.',
      url='https://github.com/tinkerborg/cloudsql-connector-python',
      author='tinkerborg',
      license='GPL',
      packages=['cloudsql'],
      install_requires=[
        'mysql-connector',
        'google-api-python-client'
      ],
      zip_safe=False)
