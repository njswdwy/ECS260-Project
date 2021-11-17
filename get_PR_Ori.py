import datetime

from github import Github, RateLimitExceededException, BadCredentialsException, BadAttributeException, \
    GithubException, UnknownObjectException, BadUserAgentException
import pandas as pd
import requests
import time
from urllib3 import Retry

access_token = ""


f = open('RP_Log.txt', 'a')
f.write((str(datetime.datetime.now())))


cleanedProjectList = pd.read_csv('PRs_dataset/cleaned_project_list.csv')


#get pr data
def extract_project_PRs(pr_list, sDate, eDate):
    df_PRs = pd.DataFrame()
    dateLimit = False

    merged_pr_count = 0
    for pr in pr_list:
            try:
                # print(g.rate_limiting)
                print(f'Extracting data from PR # {pr.number}')
                PRsDate = pr.created_at
                if sDate <= PRsDate and eDate >= PRsDate:
                    print('Yes')
                    dateLimit = True
                elif dateLimit:
                    print('Not in date')
                    break
                else:
                    print('No')
                    continue
                df_PRs = df_PRs.append({
                    'pr_id': pr.id,  # PRs features
                    'pr_title': pr.title,
                    'pr_number': pr.number,
                    'additions': pr.additions,
                    'deletions': pr.deletions,
                    'pr_changed_files': pr.changed_files,  # number of changed files
                    'pr_commits_count': pr.commits,  # number of commits
                    'pr_comments_count': pr.comments,
                    'pr_review_comments_count': pr.review_comments,
                    'pr_created_at': pr.created_at,  # when this pull request was created.
                    'pr_closed_at': pr.closed_at,  # when this pull request was closed.
                    'contributor': pr.user.name,  # Contributor's information
                    'contributor_id': pr.user.id,
                    'is_merged': pr.is_merged(),
                    'pr_merged_at': pr.merged_at,

                }, ignore_index=True)
            except RateLimitExceededException as e:
                print('Rate limit exceeded')
                f.write(str(e.status))
                f.write('Rate limit exceeded')
                f.write('\n')
                time.sleep(3600)
                continue
            except BadCredentialsException as e:
                f.write(str(e.status))
                f.write('Bad credentials exception')
                f.write('\n')
                break
            except UnknownObjectException as e:
                f.write(str(e.status))
                f.write('Unknown object exception')
                f.write('\n')
                break
            except GithubException as e:
                f.write(str(e.status))
                f.write('General exception')
                f.write('\n')
                break
            except requests.exceptions.ConnectionError as e:
                f.write('Retries limit exceeded')
                f.write(str(e))
                f.write('\n')
                time.sleep(10)
                continue
            except requests.exceptions.Timeout as e:
                f.write(str(e))
                f.write('Time out exception')
                f.write('\n')
                time.sleep(10)
                continue
            except:
                f.write('exception')
                continue

    return df_PRs


for i in range(5, len(cleanedProjectList)):
    try:
        projectName = cleanedProjectList['Project Full Name'][i]
        startDate = datetime.datetime.strptime(cleanedProjectList['Project Startdate'][i], '%m/%d/%Y')
        endDate = datetime.datetime.strptime(cleanedProjectList['Project Enddate'][i], '%m/%d/%Y')
        print(projectName + ' ' + str(startDate) + ' ' + str(endDate))
        f.write(projectName + '\n')
        g = Github(access_token, retry = Retry (total = 15, status_forcelist = (500, 502, 504), backoff_factor = 0.3), timeout=6000, per_page=100)
        repo = g.get_repo(projectName)
        pr_list = repo.get_pulls(state = 'closed', sort = 'created')
        projectDF = extract_project_PRs(pr_list, startDate, endDate)
        projectDF.to_csv('PRs_dataset/' + projectName + '.csv', sep = ',', encoding = 'utf-8', index = True)
    except RateLimitExceededException as e:
        print('Rate limit exceeded')
        f.write(str(e.status))
        f.write('Rate limit exceeded')
        f.write('\n')
        time.sleep(3600)
        continue
    except BadCredentialsException as e:
        f.write(str(e.status))
        f.write('Bad credentials exception')
        f.write('\n')
        break
    except UnknownObjectException as e:
        f.write(str(e.status))
        f.write('Unknown object exception')
        f.write('\n')
        break
    except GithubException as e:
        f.write(str(e.status))
        f.write('General exception')
        f.write('\n')
        break
    except requests.exceptions.ConnectionError as e:
        f.write('Retries limit exceeded')
        f.write(str(e))
        f.write('\n')
        time.sleep(10)
        continue
    except requests.exceptions.Timeout as e:
        f.write(str(e))
        f.write('Time out exception')
        f.write('\n')
        time.sleep(10)
        continue
    except:
        f.write('exception')
        continue
