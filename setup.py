from setuptools import setup

setup(name='weeblycloud',
      version='1.0.0',
      description='A client library for the Weebly Cloud API',
      url='https://github.com/Weebly/cloud-client-python',
      author='Daniel Nussbaum',
      author_email='daniel.e.nussbaum@gmail.com',
      license='Weebly',
      packages=['weeblycloud'],
      install_requires=[
          'wheel',
          'requests'
      ],
      zip_safe=True)
