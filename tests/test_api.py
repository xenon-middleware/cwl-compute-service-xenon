# -*- coding: utf-8 -*-

from .context import app
from app import app

import json


def test_api_def():
	swagger_text = app.get_swagger()
	swagger = json.loads(swagger_text)
	assert swagger['info']['title'] == 'Compute Service API'

