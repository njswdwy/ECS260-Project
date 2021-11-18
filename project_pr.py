import  csv
import os
file1 = open('cleaned_project_list.csv')

f1_csv = csv.reader(file1)

res = []
for row in f1_csv:
    res.append(row)

path = "./PRs_dataset/apache/"

all_file_name = os.listdir(path)

print(all_file_name) 

# 115

new_res = []

header1 = ['average_additions','average_deletions','average_pr_changed_files','average_pr_commits_count','average_pr_comments_count','average_pr_review_coments_count','average_total_comments','merged_average_additions','merged_average_deletions','merged_average_pr_changed_files','merged_average_pr_commits_count','merged_average_pr_comments_count','merged_average_pr_review_coments_count','merged_average_total_comments']
new_header = res[0]+header1

new_res.append(new_header)

for item in res[1:]:
    filefold = item[1].split('/')
    filename = filefold[1]+'.csv'
    if filename in all_file_name:
        temp_file = open(path+filename)
        temp_file_csv = csv.reader(temp_file)
        count = 0
        total_additions = 0
        total_deletions = 0
        total_pr_changed_files = 0
        total_pr_commits_count = 0
        total_pr_comments_count = 0
        total_pr_review_coments_count = 0

        merged_count = 0
        merged_total_additions = 0
        merged_total_deletions = 0
        merged_total_pr_changed_files = 0
        merged_total_pr_commits_count = 0
        merged_total_pr_comments_count = 0
        merged_total_pr_review_coments_count = 0


        average_additions = 0
        average_deletions = 0
        average_pr_changed_files  = 0
        average_pr_commits_count = 0
        average_pr_comments_count  = 0
        average_pr_review_coments_count = 0

        merged_average_additions = 0
        merged_average_deletions = 0
        merged_average_pr_changed_files = 0
        merged_average_pr_commits_count = 0
        merged_average_pr_comments_count = 0
        merged_average_pr_review_coments_count = 0
        merged_average_total_comments = 0

        for row in temp_file_csv:
            count+=1
            if count == 1:
                continue
            additions = float(row[4])
            deletions = float(row[5])
            pr_changed_files = float(row[6])
            pr_commits_count = float(row[7])
            pr_comments_count = float(row[8])
            pr_review_comments_count  = float(row[9])
            if_merged = float(row[14])

            total_additions+=additions
            total_deletions+=deletions
            total_pr_changed_files+=pr_changed_files
            total_pr_commits_count+=pr_commits_count
            total_pr_comments_count+=pr_comments_count
            total_pr_review_coments_count+=pr_review_comments_count

            if if_merged>0.5:
                merged_count+=1
                merged_total_additions+=additions
                merged_total_deletions+=deletions
                merged_total_pr_changed_files+=pr_changed_files
                merged_total_pr_commits_count+=pr_commits_count
                merged_total_pr_comments_count+=pr_comments_count
                merged_total_pr_review_coments_count+=pr_comments_count

        if count > 1:
            average_additions = total_additions/(count-1)
            average_deletions = total_deletions/(count-1)
            average_pr_changed_files = total_pr_changed_files/(count-1)
            average_pr_commits_count = total_pr_commits_count/(count-1)
            average_pr_comments_count = total_pr_comments_count/(count-1)
            average_pr_review_coments_count = total_pr_review_coments_count/(count-1)
            average_total_comments = average_pr_comments_count+average_pr_review_coments_count

        if merged_count>0:
            merged_average_additions = merged_total_additions/merged_count
            merged_average_deletions = merged_total_deletions/merged_count
            merged_average_pr_changed_files = merged_total_pr_changed_files/merged_count
            merged_average_pr_commits_count = merged_total_pr_commits_count/merged_count
            merged_average_pr_comments_count = merged_total_pr_comments_count/merged_count
            merged_average_pr_review_coments_count = merged_total_pr_review_coments_count/merged_count
            merged_average_total_comments = merged_average_pr_comments_count+merged_average_pr_review_coments_count

        new_temp_list = [average_additions,average_deletions,average_pr_changed_files,average_pr_commits_count,average_pr_comments_count,average_pr_review_coments_count,average_total_comments]
        new_temp_list.append(merged_average_additions)
        new_temp_list.append(merged_average_deletions)
        new_temp_list.append(merged_average_pr_changed_files)
        new_temp_list.append(merged_average_pr_commits_count)
        new_temp_list.append(merged_average_pr_comments_count)
        new_temp_list.append(merged_average_pr_review_coments_count)
        new_temp_list.append(merged_average_total_comments)

        real_new_temp = item+new_temp_list
        new_res.append(real_new_temp)


final_file = "cleaned_project_w_pr.csv"

final_my_file = open(final_file,'w')

f_csv_2 = csv.writer(final_my_file)

f_csv_2.writerows(new_res)


    
