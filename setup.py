from distutils.core import setup

setup(
    name='job_helper',
    version='0.1.5',
    description="Job helper to use with the job api",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ],
    author='Matthias Dillen',
    author_email='matthias.dillen@inuits.eu',
    license='MIT',
    packages=[
        'job_helper'
    ],
    provides=['job_helper']
)
