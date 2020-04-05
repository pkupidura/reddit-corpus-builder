import math
from dataclasses import dataclass
import random
from typing import List
from os import listdir, path

MIN_WORDS_COUNT = 5

WORD_PERCENTAGE_PER_FILE = 0.43


@dataclass
class Comment:
    content: str
    word_count: int


def count_words(s: str) -> int:
    return len(s.strip().split(" "))


def read_comments(file_path: str) -> List[Comment]:
    with open(file_path, 'r') as f:
        lines = f.readlines()
        comments = [line[7:].strip() for line in lines if len(line) > 0]
        return [Comment(content=comment, word_count=count_words(comment)) for comment in comments if
                not comment.startswith("[removed]")]


def get_comment_files(corpus_path: str) -> List[str]:
    return [f for f in listdir(corpus_path) if path.isfile(path.join(corpus_path, f)) and f.startswith("comments")]


def pick_comments_from_file(file_path: str) -> List[Comment]:
    comments = [c for c in read_comments(file_path) if c.word_count > MIN_WORDS_COUNT]
    file_word_count = sum([c.word_count for c in comments])
    desired_word_count = math.ceil(WORD_PERCENTAGE_PER_FILE * file_word_count)

    random.shuffle(comments)

    word_count_acc = 0
    picked_comments = []

    for c in comments:
        if word_count_acc + c.word_count >= desired_word_count:
            continue
        else:
            picked_comments.append(c)
            word_count_acc += c.word_count

    return picked_comments


def write_comments_to_file(file_path: str, comments: List[Comment]):
    with open(file_path, 'w') as f:
        for c in comments:
            f.write(c.content)
            f.write("\n")


def process_comments_file(file_name: str, input_corpus_path: str, output_corpus_path: str) -> int:
    picked_comments = pick_comments_from_file(path.join(input_corpus_path, file_name))
    write_comments_to_file(path.join(output_corpus_path, file_name), picked_comments)
    return sum([c.word_count for c in picked_comments])


def pick_comments(input_corpus_path: str, output_corpus_path: str) -> int:
    output_corpus_size = 0

    for file in get_comment_files(input_corpus_path):
        try:
            output_corpus_size += process_comments_file(file, input_corpus_path, output_corpus_path)
        except Exception as e:
            print(f"Failed to process {file}")
            print(e)

    return output_corpus_size

