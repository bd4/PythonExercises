import os
import os.path
import argparse
import re
import fnmatch
import io
import sys


parser = argparse.ArgumentParser()

parser.add_argument("path", help="path to search in", nargs='?', default="./")
parser.add_argument("-regex", help="use regular expression matching")
parser.add_argument("-name", help="name of file")
parser.add_argument("-type", help="type: be it a file or dir", choices='df')

results_found = False

def initialize_args(argslist = sys.argv[1:]):
    global args
    global parser
    args = parser.parse_args(argslist)
    
    return args

def do_search(provided_path, regex_pattern, name_to_match, type_ForD):
    outputFromSearch = io.StringIO()
    
    if regex_pattern:
        try:
            compiled_re = re.compile(regex_pattern)
        except re.error as ex:
            print("Illegal regex '%s': %s" % (regex_pattern, ex))
            exit(1)
    else:
        compiled_re = None
    
    if not os.path.isdir(provided_path):
        exit("That is not a valid directory")
    
    outputFromSearch = search_recursively(provided_path, compiled_re, name_to_match, type_ForD)
    return outputFromSearch


def process_asset(fileOrDir, fileType, fileTypeRequired, compiled_re, name_to_match, rootDir=""):
    
    global results_found
    abs_url = os.path.join(rootDir, fileOrDir)
    base_name = os.path.basename(fileOrDir)
    
    if fileTypeRequired and fileType != fileTypeRequired:
        return None
    if compiled_re is not None and not compiled_re.search(base_name):
        return None
    if name_to_match is not None and not fnmatch.fnmatch(base_name, name_to_match):
        return None
    
    results_found = True
    return abs_url


def search_recursively(provided_path, regex_pattern, name_to_match, type_ForD):
    
    search_results_output = io.StringIO()
    
    for root, dirs, files in os.walk(provided_path, topdown=True):    
        d_processed = process_asset(root, 'd', type_ForD, regex_pattern, name_to_match)
        if d_processed is not None:
            print(d_processed, file=search_results_output)
        
        for f in files:
            f_processed = process_asset(f, 'f', type_ForD, regex_pattern, name_to_match, root)
            if f_processed is not None:
                print(f_processed, file=search_results_output)
    
    return search_results_output


#execute the search
initArgs = initialize_args()
results = do_search(args.path, args.regex, args.name, args.type)
print(results.getvalue())
results.close()
if results_found is not True:
    print("Sorry, no results were found")