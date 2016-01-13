#!/usr/bin/env python2

import sys
import re

with open(sys.argv[1]) as tpl:
    content = tpl.read()

    for env in sys.argv[2:]:
        var, value = env.split('=', 1)
        content = content.replace('{{' + var + '}}', re.escape(value))

    print content
