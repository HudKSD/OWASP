from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MAPPINGS = ROOT / "docs" / "04-mappings"

REQUIRED_FILES = [
  "mapping-owasp-llm-top10-2025.md",
  "mapping-owasp-ml-top10-2023.md",
  "mapping-owasp-aisvs.md",
  "mapping-owasp-ai-testing-guide.md",
  "mapping-mitre-atlas.md",
  "mapping-aibom.md",
]

def main() -> int:
  missing = []
  for f in REQUIRED_FILES:
    if not (MAPPINGS / f).exists():
      missing.append(f)

  if missing:
    print("Missing mapping files:")
    for f in missing:
      print(f"- {f}")
    return 1

  print("OK: Mapping files present")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
