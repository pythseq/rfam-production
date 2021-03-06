'''
Created on 2 Mar 2016

@author: ikalvari

Description: This is a configuration file with all the paths on the cluster

'''

from config import rfam_local as cfl

# ------------------------------DATABASES--------------------------------------
# Dictionaries
RFAMLIVEPUB = cfl.RFAMLIVEPUB

RFAMLIVE = cfl.RFAMLIVE

RFAMLIVE_DJANGO = cfl.RFAMLIVE_DJANGO

#RFAM12 = cfl.RFAM12

RFAMLIVELOC = cfl.RFAMLIVELOC

#XFAMDEV = cfl.XFAMDEV
RFAMLOCAL = cfl.RFAMLOCAL
RFAMREL = cfl.RFAMREL

# ---------------------------------SEQDBs--------------------------------------

RFAM_SEED_DB = cfl.RFAM_SEED_SEQ_14_1

# ----------------------------Django settings----------------------------------

# DATABASES
RFAMDEV = cfl.RFAMDEV

RFAMLOC = cfl.RFAMLOC

# SETTINGS
SECRET_KEY = cfl.SECRET_KEY

# ---------------------------------PATHS---------------------------------------

FA_GEN = cfl.FA_GEN
ESL_PATH = cfl.ESL_SFETCH
RFAMSEQ_PATH = cfl.RFAMSEQ_PATH
FAM_VIEW_PL = cfl.FAM_VIEW_PL
ESL_SEQSTAT = cfl.ESL_SEQSTAT
TMP_PATH = cfl.TMP_PATH

ESL_FSEQ_PATH = cfl.ESL_FSEQ_PATH
FSR_PATH = cfl.FSR_PATH
FSR_LOCAL = cfl.FSR_LOCAL
ENA_URL = cfl.ENA_URL

# Maybe delete these
TAX_NODES_DUMP = cfl.TAX_NODES_DUMP
TAX_NAMES_DUMP = cfl.TAX_NAMES_DUMP
RFAM_NCBI_IDS = cfl.RFAM_NCBI_IDS
VALID_NCBI_IDS = cfl.VALID_NCBI_IDS
NCBI_RANKS = cfl.NCBI_RANKS

# -------------------------------LSF GROUPS------------------------------------
# rfamprod privileges required
FA_EXPORT_GROUP = cfl.FA_EXPORT_GROUP
RFAM_VIEW_GROUP = cfl.RFAM_VIEW_GROUP

# --------------------------------Rfam info------------------------------------

RFAM_EMAIL = cfl.RFAM_EMAIL
# RFAM_FTP = cfl.RFAM_FTP
BROWSER_HUB_DESC_URL = cfl.BROWSER_HUB_DESC_URL
