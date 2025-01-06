#!/usr/bin/env python3

from json import loads, dumps
from boto3 import client
from datetime import datetime
from dataclasses import dataclass


@dataclass
class ScheduleName:
    group: str
    name: str


@dataclass
class Schedule:
    group: str
    name: str
    schedule: str
    enabled: bool
    function: str
    event: dict
    dispatch_at: datetime = None


class AWSScheduler:
    def __init__(self) -> None:
        self.c = client("scheduler")

    def list(self, group: str = "default") -> list[ScheduleName]:
        return [
            ScheduleName(group=x["GroupName"], name=x["Name"])
            for x in self.c.list_schedules(GroupName=group)["Schedules"]
        ]

    def get(self, info: ScheduleName) -> Schedule:
        res = self.c.get_schedule(GroupName=info.group, Name=info.name)
        schedule = Schedule(
            group=info.group,
            name=info.name,
            schedule=res["ScheduleExpression"],
            enabled=res["State"] == "ENABLED",
            function=res["Target"]["Arn"],
            event=None,
        )
        try:
            schedule.event = loads(res["Target"]["Input"])
        except:
            pass
        if "at" in schedule.schedule:
            dt = datetime.strptime(schedule.schedule, "at(%Y-%m-%dT%H:%M:%S)")
            schedule.dispatch_at = dt
        return schedule

    def add(
        self,
        group: str,
        name: str,
        function: str,
        role: str,
        dispatch_at: datetime,
        event: dict,
    ) -> dict:
        return self.c.create_schedule(
            ActionAfterCompletion="DELETE",
            FlexibleTimeWindow={"Mode": "OFF"},
            GroupName=group,
            Name=name,
            ScheduleExpression=dispatch_at.strftime("at(%Y-%m-%dT%H:%M:%S)"),
            ScheduleExpressionTimezone="Asia/Tokyo",
            State="ENABLED",
            Target={
                "Arn": function,
                "Input": dumps(event),
                "RetryPolicy": {
                    "MaximumEventAgeInSeconds": 86400,
                    "MaximumRetryAttempts": 0,
                },
                "RoleArn": role,
            },
        )

    def delete(self, info: ScheduleName) -> dict:
        return self.c.delete_schedule(GroupName=info.group, Name=info.name)
