#!/usr/bin/env python3

# I wrote this on an airplane in 25 minutes, don't judge me =)
#
# TODO: jinja2 templates?
# TODO: tag names are links to the index for that tag?

import os
import datetime
from dateutil.parser import parse as dateutilparse

cur_dir = os.getcwd()

index_file = 'README.md'
readme_src_file = 'README_src.md'
end_sigil = '===='
dir_ignore_list = [
    '.git',
]

file_ignore_list = [
    index_file,
    readme_src_file,
    'generate-index.py',
]

known_md = [
    'Title',
    'Date',
]

# walk gives an iterator which returns each element as:
# ('/some/path/string', ['list_of_dirs'], ['list_of_files'])

# find blogs:
blogs = []
for e in os.walk(cur_dir):
    found_skip = False
    for skip in dir_ignore_list:
        if e[0].count(skip) > 0:
            found_skip = True
    if found_skip:
        continue

    print("Scanning path {}".format(e[0]))
    for f in e[2]:
        found_skip = False
        for skip in file_ignore_list:
            if f.count(skip) > 0:
                found_skip = True
        if found_skip:
            continue

        print("Found file {}".format(f))

        metadata = {}
        metadata["timestamp"] = 0
        with open(os.path.join(e[0], f), 'r') as fd:
            metadata['relpath'] = os.path.relpath(os.path.join(e[0], f), cur_dir)
            for line in reversed(fd.readlines()):
                if line.count(end_sigil) > 0:
                    break
                if line.count(':') == 0:
                    continue
                key, content = line.split(':', 1)
                if key == 'Tags':
                    metadata[key] = [t.strip() for t in content.split(',')]
                elif key in known_md:
                    metadata[key] = content.strip()
            if "Date" in metadata.keys():
                ts = dateutilparse(metadata["Date"]).timestamp()
                print("Parsed Date: {}".format(ts))
                metadata["timestamp"] = ts
        blogs.append(metadata)


def tags_to_s(tags):
    if not tags:
        tags = ['untagged']
    return "".join(["'", "', '".join(tags), "'"])


# https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
def flatten_list(l):
    return [item for sublist in l for item in sublist]


with open(os.path.join(cur_dir, index_file), 'w') as fd:
    # first write out title
    fd.write("# Carl Myers' Blog\n")
    fd.write("## Index generated on {}\n".format(datetime.datetime.now()))
    fd.write("\n")

    # next write out the readme src file
    with open(os.path.join(cur_dir, readme_src_file), 'r') as sfd:
        for line in sfd.readlines():
            fd.write(line)

    fd.write("\n")

    fd.write("# Post Index\n")
    fd.write("\n")

    fd.write("## All Blog Posts\n")
    fd.write("| Date | Title | Tags |\n")
    fd.write("| ---- | ----- | ---- |\n")
    for b in reversed(sorted(blogs, key=lambda x: x["timestamp"])):
        fd.write("| {} | {} | {} |\n".format(b.get("Title", "Unknown"), b.get("Date", "Unknown"), tags_to_s(b.get("Tags"))))

    fd.write("\n\n")
    for t in sorted({*flatten_list([x.get("Tags", ['untagged']) for x in blogs])}):
        fd.write("## Posts Tagged '{}'\n\n".format(t))
        fd.write("| Date | Title | Tags |\n")
        fd.write("| ---- | ----- | ---- |\n")
        for b in reversed(sorted(blogs, key=lambda x: x["timestamp"])):
            if t in b.get("Tags", ['untagged']):
                fd.write("| {} | {} | {} |\n".format(b.get("Title", "Unknown"), b.get("Date", "Unknown"), tags_to_s(b.get("Tags"))))
        fd.write("\n\n")
