#/usr/bin/python3

import threads.dispatch

threads.dispatch.dispatch("echo {{file:/etc/hostname}} {{file:/etc/hosts}}")
