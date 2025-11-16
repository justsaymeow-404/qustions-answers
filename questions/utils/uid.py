from __future__ import annotations

import logging

from dataclasses import dataclass
from typing import Optional
from uuid import UUID, uuid4

from rest_framework.exceptions import ValidationError
from rest_framework.request import Request


logger = logging.getLogger('questions')


@dataclass(frozen=True)
class UIDResult:
    uid: UUID
    need_set_cookie: bool


def get_or_create_uid(request:Request) -> UIDResult:
    raw = request.headers.get('X-User-ID')
    if raw:
        try:
            uid = UUID(str(raw))
            logger.info('UID from header uid=%s', str(uid))
            return UIDResult(uid=uid, need_set_cookie=False)
        except ValueError:
            logger.warning('Invalid X-User-ID header %s', raw)
            raise ValidationError({'X-User-ID': 'Invalid UUID'})
    
    raw = request.COOKIES.get('uid')
    if raw:
        try:
            uid = UUID(str(raw))
            logger.info('UID from cookie id=%s', str(uid))
            return UIDResult(uid=uid, need_set_cookie=False)
        except ValueError:
            logger.warning('Invalid uid cookie, will generate new %s', raw)
    
    new_uid = uuid4()
    logger.info('Generated new UID=%s', str(new_uid))
    return UIDResult(uid=new_uid, need_set_cookie=True)
