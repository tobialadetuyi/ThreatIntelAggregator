import os
import importlib
import logging
import time
import json
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# ======================
# LOGGING CONFIGURATION
# ======================
class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "source": record.name,
            "message": record.getMessage(),
            "exception": None
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)

# Configure rotating logs (max 1MB per file, keep 3 backups)
log_handler = RotatingFileHandler(
    'threat_intel.log',
    maxBytes=1_000_000,
    backupCount=3,
    encoding='utf-8'
)
log_handler.setFormatter(JSONFormatter())

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        log_handler,
        logging.StreamHandler()
    ]
)
logging.addLevelName(logging.WARNING, "WARN")  # Simplify level names

logger = logging.getLogger(__name__)

# ======================
# RETRY CONFIGURATION
# ======================
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

def retry_on_failure(func):
    """Decorator to retry a function on transient failures."""
    def wrapper(*args, **kwargs):
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.warning(f"Attempt {attempt}/{MAX_RETRIES} failed: {str(e)}")
                if attempt == MAX_RETRIES:
                    raise
                time.sleep(RETRY_DELAY * attempt)
    return wrapper

# ======================
# CORE FUNCTIONALITY
# ======================
load_dotenv()

@retry_on_failure
def fetch_threat_data(source):
    """
    Fetch threat intelligence data from a specified source with retries.
    
    Args:
        source (str): Name of the threat intel source (e.g., 'otx', 'abuseipdb').
    
    Returns:
        list: List of threat data dictionaries, or empty list on failure.
    """
    source = source.lower()
    try:
        logger.info(f"Attempting to fetch data from source: {source}")
        
        # Dynamically import the module and fetch function
        module = importlib.import_module(f"sources.{source}")
        fetch_func = getattr(module, f"fetch_from_{source}")
        
        logger.info(f"[{source.upper()}] Fetching data...")
        data = fetch_func()
        
        if not isinstance(data, list):
            logger.error(f"{source.upper()} returned invalid data format (expected list)")
            return []
        
        logger.info(f"Successfully fetched {len(data)} records from {source}")
        return data
    
    except ModuleNotFoundError:
        logger.error(f"Source module not found: {source}. Ensure 'sources/{source}.py' exists.")
        return []
    except AttributeError:
        logger.error(f"Function 'fetch_from_{source}' not found in {source}.py")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching from {source}: {str(e)}", exc_info=True)
        return []

