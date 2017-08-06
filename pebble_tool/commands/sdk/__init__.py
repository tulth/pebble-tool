from __future__ import absolute_import, print_function
__author__ = 'katharine'

import os
import subprocess
import logging

from pebble_tool.exceptions import ToolError, MissingSDK
from pebble_tool.sdk import add_tools_to_path, sdk_path, sdk_manager
from ..base import BaseCommand

logger = logging.getLogger("pebble_tool.commands.sdk")


class SDKCommand(BaseCommand):
    def get_sdk_path(self):
        path = sdk_manager.path_for_sdk(self.sdk) if self.sdk is not None else sdk_path()
        logger.debug("SDK path: %s", path)
        if not os.path.exists(os.path.join(path, 'pebble', 'waf')):
            raise MissingSDK("SDK unavailable; can't run this command.")
        return path

    @classmethod
    def add_parser(cls, parser):
        parser = super(SDKCommand, cls).add_parser(parser)
        parser.add_argument('--sdk', nargs='?', help='SDK version to use for this command, if not the '
                                                     'currently selected one.')
        return parser

    def add_arm_tools_to_path(self):
        add_tools_to_path()

    def __call__(self, args):
        super(SDKCommand, self).__call__(args)
        self.sdk = args.sdk
        self.add_arm_tools_to_path()
