import subprocess
import os, sys
import argparse

def produce_idb32_file(args):
    cmd = [args['ida32'], "-B", args["input"]]
    res = subprocess.call(cmd, stdin=None, stdout=None, stderr=None, shell=False)
    if res == 0:
        args["idb"] = filepath.replace(filename, )
        return True
    return False

def produce_idb64_file(args):
    cmd = [args['ida64'], "-B", args["input"]]
    res = subprocess.call(cmd, stdin=None, stdout=None, stderr=None, shell=False)
    if res == 0:
        return True
    return False
    
def produce_idb_file(args):
    filepath = args["input"]
    filename = os.path.basename(filepath)
    idb32_filename = filepath.replace(filename, filename.split(".")[0] + ".idb")
    idb64_filename = filepath.replace(filename, filename.split(".")[0] + ".i64")
    if args['overwrite'] == False:
        if os.path.exists(idb32_filename):
            args["idb"] = idb32_filename
            return True
        if os.path.exists(idb64_filename):
            args["idb"] = idb64_filename
            return True
    if produce_idb32_file(args):
        if os.path.exists(idb32_filename):
            args["idb"] = idb32_filename
            return True
    if produce_idb64_file(args):
        if os.path.exists(idb64_filename):
            args["idb"] = idb64_filename
            return True
    return False

def run_ida_script(args):
    ida = ""
    idb_filename = args["idb"]
    if idb_filename.endswith(".idb"):
        ida = args['ida32']
    elif idb_filename.endswith(".i64"):
        ida = args['ida64']
    else:
        return -1
    ida_script_path = args['script']
    args = [ida, "-A", '-S"%s"' % ida_script_path, idb_filename ]
    res = subprocess.call(args, stdin=None, stdout=None, stderr=None)
    return res
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Morph multiple files from dir')
    parser.add_argument('-ida_dir', type=str, default='C:\\Program Files (x86)\\IDA 6.8', help='path to directory with IDA 6.8 (by default C:\\Program Files (x86)\\IDA 6.8\\)')
    parser.add_argument('-input', type=str, help='path to input executable file')
    parser.add_argument('-script', type=str, help='path to IDA python script')
    parser.add_argument('-overwrite', action='store_true')
    args = vars(parser.parse_args())
    assert os.path.exists(args['ida_dir']), "IDA directory not found (%s)" % args['ida_dir']
    assert os.path.exists(args['input']), 'input executable file not found (%s)' % args['script']
    assert os.path.exists(args['script']), 'IDA script not found (%s)' % args['script']
    args['ida32'] = os.path.join(args['ida_dir'], "idaq.exe")
    args['ida64'] = os.path.join(args['ida_dir'], "idaq64.exe")
    assert os.path.exists(args['ida32']), "IDA32 not found"
    assert os.path.exists(args['ida64']), "IDA64 not found"
    
    if produce_idb_file(args):
        if run_ida_script(args):
            pass
