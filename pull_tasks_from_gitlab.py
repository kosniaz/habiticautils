# first part:
# get new issues from gitlab and add them to habitica, if not already there
# second part: for all habitica-gitlab tasks, check if any one of them is moved to done or closed and check the task
import requests

project_ids={
        "planv": 26891757,
        "covid-va": 1234,
        "river": 1111
        }
MY_USERNAME="kosniaz"
MY_ACCESS_TOKEN="glpat--hUsRcf38VouGfSKg_os"
my_header={"PRIVATE-TOKEN" : MY_ACCESS_TOKEN}

def get_gitlab_issues(project):

    r=requests.get("https://gitlab.com/api/v4/projects/"+str(project_ids[project])+"/issues?per_page=100",headers=my_header)
    #print(r.json())
    return r.json()

def is_assigned_to_me(issue_dict):
    if issue_dict['assignee']['username']==MY_USERNAME:
        return True
    else:
        return False

def is_watch_in_comments(project,issue_id):

    # e.g. https://gitlab.com/api/v4/projects/26891757/issues/1?per_page=100&order_by=updated_at
    r=requests.get("https://gitlab.com/api/v4/projects/"+str(project_ids[project])+"/issues/"+str(issue_id)+"/notes?per_page=100&order_by=updated_at",headers=my_header)
    # traverse comments from newer to older
    #print(r.json())
    for note in r.json():
        #print(note['author'])
        if "to GTD" in note['body'] and note['author']['username']==MY_USERNAME:
            return True
    return False

def get_issues_to_be_sycned(project):
    issues=get_gitlab_issues(project)
    print(issues[0]['iid'])
    issues_to_be_synced = [i for i in issues if is_watch_in_comments(project,i['iid'])]
    print(issues_to_be_synced)
    return issues_to_be_synced 
get_issues_to_be_sycned("planv")
#get_gitlab_issues("planv")

