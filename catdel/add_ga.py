import os
from pathlib import Path
import shutil
from bs4 import BeautifulSoup
import streamlit as st
from dotenv import load_dotenv
import logging

# Get the logger for this module
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get Google Analytics ID from environment variable
GA_ID_VALUE = os.getenv("GA_ID")
if not GA_ID_VALUE:
    raise EnvironmentError("GA_ID environment variable is not set")

# Constants for Google Analytics script injection
GA_ID = "google_analytics"
GA_SCRIPT_TEMPLATE = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
<script id='{ga_id_id}'>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{ga_id}');
</script>
"""
GA_SCRIPT = GA_SCRIPT_TEMPLATE.format(ga_id=GA_ID_VALUE, ga_id_id=GA_ID)
INDEX_HTML_PATH = Path(st.__file__).parent / "static" / "index.html"
BACKUP_SUFFIX = '.bck'

def inject_ga() -> None:
    """Injects Google Analytics script into the Streamlit index.html file."""
    try:
        if not INDEX_HTML_PATH.exists():
            logger.error("index.html file does not exist at %s", INDEX_HTML_PATH)
            return

        soup = BeautifulSoup(INDEX_HTML_PATH.read_text(), features="html.parser")
        if not soup.find(id=GA_ID):
            backup_index = INDEX_HTML_PATH.with_suffix(BACKUP_SUFFIX)
            if not backup_index.exists():
                shutil.copy(INDEX_HTML_PATH, backup_index)

            new_html = str(soup).replace('<head>', '<head>\n' + GA_SCRIPT)
            INDEX_HTML_PATH.write_text(new_html)
            logger.info("Google Analytics script injected successfully.")
        else:
            logger.info("Google Analytics script already exists in index.html.")
    except FileNotFoundError as e:
        logger.error("File not found: %s", e)
    except PermissionError as e:
        logger.error("Permission error: %s", e)
    except Exception as e:
        logger.error("Error injecting Google Analytics script: %s", e)

def inject_ga_if_on_server() -> None:
    """Injects Google Analytics script only if the server is running."""
    if st.config.get_option('server.runOnSave'):
        from catdel import add_ga
        add_ga.inject_ga()

if __name__ == '__main__':
    inject_ga()
