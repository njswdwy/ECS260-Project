import pandas as pd

cleanedProjectList = pd.read_csv('cleaned_project_w_frequncy.csv')

cleanedProjectList = cleanedProjectList.drop('Comment Length', 1)
cleanedProjectList = cleanedProjectList.drop('average_pr_comments_count', 1)
cleanedProjectList = cleanedProjectList.drop('average_pr_review_coments_count', 1)
cleanedProjectList = cleanedProjectList.drop('Unnamed: 0', 1)
cleanedProjectList = cleanedProjectList.drop('Unnamed: 0.1', 1)
cleanedProjectList = cleanedProjectList.drop('merged_average_pr_review_coments_count', 1)
cleanedProjectList = cleanedProjectList.drop('merged_average_pr_comments_count', 1)

print(cleanedProjectList.columns.tolist())


cleanedProjectList = cleanedProjectList[['Project Full Name', 'Project Status', 'Project Startdate', 'Project Enddate', 'PR Number', 'Merged PR Number', 'First PR Created Time', 'Merge Frequency', 'Issue Comment Number', 'Review Comment Number', 'Commits number', 'Stars', 'Forks', 'size', 'contributor', 'average_additions', 'average_deletions', 'average_pr_changed_files', 'average_pr_commits_count', 'average_total_comments', 'merged_average_additions', 'merged_average_deletions', 'merged_average_pr_changed_files', 'merged_average_pr_commits_count', 'merged_average_total_comments']]

for i in range(0, len(cleanedProjectList)):
    print(cleanedProjectList['average_additions'][i])
    cleanedProjectList['Issue Comment Number'][i] = cleanedProjectList['Issue Comment Number'][i] + cleanedProjectList['Review Comment Number'][i]
    if cleanedProjectList['average_additions'][i] == 0:
        cleanedProjectList = cleanedProjectList.drop(i)

cleanedProjectList = cleanedProjectList.drop('Review Comment Number', 1)
cleanedProjectList = cleanedProjectList.reset_index(drop=True)




cleanedProjectList.to_csv('Filtered_Final_Project_List.csv', sep = ',', encoding = 'utf-8', index = True)

