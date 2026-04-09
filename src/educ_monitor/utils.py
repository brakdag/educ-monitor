import logging
from datetime import datetime

logger = logging.getLogger("educ_monitor.utils")

def parse_date(date_str: str | None) -> str | None:
    """
    Attempts to parse a date string into ISO format (YYYY-MM-DD).
    
    Supports multiple common formats used by the DGE API and handles 
    cleaning of whitespace or trailing time information.
    
    Args:
        date_str (str | None): The raw date string from the API.
        
    Returns:
        str | None: The date in YYYY-MM-DD format, or None if parsing fails.
    """
    if not date_str:
        return None

    # 1. Clean the string: take only the first part (before space) and strip whitespace
    clean_date = date_str.split(' ')[0].strip()
    
    # 2. Define supported formats in order of probability
    # %y is 2-digit year, %Y is 4-digit year
    formats = ["%d/%m/%y", "%d/%m/%Y", "%d-%m-%y", "%d-%m-%Y", "%Y-%m-%d"]
    
    for fmt in formats:
        try:
            return datetime.strptime(clean_date, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
            
    logger.warning(f"Could not parse date string: '{date_str}' using supported formats.")
    return None