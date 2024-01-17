import os

top_words = 0
top_lines = 0

def analyze_md_files(folder_path):
    global top_words, top_lines
    log = []

    # Check if the path exists
    if not os.path.exists(folder_path):
        print("Folder path does not exist.")
        return

    # Iterate through files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    num_lines = len(lines)
                    num_words = sum(len(line.split()) for line in lines)
                    log.append([file, num_words, num_lines])

                    if (top_words == None or top_words < num_words):
                        top_words = num_words

                    if (top_lines == None or top_lines < num_lines):
                        top_lines = num_lines

    return log

folder_path = './src/content/blog/'
logs = analyze_md_files(folder_path)
result = sorted(logs, key=lambda x: x[1], reverse=True)

for element in result:
    print(f"{element[0]}")
    print(f"{round((element[1] / top_words) * 100)} % \t {element[1]} words \t {round((element[2] / top_lines) * 100)} % \t {element[2]} lines\n")


