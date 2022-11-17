from distutils.core import setup

setup(
    author="Inuits",
    author_email="developers@inuits.eu",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    description="An async job system using RabbitMQ & CloudEvents",
    install_requires=[
        "cloudevents>=1.4.0",
        "Flask>=1.1.2",
        "rabbitmq-pika-flask>=1.2.15",
    ],
    license="GPLv2",
    name="job_helper",
    packages=["job_helper"],
    provides=["job_helper"],
    version="1.2",
)
