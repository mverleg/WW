
Goals
--------------------

* Lots...
* ...

Requirements
--------------------

* django
* django-haystack
* whoosh
* bootstrap (already included)
* jquery (already included)
* sqlite3 (default on Ubuntu?)
* pinyin (literal name of a python module)

A real database like postgres or mysql is recommended instead of sqlite3 for live website and possibly before. But as long as you have no important data to migrate, it is easy to switch, so play around first.

Setup
--------------------

* Install the requirements
* Create the database using (this will also create and show your output your account info)::

    python2 manage.py migrate

* Compile translations using (if you get about four paths, it works)::

    python manage.py compilemessages

* Build the search index using::

    python manage.py rebuild_index

* Start the server using (you can always start the server with this command, and stop it with ctrl + C; it needs to be restarted after some syntax etc errors)::

    python manage.py runserver

* Open your browser and go to::

    http://127.0.0.1:8000/

* (Notice the control panel link at the bottom).

Good luck!

Bugs
--------------------

* For some reason, the menu does fold for small windows, but the open button doesn't work.
* Deleting a phrase also deletes all statistics derived from; maybe hide the phrase instead
*


