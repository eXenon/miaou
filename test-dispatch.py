#/usr/bin/python3

import dispatch

dispatch.dispatch("perl /tools/network/unix/massping/massping-h.pl -s {{file:/home/auditor/reports/Rexel/04-Pays-Bas/massping/ips.txt}} -o /home/auditor/reports/Rexel/04-Pays-Bas/top1000 -p top1000")
