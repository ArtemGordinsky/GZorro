GZorro
------
A command-line file Gzipping utility
Useful for one-time manual compression of static websites or particular files. Resulting files are ready for serving (except for the metadata).

Testing info
------
Tested on OS X 10.8.4 with Python 2.7.2 and 3.3

Usage
------
`$ python Gzorro.py [directory path] or [file path]`

If a file is provided, a compressed version will be saved near the provided file, with a '.gz' appended to the original name.
If it's a directory, a "Compressed" folder will be created inside the given one with compressed files inside.

Todo
------
* More input validation (access, non-emptiness, etc)
* Confirmation of certain processes
