Hamster-Harvester
=================

Set up
------
Copy the ``settings.py.template`` file to ``settings.py`` and fill it in with your
actual server information.

Downloading
-----------
::

   ./download_projects.py                                                            

Download the projects and tasks from Harvest into your Hamster database.  This just
seeds the DB with the task names; it does not retrieve any of the work entries.

Uploading
---------
::

   ./upload_activities.py 2012-06-18 2012-06-22                                      

Upload the facts from the Hamster DB in   the Harvest category between June 18, 2012
and June 22, 2012, inclusive.
