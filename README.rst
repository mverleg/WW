
Requirements
--------------------

Python:
* django 1.7.8 (and dependencies, automatic with pip)
* django-haystack
* whoosh
* pinyin (literal name of a python module)
* pytz

Client:
* bootstrap (already included)
* jquery (already included)

Ubuntu:
* sqlite3 (default on Ubuntu?)

A real database like postgres or mysql is recommended instead of sqlite3 for live website and possibly before. But as long as you have no important data to migrate, it is easy to switch, so play around first.

Setup
--------------------

* Install the requirements::

    pip install --upgrade django==1.7.8 mysql_python django-haystack whoosh pinyin pytz

* Create the database using (this will also create and show your account info the first time)::

    python2 source/manage.py migrate

* Compile translations using (if you get about four paths, it works)::

    python2 source/manage.py makemessages --all --ignore 'env'
    python2 source/manage.py compilemessages

* Build the search index using::

    python2 source/manage.py rebuild_index --noinput

* Start the server using (you can always start the server with this command, and stop it with ctrl + C; after syntax etc errors it needs to be restarted)::

    python2 source/manage.py runserver

* Open your browser and go to::

    http://127.0.0.1:8000/

* Notice the control panel link at the bottom? Have you tried searching for an empty string? Did you try setting your known language to Dutch?

Good luck!

VERY basic intro
--------------------
General files:

* manage.py / wsgi.py: These run the project, you can mostly ignore their content.
* settings.py: Settings for the project; no need to understand all of them at first.
* urls.py: This tells Django which URL should be handled by which code (like an index table).
* database.sqlite3: Database file, you can ignore it (contains all the data though, so be careful).
* searchindex.whoosh/: Contains search index stuff, can be recreated with python2 manage.py rebuild_index.

Then there are a bunch of apps, which each have their own directory. They are semi-isolated pieces of code that together make the whole website. They can't always be well isolated, but ideally they are completely independent so they can be re-used in new projects. They are built like this:

* urls.py: Like before. I like to organize them per app, su they are nested.
* views.py: These functions get information about what the user wants (request) and have to convert it into a page for the user to see (response). They use the models, templates and forms for this.
* models.py: Models are Python classes that represent all the stored data. The model gives the shape of the data (table in database), while each instance is a data entry (row in database). The database is created from the models (and migrations) automatically, and queries should also not be done by hand but rather use ModelName.objects.filter(name = ...). For example, each user is a Learner instance, which has a name, email, password, some settings, etc. The name can be seen to be a CharField (which will be a text column in the database). The current user can be found through request.user . You can then change this data, e.g. request.user.name = 'beibei', which will be saved to the database automatically if you call request.user.save() . They can also have most any functionality that is logical to associate with that concept. E.g. Translation is also a model, which of course has a language and a text (e.g. Dutch/"eekhoorn"). But it can also calculate it's own score (from votes), or give the url of it's own page (each phrase has a page). So derived data or data manipulation can also be part of models.
* forms.py: Where models are an abstraction of the database, forms are an abstration of HTML <form>s. Checking all user input is very tedious (is the age he submitted really a number? is it reasonable? etc). Forms can do that for you: tell which fields there are and which data they should expect, and they'll validate most of it. Then you can do stuff with it (in a view). A special type is the ModelForm, which lets the user change things about a model instance (e.g. change his name, or add a Translation).
* templates/: Templates give the basic structure and layout of pages. Basically they are the pages with all dynamic data left out (e.g. the user's name, which is different for every user). E.g. show_list.html gives the HTML layout of the page with a table which will contain the translations (which are different for every list, so dynamic). A view will provide these translations, which are then entered into the table using {{var}} for variables and {% for ...%} to create a row for every translation. Since a lot of pages share a lot of layout (background, menu, footer), templates can extend other templates (usually 'frame.html') where they just replace those {%block%}'s that are different.
* admin.py: This specifies what is visible in the control panel, but has no effect on the rest of the site. They are a special type of forms.
* migrations/: These specify model/database changes. If the models change, what should happen to the data? You don't need to read them and they're mostly auto-generated.
* search_indexes.py: This tells the search app (haystack) which data should be searchable, how, etc.
* middleware.py: This is code that runs for every page, in this case making sure each user has a language specified.
* static/ Some static files (stylesheets, javascript, images) that the user's browser should download as-is. You can ignore it for now.

The specific ones at this point are:

* basics: Mostly general stuff that is used by all other apps.
* learners: This is user account stuff; I extended the Django system. If you want to add user settings see models.py; ignore the rest.
* phrasebook: This has all the phrases (ideas) and translations (strings) related stuff.
* lists: This has all the stuff about lists of translations, and manages user access to it.
* opinions: This handles votes, maybe comments in the future. Pretty small.
* study: This handles the actual studying, as well as statistics about it. Many things to tweak here, but not the best starting point.

What you could do: Have a look at the site. If you want to change data or see the structure, see the control panel. For normal pages, if you are curious or notice a problem, find the page's url in urls.py to see which views.py function is responsible. Notice that the general pattern is to do some of these: Maybe check permissions. Get some data using models (instance = ModelName.objects.filter(...)). Maybe create a form (empty: FormName(None), filled out: FormName(request.POST)), if it's filled then check if it's valid. Maybe change some data (instance.save). Then either redirect or render a page (return render(request, 'templatename.html', {context}). Rendering happens by taking an HTML file and replacing all {{var}} with provided variables, possibly with simple logic like {%if...%} and {%for...%}. Templates are usually given a 'context', which is a dictionary whose keys will be available variables in the template (like {{var}} before). That's the basic idea of views. Just change some things and commit a lot so you can always go back. Do ask for help!

License
--------------------

The MIT License, see LICENSE file.


