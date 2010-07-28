import os

from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.3'
long_description = """
%s

%s
""" % (read("README.txt"),
       read("docs", "CHANGES.txt"))

setup(name='p4a.video',
      version=version,
      description="Plone4Artists video abstraction library",
      long_description=long_description,
      classifiers=[
          'Framework :: Zope2',
          'Framework :: Zope3',
          'Framework :: Plone',
          'Programming Language :: Python',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Multimedia :: Video'
          ],
      keywords='Plone4Artists video multimedia quicktime flash flv vodcast',
      author='Rocky Burt',
      author_email='rocky@serverzen.com',
      url='http://plone.org/products/plone4artistsvideo',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['p4a'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'p4a.subtyper',
          'p4a.common>=1.0',
          'p4a.z2utils>=1.0',
          'p4a.fileimage>=1.0',
          'hachoir_core==1.2',
          'hachoir_metadata==1.2',
          'hachoir_parser==1.2',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
