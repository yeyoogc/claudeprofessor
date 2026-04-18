"""Run comment processing: reply to 'PROFESOR' comments + send guide DM."""
import argparse
from agents.comments import process_comments

parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true", help="Print matches, no API calls")
args = parser.parse_args()

process_comments(dry_run=args.dry_run)
