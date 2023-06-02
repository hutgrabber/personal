import re
file_path = '/Users/sparsh/Projects/secret-code-stash/personal-git/thm/mr_robot/'

words = open(file_path + 'words.txt', 'r').readlines()
formatted = []
for i in words:
    formatted.append(re.sub('\n', '', i))

remove_dups = list(dict.fromkeys(formatted))
print(remove_dups)

with open(file_path + "new.txt", "w") as output:
    output.write(str(remove_dups))