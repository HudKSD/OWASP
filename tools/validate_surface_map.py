import json
import sys
from pathlib import Path

try:
  import jsonschema
except ImportError:
  print("Missing dependency: jsonschema. Install with: pip install jsonschema")
  sys.exit(2)

def main() -> int:
  if len(sys.argv) != 2:
    print("Usage: python tools/validate_surface_map.py path/to/map.json")
    return 2
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
