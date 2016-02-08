from setuptools import setup, find_packages

setup(
    name='captainhook',
    version='0.1',
    description='',
    long_description='',
    author='Praekelt Consulting',
    author_email='dev@praekelt.com',
    license='BSD',
    url='',
    packages=find_packages(),
    install_requires=[
        'django',
        'raven',
        'django-celery',
    ],
    include_package_data=True,
    tests_require=[
        'django-setuptest>=0.1.6',
    ],
    test_suite="setuptest.setuptest.SetupTestSuite",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
