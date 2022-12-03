#!/home/mdavis/anaconda3/bin/python
"""Walks through a data structure, finds spectro2.out and runs rsummarize
in each dir"""
import os
from os.path import join
import random
import subprocess

# import sys




def main():
    """Locate spectro2.out files in subdirs,
    runs rsummarize on each then prints a summary of remaining work to be done
    spectro2.out files are assumed to all be located at the same level of depth
    for summary.txt to be accurate"""
    # TODO allow choosing input directory
    completed, incompleted = check_completed()
    rsum_options = ["json", "csv", "tex"]

    # form individual tables
    for spec_dir in completed:
        rsum_outputs_sep = run_rsummarize([spec_dir], rsum_options)
        write_rsums(spec_dir, rsum_outputs_sep)

    write_summary()

    # form composite tables
    rsum_outputs = run_rsummarize(completed, rsum_options)
    write_rsums(".", rsum_outputs, "combined")

    #TODO
    panda_tables = parse_into_pandas(rsum_outputs)
    pandas_tables = insert_experiment(panda_tables)
    fixed_panda_tables = fix_pandas_tables(completed, panda_tables)
    write_pandas(fixed_pandas_tables)

def parse_into_pandas(rsum_outputs):
    """TODO read either csv or json into a pandas dataframe"""
    pass

def insert_experiment(pandas_tables):
    """TODO allow inserting experimental values from a plaintext file?"""
    pass

def fix_pandas_tables(dir_list, panda_tables):
    """TODO fix headers with proper names of molecules, format for LaTex etc"""
    pass

def write_pandas(fixed_pandas_tables):
    """TODO write pandas dataframe to organized file(s)"""
    pass



def write_summary(directory: str = "."):
    """I should make this reusable and just operate on the filesystem...
    It's redundant computational cost but that doesn't
    matter compared to the convenience of reusing this fn
    """

    def get_motivational():
        """Print friendly message"""
        # TODO add more
        motivationals = [
            "Do your best!\n",
            "Keep going!\n",
            "Good progress!\n",
            "Get to work!\n",
            "Don't stop now!\n",
            "You can do it!\n",
            "Work hard, play hard :)\n",
            "Courage is the magic that turns dreams into reality!\n",
            "Little rough, don't ya think?\n",
            "Eyes on the prize!\n",
            "One step at a time!\n",
        ]
        return random.choice(motivationals)

    completed, incompleted = check_completed(directory)
    filename = join(directory, "summary.txt")
    completed_str = ""
    incompleted_str = ""
    for path in completed:
        completed_str += f"{path} completed\n"
    for path in incompleted:
        incompleted_str += f"{path} incompleted\n"
    with open(filename, "w") as file:
        file.write("--COMPLETED QFFs--\n")
        file.write(completed_str)
        file.write("--INCOMPLETED QFFs--\n")
        file.write(get_motivational())
        file.write(incompleted_str)


def write_rsums(spec_dir: str, rsum_outputs: dict, header: str = "spectro2"):
    """Runs rustsummarize and outputs files.
    Actually I guess I should decompose this function"""
    for flag, output in rsum_outputs.items():
        filename = header + "." + flag
        filepath = join(spec_dir, filename)
        with open(filepath, "w") as file:
            file.write(output)


def run_rsummarize(completed_dirs: list, options: list = ["json"]):
    """Runs rsummarize with all files grouped together into a giant data table.
    Run at toplevel of a species directory

    Since this is almost exactly the same as below, I should probably delete the below one and just run this with a single input as a list
    """
    rsum_outputs = {}
    outfiles = [join(completed_dir, "spectro2.out") for completed_dir in completed_dirs]

    for opt in options:
        out = subprocess.run(
            ["rsummarize", f"--{opt}"] + outfiles, capture_output=True, check=False
        ).stdout.decode()
        rsum_outputs[opt] = out

    opt = "sum"
    out = subprocess.run(
        ["rsummarize"] + outfiles, capture_output=True, check=False
    ).stdout.decode()
    rsum_outputs[opt] = out

    return rsum_outputs


def check_completed(target_dir: str = "."):
    """Check if spectro files are in current directory, return completed and
    incompleted as lists"""

    def get_depth(path):
        """helper function that was probably dumb"""
        depth = len(path.split("/"))
        return depth

    completed = []
    incompleted = []
    for root, dirs, files in os.walk(target_dir):
        if "spectro2.out" in files:
            completed.append(root)
        else:
            incompleted.append(root)
    max_depth = max([get_depth(path) for path in incompleted])
    incompleted = [path for path in incompleted if get_depth(path) == max_depth]
    return completed, incompleted


if __name__ == "__main__":
    main()  # I think this is how you do this?
