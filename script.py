import datetime

from github import Github, RateLimitExceededException, BadCredentialsException, BadAttributeException, \
    GithubException, UnknownObjectException, BadUserAgentException
import pandas as pd
import requests
import datetime
import time
from urllib3 import Retry

access_token = "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"
projectList = pd.read_csv("Cleaned_Project_List(1)(1).csv")
projectList['full Name'] = projectList['GitHub Link']
for i in range(len(projectList)):
    projectList['full Name'][i] = '/'.join(projectList['full Name'][i].split('/')[-2:])


f = open('log.txt','a')
f.write((str(datetime.datetime.now())))

#get pr data
def extract_project_PRs(pr_list):
    df_PRs = pd.DataFrame()

    merged_pr_count = 0
    for pr in pr_list:
            try:
                # print(g.rate_limiting)
                print(f'Extracting data from PR # {pr.number}')
                f.write('Extracting data from PR # {number}\n'.format(number = pr.number))
                # Review Comments on the Pull requests
                normal_comments = []
                review_comments = []
                comments = []
                commit_ = []
                if pr.is_merged():
                    merged_pr_count += 1
                # get normal conversation comments
                if pr.get_issue_comments().totalCount > 0:
                    for comment in pr.get_issue_comments():
                        cmt = {
                            'comment_id': comment.id,
                            'comment_body': comment.body,
                            'comment_created': comment.created_at,
                            'commenter': comment.user.login,
                            'type': comment.user.type
                        }
                        comment_cont = comment.body
                        normal_comments.append(cmt)
                        comments.append(comment_cont)

                # get review comments
                if pr.get_comments().totalCount > 0:
                    for comment in pr.get_comments():
                        cmt = {
                            'comment_id': comment.id,
                            'comment_body': comment.body,
                            'comment_created': comment.created_at,
                            'commenter': comment.user.login,
                            'type': comment.user.type
                        }
                        review_comments.append(cmt)

                # get commits
                if pr.get_commits().totalCount > 0:
                    for commit in pr.get_commits():
                        commit_content = {
                            'committer': commit.committer,
                            'commif_id': commit.sha,
                            'commit_time': commit.last_modified
                        }
                        commit_.append(commit_content)
                df_PRs = df_PRs.append({
                    'pr_id': pr.id,  # PRs features
                    'pr_title': pr.title,
                    # 'pr_body': pr.body,
                    'pr_number': pr.number,
                    'pr_url': pr.url,
                    # 'pr_html_url': pr.html_url,
                    'pr_state': pr.state,
                    'additions': pr.additions,
                    'deletions': pr.deletions,
                    'pr_changed_files': pr.changed_files,  # number of changed files
                    'pr_commits_count': pr.commits,  # number of commits
                    'pr_comments_count': pr.comments,
                    'pr_review_comments_count': pr.review_comments,
                    'pr_labels_count': len([l.name for l in pr.labels]),
                    'pr_assignees_count': len(pr.assignees),
                    'pr_labels': [l.name for l in pr.labels],
                    'pr_created_at': pr.created_at,  # when this pull request was created.
                    'pr_closed_at': pr.closed_at,  # when this pull request was closed.
                    #                         'pr_review_comments1': review_comments,
                    #                         'pr_review_comments2': pr.get_review_comments,
                    'contributor': pr.user.name,  # Contributor's information
                    'contributor_id': pr.user.id,
                    # 'contributor_email': pr.user.email,
                    # 'contributor_type': pr.user.type,
                    # 'contributor_public_repos': pr.user.public_repos,
                    # 'contributor_private_repos': pr.user.owned_private_repos,
                    # 'contributor_followings': pr.user.following,
                    # 'contributor_followers': pr.user.followers,
                    'is_merged': pr.is_merged(),
                    'pr_merged_at': pr.merged_at,
                    # this pull request was merged. If this pull request has not been merged then this attribute will be None.
                    #                         'requested_reviewers':pr.requests,
                    'pr_normal_comment': normal_comments,
                    'pr_review_comment': review_comments,
                    'pr_commit': commit_,
                    'comments_content': comments

                }, ignore_index=True)
            except RateLimitExceededException as e:
                f.write(str(e.status))
                f.write('Rate limit exceeded')
                f.write('\n')
                time.sleep(300)
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

    return (df_PRs,merged_pr_count)

# get projectList table
def extract_projects(projectList):

    df = pd.DataFrame()
    df['Project Full Name'] = projectList['full Name']
    df['Project Status'] = projectList['Project Status']
    df['Project Startdate'] = projectList['Project Startdate']
    df['Project Enddate'] = projectList['Project Enddate']
    df['PR Number'] = 0
    df['Merged PR Number'] = 0
    df['First PR Created Time'] = None
    df['Comment Length'] = 0
    df['Merge Frequency'] = 0
    df['Issue Comment Number'] = 0
    df['Review Comment Number'] = 0
    df['Commits number'] = 0
    df['Stars'] = 0
    df['Forks'] = 0
    df['size'] = 0
    df['contributor'] = 0
    # shape = df.shape


    for i in range(0, len(projectList)):
        print(str(i + 1) + ' ' + df['Project Full Name'][i])
        f.write(str(i + 1) + ' ' + df['Project Full Name'][i] + '\n')
        project_name = df['Project Full Name'][i]
        # project_name = 'apache/aries'
        try:
            g = Github(access_token, retry = Retry (total = 15, status_forcelist = (500, 502, 504), backoff_factor = 0.3), timeout=6000, per_page=100)
            repo = g.get_repo(project_name)
            pr_list = repo.get_pulls(state='closed',sort='created')
            pr_number = pr_list.totalCount
            df['PR Number'][i] = pr_number
            df['size'][i] = repo.size
            df['contributor'][i] = repo.get_contributors().totalCount

            # merged_pr_number =0

            # prs, merged_pr = extract_project_PRs(pr_list)
            # prs.to_csv('PRs_dataset/' + project_name + '.csv', sep=',', encoding='utf-8', index=True)

            if pr_number > 0:
                df['First PR Created Time'][i] = pr_list[0].created_at
            #     PRs_comment = repo.get_pulls_comments(sort='created').totalCount
            df['Review Comment Number'][i] = repo.get_pulls_review_comments(sort='created').totalCount
            df['Issue Comment Number'][i] = repo.get_issues_comments(sort='created').totalCount
            df['Commits number'][i] = repo.get_commits().totalCount
            df['Forks'][i] = repo.forks
            df['Stars'][i] = repo.get_stargazers().totalCount
            # df['Merged PR Number'][i] = merged_pr
            df['Merged PR Number'][i] = 0
            print('Complete')

        except RateLimitExceededException as e:
            f.write(str(e.status))

            f.write(' Rate limit exceeded\n')
            time.sleep(300)
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
        except requests.exceptions.Timeout as e:
            print(str(e))
            print('Timeout exception')
            time.sleep(10)
            continue
        except GithubException as e:

            f.write(str(e.status))
            f.write('GithubException')
            f.write('\n')
            continue
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
    return df


df = extract_projects(projectList)
df.to_csv('PRs_dataset/project_list.csv', sep=',', encoding='utf-8', index=True)






