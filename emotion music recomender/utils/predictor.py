import sys
import os

# Get the parent directory of the current script (exp1)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..') # Go up one level from 'utils' to 'exp1'

# Add the project root to the Python path
sys.path.insert(0, project_root)

from config import MODEL_PATHS
# ... rest of your code






