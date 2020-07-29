import os
import search_file
from config import INSERT_OPTIONS_DICT, REPLACE_OPTIONS_DICT, TEST, USE_HEADER_LINKS

USE_HEADER_LINKS = os.getenv('BEAR_BR_SECTIONS', str(USE_HEADER_LINKS)).lower() == 'true'

WRITE_API_URL = "bear://x-callback-url/add-text"
OPEN_NOTE_API_URL = "bear://x-callback-url/open-note"

# You can change that (markdown rendering of links)
BACKREFERENCES_SECTION = '\n\n' + '-' * 3 + '\n'
DEFAULT_BACKREFERENCES_INTRO_TEXT = "This note is referenced in:\n"
BACKREFERENCES_INTRO_TEXT = DEFAULT_BACKREFERENCES_INTRO_TEXT
BACKREFERENCE_PREFIX = '\t*'

ROOT_SECTION_TEXT = "/"
ROOT_SECTION_TEXT = os.getenv('BEAR_ROOT_SECTION_TEXT', ROOT_SECTION_TEXT)

HOME = os.getenv('HOME', '')
LIBRARY = os.path.join(HOME, 'Library')
INSERT_OPTIONS = '&'.join(f'{k}={v}' for k, v in INSERT_OPTIONS_DICT.items())
REPLACE_OPTIONS = '&'.join(f'{k}={v}' for k, v in REPLACE_OPTIONS_DICT.items())

# Unique identifier that we use for backreference links
# (this is not interpreted by Bear when an ID is provided in open-note)
BACKREFMARKER = "__backreference_link__"

BEAR_DB = search_file.find_first(r'.*bear.*database\.sqlite$', LIBRARY)
# Maybe use "find ~ -iname database.sqlite | grep bear"?
BEAR_DB = os.getenv('BEAR_DB_LOCATION', BEAR_DB)

if not BEAR_DB:
    print(
        f"\n\nERROR: Couldn't locate Bear app database,"
        f"please provide a valid 'BEAR_DB_LOCATION' (as environment variable).\n\n"
    )
    exit(1)

# Just in case, this one needs to be non-empty
if not BACKREFERENCES_INTRO_TEXT:
    print("!! WARNING: This is ugly, but we need `BEAR_BACKREFERENCES_INTRO_TEXT` to be non-empty.\n"
          "It's even worse, we need it to be present in the document only if the backref section exists."
          "We used the default value instead of the empty string you provided. SOrRy.\n")
    BACKREFERENCES_INTRO_TEXT = DEFAULT_BACKREFERENCES_INTRO_TEXT


# For people that don't want to interact with python code
BACKREFERENCES_SECTION = os.getenv('BEAR_BACKREFERENCES_SEPARATOR', BACKREFERENCES_SECTION)
BACKREFERENCES_INTRO_TEXT = os.getenv('BEAR_BACKREFERENCES_INTRO_TEXT', BACKREFERENCES_INTRO_TEXT)
BACKREFERENCE_PREFIX = os.getenv('BEAR_BACKREFERENCE_PREFIX', BACKREFERENCE_PREFIX)
TEST = os.getenv('BEAR_TEST', str(TEST)).lower() == 'true'
