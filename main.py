"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
  main.py updatedb
"""
from docopt import docopt
import subprocess
import os

from alayatodo import app

    
def _run_sql(filename):
    try:
        subprocess.check_output(
            "sqlite3 %s < %s" % ('alayatodo.db', filename),
            # stderr=subprocess.STDOUT,
            shell=True
        )
    except (subprocess.CalledProcessError, ex):
        print(ex.output)
        os.exit(1)


if __name__ == '__main__':
    args = docopt(__doc__) 
    if args['initdb']:
        _run_sql('resources/database.sql')
        _run_sql('resources/fixtures.sql')
        print("AlayaTodo: Database initialized.")
    else:
        # added a flag to run the migration script
        if args['updatedb']:
            _run_sql('resources/migration.sql')
            print("AlayaTodo: Successfully Migrated DB")
        else:
            app.run(use_reloader=True)
