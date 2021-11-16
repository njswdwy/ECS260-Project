import datetime

from github import Github, RateLimitExceededException, BadCredentialsException, BadAttributeException, \
    GithubException, UnknownObjectException, BadUserAgentException
import pandas as pd
import requests
import datetime
import time
from urllib3 import Retry

access_token = "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"
projectList = pd.read_csv("cleaned_project_list.csv")


def get_mergedpr(projectList):
    df =  projectList

    for i in range(len(projectList)):
        project_name = df['Project Full Name'][i]
        try:
            g = Github(access_token, retry = Retry (total = 15, status_forcelist = (500, 502, 504), backoff_factor = 0.3), timeout=6000, per_page=100)
            repo = g.get_repo(project_name)
            print(project_name)
            pr_list = repo.get_pulls(state='closed',sort='created')
            merged_pr = 0
            for pr in pr_list:
                try:
                    print(f'Extracting data from PR # {pr}')
                    if pr.is_merged():
                        merged_pr += 1
                except RateLimitExceededException as e:
                    print(str(e.status))
                    print('Rate limit exceeded')
                    print('\n')
                    print(i)
                    print(project_name)
                    return  df
                    time.sleep(300)

                    continue
                except BadCredentialsException as e:
                    print(str(e.status))
                    print('Bad credentials exception')
                    print('\n')
                    break
                except UnknownObjectException as e:
                    print(str(e.status))
                    print('Unknown object exception')
                    print('\n')
                    break
                except GithubException as e:
                    print(str(e.status))
                    print('General exception')
                    print('\n')
                    break
                except requests.exceptions.ConnectionError as e:
                    print('Retries limit exceeded')
                    print(str(e))
                    print('\n')
                    time.sleep(10)
                    continue
                except requests.exceptions.Timeout as e:
                    print(str(e))
                    print('Time out exception')
                    print('\n')
                    time.sleep(10)
                    continue

            df['Merged PR Number'][i] = merged_pr

        except BadCredentialsException as e:
            print(str(e.status))
            print('Bad credentials exception')
            print('\n')
            break
        except UnknownObjectException as e:
            print(str(e.status))
            print('Unknown object exception')
            print('\n')
            break
        except requests.exceptions.Timeout as e:
            print(str(e))
            print('Timeout exception')
            time.sleep(10)
            continue
        except GithubException as e:

            print(str(e.status))
            print('GithubException')
            print('\n')
            continue
        except requests.exceptions.ConnectionError as e:
            print('Retries limit exceeded')
            print(str(e))
            print('\n')
            time.sleep(10)
            continue
        except requests.exceptions.Timeout as e:
            print(str(e))
            print('Time out exception')
            print('\n')
            time.sleep(10)
            continue
    return df

get_mergedpr(projectList)
