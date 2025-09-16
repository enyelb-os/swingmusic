"""
Pakage for all extra functionalities.
"""

from flask_openapi3 import APIBlueprint, Tag

tag = Tag(name="Extra", description="Extra functionalities")
api = APIBlueprint("extra", __name__, url_prefix="/extra")

# Import sub-modules to register their blueprints
from . import download

# Register blueprints
api.register_api(download.api)