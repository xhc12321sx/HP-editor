import os
import re
from pydub import AudioSegment

def each_book(dir, rst_dir):
    ls = os.listdir(dir)
    ls.sort()
    i = 0
    p = 0
    while i < (len(ls)):
        chapter = find_chapter(ls[i])
        p = i + 1
        while chapter != None and p < len(ls) and chapter == find_chapter(ls[p]):
            p += 1
        each_chapter(dir, ls[i:p], rst_dir)
        i = p
    pass

def each_chapter(dir, ls, rst_dir):
    name = re.sub(r"-[1-9][0-9]?", "", ls[0])
    print(name)
    ls.sort(key=find_part)
    rst = AudioSegment.from_mp3(dir+"/"+ls[0])
    for i in range(1, len(ls)):
        rst += AudioSegment.from_mp3(dir+"/"+ls[i])
    rst.export(rst_dir +"/"+name, format="mp3")
    pass

part_pattern = re.compile(r"-[1-9][0-9]?")
double_dig_pattern = re.compile(r"[1-9][0-9]?")
def find_part(name):
    match = re.search(part_pattern, name)
    if match != None:
        match = re.search(double_dig_pattern, match.group())
        return int(match.group())
    else:
        return None
    pass

chapter_pattern = re.compile(r"Chapter [1-9][0-9]?")
def find_chapter(name):
    match = re.search(chapter_pattern, name)
    if match != None:
        match = re.search(double_dig_pattern, match.group())
        return int(match.group())
    else:
        return None

if __name__ == "__main__":
    booklist = os.listdir("./HP")
    booklist.sort()
    for book in booklist:
        if not os.path.exists("./rst/" + book):
            os.mkdir("./rst/" + book)
        each_book(os.getcwd() + "/HP/" + book, "./rst/" + book)
    pass