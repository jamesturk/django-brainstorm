from distutils.core import setup

long_description = open('README.rst').read()

setup(
    name='django-brainstorm',
    version="0.2.0",
    package_dir={'brainstorm': 'brainstorm'},
    packages=['brainstorm'],
    package_data={'brainstorm': ['templates/brainstorm/*.html']},
    description='Django brainstorming site',
    author='James Turk',
    author_email='jturk@sunlightfoundation.com',
    license='BSD License',
    url='http://github.com/sunlightlabs/django-brainstorm/',
    long_description=long_description,
    platforms=["any"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Web Environment',
    ],
)
