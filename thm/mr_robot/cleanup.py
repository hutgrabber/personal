words = open(file_path + 'words.txt', 'r').readlines()
formatted = []
for i in words:
    formatted.append(re.sub('\n', '', i))