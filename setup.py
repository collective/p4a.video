from setuptools import setup, find_packages

version = '1.2'

setup(name='p4a.video',
      version=version,
      description="Plone4Artists video abstraction library",
      long_description="""p4a.video is a Python video library for dealing
with video files and their various means of storing/loading metadata.""",
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
      url='http://www.plone4artists.org/products/plone4artistsvideo',
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
