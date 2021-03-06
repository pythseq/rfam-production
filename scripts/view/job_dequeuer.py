#!/usr/bin/python

"""
Copyright [2009-2017] EMBL-European Bioinformatics Institute
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
     http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

"""
Description: A Python handler to run family view process by calling
             rfam_family_view.pl. Replaces job_dequeuer.pl.

Notes: 1. Call this script as rfamprod
       2. Keep # of concurrent jobs to 10 to avoid deadlocks
       3. Families defined in DEM_FAMS required double the memory to complete
          the view process
"""
# ---------------------------------IMPORTS-------------------------------------

import os
import sys
import subprocess
import time
import argparse
from config import rfam_config as rfc

# -----------------------------------------------------------------------------
# memory to allocate
MEM_R = 10000  # regular families
MEM_D = 20000  # mem demanding families
TMP_MEM = 4000  # temporary memory to allocate

PER_SYM_ASCII = 37  # ascii code for the percent symbol (%)

# memory demanding family accessions
DEM_FAMS = ["RF00002", "RF00005", "RF00177", "RF02542"]

# Path to rfam_family_view.pl on lsf
FAM_VIEW_PL = rfc.FAM_VIEW_PL
TMP_PATH = rfc.TMP_PATH
GROUP_NAME = rfc.RFAM_VIEW_GROUP

# -----------------------------------------------------------------------------


def job_dequeue_from_file(fam_pend_jobs, out_dir):
    """
    Calls family_view_process based on a list of family job_uuid pairs as
    listed in fam_jobs file

    fam_pend_jobs: A list of all pending rfam jobs obtained from
                   _post_process table export (rfam_acc\tuuid)
    out_dir: Path to output directory where .err and .out will be generated
             upon lsf job completion (to be used for debugging purposes)
    """

    # output file listing all lsf job ids per family accession. To be used as
    # a post-processing step to update rfam_live _post_process table
    fp_out = open(os.path.join(out_dir, "famview_job_ids.txt"), 'w')
    jobs_fp = open(fam_pend_jobs, 'r')

    # create script output directory
    os.mkdir(os.path.join(out_dir, "scripts"))

    # Submit all pending jobs to the cluster
    for job in jobs_fp:

        job = job.strip().split('\t')

        print "job: ", job

        # generate .sh file in FAM_VIEW_DIR on lsf have the outdir specified
        # through command line

        filepath = lsf_script_generator(str(job[0]), str(job[1]), out_dir)

        # if(not os.path.exists(os.path.join(out_dir,str(job[0])))):
        # os.mkdir(os.path.join(out_dir,str(job[0])))

        bsub_cmd = "bsub < %s" % (filepath)

        # submit job and retrieve job_id from shell
        proc = subprocess.Popen(
            bsub_cmd, shell=True, stdout=subprocess.PIPE)

        # get job_id from shell
        job_str = proc.communicate()[0].strip()
        job_id = job_str[5:12]

        # update file
        fp_out.write("%s\t%s\t%s\t%s\n" % (
            str(job[0]), str(job[1]), str(job_id), str(time.strftime('%Y-%m-%d %H:%M:%S'))))

    fp_out.close()

# -----------------------------------------------------------------------------


def lsf_script_generator(rfam_acc, uuid, out_dir):
    """
    Generates a shell script per family to ease re-running family view
    process upon failure

    rfam_acc: Family specific accession
    uuid: Family associated uuid
    out_dir: Path to output directory where scripts will be generated
    """

    mem = None

    if (rfam_acc in DEM_FAMS):
        mem = MEM_D
    else:
        mem = MEM_R

    # get where shell script will be generated
    filepath = os.path.join(os.path.join(out_dir, "scripts"), rfam_acc + ".sh")

    fp = open(filepath, 'w')

    filename = rfam_acc

    fv_cmd = "%s -id %s -f %s family" % (FAM_VIEW_PL, uuid, rfam_acc)

    fp.write("#!/bin/csh\n")

    #queue
    fp.write("#BSUB -q %s\n" % (rfc.VIEW_QUEUE))
    # memory allocation
    fp.write("#BSUB -M %d\n" % (mem))
    fp.write("#BSUB -R \"rusage[mem=%d,tmp=%d]\"\n" % (mem, TMP_MEM))

    # pre-process
    fp.write("#BSUB -E \"mkdir -m 777 -p /tmp/%s\"\n" % (uuid))
    fp.write("#BSUB -cwd \"/tmp/%s\"\n" % (uuid))
    # generate error/output files
    fp.write("#BSUB -o \"/tmp/%s/%sJ.out\"\n" % (uuid, chr(PER_SYM_ASCII)))
    fp.write("#BSUB -e \"/tmp/%s/%sJ.err\"\n" % (uuid, chr(PER_SYM_ASCII)))

    # command for lsf to copy .out file to output directory
    fp.write("#BSUB -f \"%s/%s_%sJ.out < /tmp/%s/%sJ.out\"\n" %
             (os.path.abspath(out_dir), filename, chr(PER_SYM_ASCII), uuid, chr(PER_SYM_ASCII)))

    # command for lsf to copy .err file to output directory
    fp.write("#BSUB -f \"%s/%s_%sJ.err < /tmp/%s/%sJ.err\"\n" %
             (os.path.abspath(out_dir), filename, chr(PER_SYM_ASCII), uuid, chr(PER_SYM_ASCII)))

    # clean /tmp directory on execution host
    fp.write("#BSUB -Ep \"rm -rf /tmp/%s\"\n" % (uuid))

    # submit jobs under specified group
    fp.write("#BSUB -g \"%s\"\n\n" % (GROUP_NAME))

    # rfam_view command
    fp.write(fv_cmd)

    fp.write("\n\n")
    fp.close()

    # return file path to submit job to lsf
    return filepath

# -----------------------------------------------------------------------------


def parse_arguments():
    """
    Basic argument parsing

    return: Python's argparse parser object
    """

    parser = argparse.ArgumentParser(description="View process dequeuer")

    parser.add_argument("--view-list", help="A list of rfam_acc\tuuids to run View plugins on", type=str)
    parser.add_argument("--dest-dir", help="An existing destination directory to store logs", type=str)

    return parser

# -----------------------------------------------------------------------------


if __name__ == '__main__':

    # minor input checks
    # LSF - rfamprod

    parser = parse_arguments()
    args = parser.parse_args()

    # need to check input provided are in valid format
    lsf_fam_jobs = args.view_list
    lsf_outdir = args.dest_dir

    job_dequeue_from_file(lsf_fam_jobs, lsf_outdir)

