import os
import argparse

from pathlib import Path
from itertools import islice

space =  '    '
branch = '│   '
tee =    '├── '
last =   '└── '

def tree(input_dir_path: Path, level: int=-1, limit_to_directories: bool=False, length_limit: int=1000):
    """Given a directory Path object print a visual tree structure"""
    
    dir_path = Path(input_dir_path) # accept string coerceable to Path
    
    print(f"dir_path: {dir_path}\n")
    
    files = 0
    directories = 0
    
    def inner(dir_path: Path, prefix: str='', level=-1):
        nonlocal files, directories
        
        if not level: 
            return # 0, stop iterating
        
        if limit_to_directories:
            #contents = [d for d in dir_path.iterdir() if d.is_dir()]
            #cannot use the above expression with external drives because of permissions issues
            contents = []
            for d in dir_path.iterdir():
                if "$RECYCLE.BIN" in str(d):
                    pass
                elif "System Volume Information" in str(d):
                    pass
                elif d.is_dir():
                    contents.append(d)

            #to get the right numbers for the files inside of each sub directory
            #count the files inside each then add that to the items to be zipped
            dir_file_counts = []
            for d in contents:
                
                num_files = [f for f in d.iterdir() if f.is_file()]
                dir_file_counts.append(len(num_files))
                
        else: 
            contents = list(dir_path.iterdir())
            
        pointers = [tee] * (len(contents) - 1) + [last]
        
        for pointer, path, file_count in zip(pointers, contents, dir_file_counts):
            
            if path.is_dir():
                yield prefix + pointer + path.name + f" (files: {file_count})"
                
                directories += 1
                
                extension = branch if pointer == tee else space 
                
                yield from inner(path, prefix=prefix+extension, level=level-1)
                
            elif not limit_to_directories:
                
                yield prefix + pointer + path.name
                
                files += 1
                       
    num_files = len([f for f in dir_path.iterdir() if f.is_file()])
    
    if dir_path.name:
        print(dir_path.name + f" (files: {num_files})")
        with open('dir_list.txt', mode='w', encoding="utf-8") as f:
            f.writelines(input_dir_path + f" (files: {num_files})\n")
            f.close()
    else:
        print(input_dir_path + f" (files: {num_files})")
        with open('dir_list.txt', mode='w', encoding="utf-8") as f:
            f.writelines(input_dir_path + f" (files: {num_files})\n")
            f.close()
    
    iterator = inner(dir_path, level=level)
    
    #print to file
    
    for line in iterator:
        with open('dir_list.txt', mode='a', encoding="utf-8") as f:
            f.writelines(line + "\n")
    
    f.close()

    # for line in islice(iterator, length_limit):
    #     print(line)
        
    # if next(iterator, None):
    #     #if we have 
    #     print(f'... length_limit, {length_limit}, reached, counted:')
        
    print(f'\n{directories} directories' + (f', {files} files' if files else ''))


def assign_arguments():

    parser = argparse.ArgumentParser(description="awn/awnless training script using either vgg16 or resnet")
    parser.add_argument('--dir', type=str, required=True)
    parser.add_argument('--length_limit', type=int, required=False)

    return parser.parse_args()

if __name__ == "__main__":

	args = assign_arguments()

	print(f"running... on {args.dir}\n\n")

	tree(args.dir, limit_to_directories=True)
