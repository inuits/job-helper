import json
import string
from datetime import datetime
from enum import Enum
from flask import g
import requests


class Status(Enum):
    QUEUED = "queued"
    IN_PROGRESS = "in-progress"
    FINISHED = "finished"
    FAILED = "failed"


class JobHelper:
    def __init__(self, job_api_base_url):
        self.job_api_base_url = job_api_base_url

    def __patch_job(self, job):
        return requests.patch(
            "{}/jobs/{}".format(self.job_api_base_url, job["_id"]), json=job
        ).json()

    def create_new_job(self, job_info: string, job_type: string, asset_id=None, mediafile_id=None,
                       parent_job_id=None):
        new_job = {
            "job_type": job_type,
            "job_info": job_info,
            "status": Status.QUEUED.value,
            "start_time": str(datetime.utcnow()),
            "user": g.oidc_token_info["email"] if hasattr(g, "oidc_token_info") else "default_uploader",
            "asset_id": "" if asset_id is None else asset_id,
            "mediafile_id": "" if mediafile_id is None else mediafile_id,
            "parent_job_id": "" if parent_job_id is None else parent_job_id,
            "completed_jobs": 0,
            "amount_of_jobs": 1
        }
        job = json.loads(requests.post(
            "{}/jobs".format(self.job_api_base_url), json=new_job
        ).text)
        return job

    def progress_job(self, job, asset_id=None, mediafile_id=None, parent_job_id=None, amount_of_jobs=None, count_up_completed_jobs=False):
        if asset_id is not None:
            job["asset_id"] = asset_id
        if mediafile_id is not None:
            job["mediafile_id"] = mediafile_id
        if parent_job_id is not None:
            job["parent_job_id"] = parent_job_id
        if amount_of_jobs is not None:
            job["amount_of_jobs"] = amount_of_jobs
        if count_up_completed_jobs:
            job["completed_jobs"] = job["completed_jobs"] + 1
        job["status"] = Status.IN_PROGRESS.value
        return self.__patch_job(job)

    def finish_job(self, job):
        job["status"] = Status.FINISHED.value
        job["completed_jobs"] = job["amount_of_jobs"]
        job["end_time"] = str(datetime.utcnow())
        return self.__patch_job(job)

    def fail_job(self, job, error_message=""):
        job["status"] = Status.FAILED.value
        job["end_time"] = str(datetime.utcnow())
        job["error_message"] = error_message
        return self.__patch_job(job)