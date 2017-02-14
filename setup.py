from setuptools import setup

setup(name='consync',
      version='0.1',
      description='Configuration sync to consul',
      url='http://github.com/elek/consync',
      author='Elek, Marton',
      author_email='elek@noreply.github.com',
      license='APACHE',
      packages=['consync'],
      entry_points = {
          'console_scripts': ['consync=consync.sync:main']
      },
      install_requires=[
         'watchdog',
         'jinja2',
         'requests',
          'python-consul'
      ],
      zip_safe=False)
