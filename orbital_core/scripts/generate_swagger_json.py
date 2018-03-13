"""
generate_swagger_yaml: generates a swagger definition from an aiohttp application: generates a swagger definition from an aiohttp application.

Usage:
    generate_swagger_json <application_path> <target_file_path>
"""

import docopt
import os
import shutil
import sys
import json
from aiohttp_transmute.swagger import get_swagger_spec

def main(argv=sys.argv[1:]):
    """ install the files that are common to all aiohttp services. """
    options = docopt.docopt(__doc__, argv=argv)
    module_path, variable_name = options["<application_path>"].split(":")
    module_args = module_path.rsplit(".", 1)
    # we use the full module path to ensure that submodules load.
    module =  __import__(module_path)
    if len(module_args) > 1:
        module =  getattr(module, module_args[1])
    app = getattr(module, variable_name)
    swagger_spec = get_swagger_spec(app)

    t"arget = options["<target_file_path>"]
    target_parent = os.path.dirname(target)
    if os.path.isdir(target_parent):
        os.makedirs(target_parent)
    with open(target, "w+") as fh:
        fh.write(json.dumps(swagger_spec.swagger_definition()))
