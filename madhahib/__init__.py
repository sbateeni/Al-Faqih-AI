# Madhahib package initialization
from .base_madhhab import BaseMadhhab
from .hanafi.hanafi_madhhab import HanafiMadhhab
from .maliki.maliki_madhhab import MalikiMadhhab
from .shafii.shafii_madhhab import ShafiiMadhhab
from .hanbali.hanbali_madhhab import HanbaliMadhhab

# Dictionary of all available madhahib
MADHAHIB = {
    'الحنفي': HanafiMadhhab,
    'المالكي': MalikiMadhhab,
    'الشافعي': ShafiiMadhhab,
    'الحنبلي': HanbaliMadhhab
}

def get_madhhab(name):
    """Get a madhhab instance by name"""
    if name in MADHAHIB:
        return MADHAHIB[name]()
    return None

def get_all_madhahib():
    """Get all available madhahib instances"""
    return {name: madhhab_class() for name, madhhab_class in MADHAHIB.items()}