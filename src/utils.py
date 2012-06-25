import harvest
import hamster.configuration
from collections import defaultdict
from dbus.exceptions import DBusException

def get_or_create_category(category_name, categories=[]):
    hamster_api = hamster.configuration.runtime.storage.conn

    try:
        category_id = hamster_api.GetCategoryId(category_name)
    except DBusException:
        category_id = hamster_api.AddCategory(category_name)

    return category_id

def get_or_create_activity(activity_name, category_id, activities=[]):
    hamster_api = hamster.configuration.runtime.storage.conn

    activity_id = None
    for aid, aname, cid, cname in activities:
        if aname == activity_name:
            activity_id = aid
            break

    if activity_id is None:
        activity_id = hamster_api.AddActivity(activity_name, category_id)

    return activity_id

def download_harvest_project_names(hostname, auth):
    session_info = harvest.API.make_session_info(hostname=hostname, auth=auth)
    harvest_api = harvest.API(session_info)
    hamster_api = hamster.configuration.runtime.storage.conn

    projects = harvest_api.projects()
    new_category_names = ['Harvest']
    new_activity_names = defaultdict(list)
    for p in projects:
        new_activity_names['Harvest'].extend([p['name'] + ' -- ' + t['name'] for t in p['tasks']])

    categories = hamster_api.GetCategories()
    for category_name in new_category_names:
        category_id = get_or_create_category(category_name, categories)
        activities = hamster_api.GetCategoryActivities(category_id)
        print '  {} ({})'.format(category_id, category_name)

        for activity_name in new_activity_names[category_name]:
            activity_id = get_or_create_activity(activity_name, category_id, activities)
            print '  {} ({})'.format(activity_id, activity_name)

def upload_hamster_facts(hostname, auth, start_date=None, end_date=None):
    session_info = harvest.API.make_session_info(hostname=hostname, auth=auth)
    harvest_api = harvest.API(session_info)
    hamster_api = hamster.configuration.runtime.storage.conn

    projects = harvest_api.projects()

    from datetime import date, datetime, timedelta
    import time
    def to_timestamp(dt):
        return time.mktime(dt.timetuple()) if dt is not None else 0

    cur_date = start_date
    while cur_date <= end_date:
        print 'Date ', cur_date

        start_timestamp = to_timestamp(cur_date)
        end_timestamp = to_timestamp(cur_date + timedelta(hours=23, 
                                                          minutes=59, 
                                                          seconds=59))

        facts = hamster_api.GetFacts(start_timestamp, end_timestamp, '')
        entries = harvest_api.entries(cur_date)

        print 'Existing Harvest entries:', entries

        new_entries = []
        print 'Hamster Facts'
        for (fact_id, start, end, description, activity_name, 
             activity_id, category_name, tags, ondate, delta) in facts:

            if category_name.lower() == 'harvest':
                start_time = datetime(*time.gmtime(start)[:7])
                end_time = datetime(*time.gmtime(end)[:7])
                
                print '{} - {}: {}'.format(
                    start_time.strftime('%I:%M%p').lower(),
                    end_time.strftime('%I:%M%p').lower(),
                    activity_name)

                project_name, task_name = activity_name.split(' -- ')
                project_id = None
                task_id = None
                for project in projects:
                    if project['name'].lower() == project_name.lower():
                        project_id = project['id']
                        for task in project['tasks']:
                            if task['name'].lower() == task_name.lower():
                                task_id = task['id']
                                break
                        break
                
                if project_id is None or task_id is None:
                    print 'None for project_id or task_id'
                    import pdb; pdb.set_trace()
                    continue

                new_entries.append(
                    dict(started_at=start_time, 
                         ended_at=end_time, 
                         spent_at=date(*time.gmtime(ondate)[:3]), 
                         notes=description,
                         project_id=project_id, task_id=task_id))
        
        cur_date += timedelta(days=1)
        print
        

        # Don't upload any entries until you're sure they're all ok.
        for entry in new_entries:
            harvest_api.add_entry(**entry)