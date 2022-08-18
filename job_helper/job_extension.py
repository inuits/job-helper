import json
import string
from datetime import datetime

from cloudevents.http import CloudEvent, to_json
from rabbitmq_pika_flask import RabbitMQ

from job_helper.Status import Status
from job_helper.Job import Job


class JobExtension:
    def __init__(self, rabbit: RabbitMQ):
        self.rabbit = rabbit

    def create_new_job(
        self,
        job_info: string,
        job_type: string,
        asset_id=None,
        mediafile_id=None,
        parent_job_id=None,
    ):
        new_job = Job(
            job_type=job_type,
            job_info=job_info,
            asset_id=asset_id,
            mediafile_id=mediafile_id,
            parent_job_id=parent_job_id,
        )

        self.__send_cloud_event(new_job.__dict__, "dams.job_created")
        return new_job

    def progress_job(
        self,
        job,
        asset_id=None,
        mediafile_id=None,
        parent_job_id=None,
        amount_of_jobs=None,
        count_up_completed_jobs=False,
    ):

        if asset_id is not None:
            job.asset_id = asset_id
        if mediafile_id is not None:
            job.mediafile_id = mediafile_id
        if parent_job_id is not None:
            job.parent_job_id = parent_job_id
        if amount_of_jobs is not None:
            job.amount_of_jobs = amount_of_jobs
        if count_up_completed_jobs:
            job.count_up_completed_jobs()
        job.status = Status.IN_PROGRESS.value
        self.__send_cloud_event(job.__dict__, "dams.job_changed")
        return job

    def finish_job(self, job, parent_job=None):
        job.status = Status.FINISHED.value
        job.completed_jobs = job.amount_of_jobs
        job.end_time = str(datetime.utcnow())
        if job.parent_job_id not in ["", None] and parent_job is not None:
            self.progress_job(parent_job, count_up_completed_jobs=True)
        self.__send_cloud_event(job.__dict__, "dams.job_changed")
        return job

    def fail_job(self, job, error_message=""):
        job.status = Status.FAILED.value
        job.end_time = str(datetime.utcnow())
        job.error_message = error_message
        self.__send_cloud_event(job.__dict__, "dams.job_changed")
        return job

    def __send_cloud_event(self, job, event_type):
        attributes = {"type": event_type, "source": "dams"}
        event = CloudEvent(attributes, job)
        message = json.loads(to_json(event))
        self.rabbit.send(message, routing_key=event_type)
