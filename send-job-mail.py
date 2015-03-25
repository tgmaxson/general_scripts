#! /usr/bin/env python
# 'send-job-mail.py' written by Tristan Maxson (tgmaxson@gmail.com)
import argparse
from tempfile import NamedTemporaryFile as tempf
from os import environ
from subprocess import PIPE, Popen

def e(var):
    return environ.get(var)

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

parser = argparse.ArgumentParser(
    description='Sends a formatted job email')
parser.add_argument(
    '--short-msg',
    '-a',
    type=str,
    default="",
    help='Short message to include in subject (default=msg)')
parser.add_argument(
    'msg',
    type=str,
    nargs='+',
    help='General message to include')
parser.add_argument(
    '--send-to',
    '-s',
    type=str,
    default=None,
    help='Address to send mail to (default=$MAILBOX)')

args = parser.parse_args()

msg  = " ".join(args.msg)
dest = args.send_to
if dest is None:
    dest = e('MAILBOX') or \
           e('mailbox') or \
           e('Mailbox')
if dest is None:
    print 'Either supply "--send-to" or set "mailbox" as a enviroment variable'
    exit()    
smsg = args.short_msg
if smsg is "":
    smsg = msg

def PBS(var):
    return e('PBS_{0}'.format(var)) or '??{0}??'.format(var)

subject = "{0}: {1} = {2}".format(PBS('JOBID').split('-')[0],
                                  PBS('JOBNAME'),
                                  smsg)
                                  
body='''PBS_JOBID = {0}
PBS_JOBNAME = {1}
PBS_O_WORKDIR = {2}
---------------------------------
PBS_WALLTIME = {3}
PBS_QUEUE = {4}
PBS_NUM_NODES = {5}
PBS_NUM_PPN = {6}
---------------------------------
{7}
'''.format(PBS('JOBID'),
           PBS('JOBNAME'),
           PBS('O_WORKDIR'),
           PBS('WALLTIME'),
           PBS('QUEUE'),
           PBS('NUM_NODES'),
           PBS('NUM_PPN'),
           msg)

with tempf() as f1:
    with tempf() as f2:
        f1.write(body)
        f1.flush()
        
        f2.write(cmdline('qstat -f {0}'.format(PBS('JOBID').split('.')[0])))
        f2.flush()
        
        cmdline("mail -a {3} -s '{1}' {2} < {0}".format(f1.name, subject, dest, f2.name))
