import sys 

try: 
    if len(sys.argv < 2):
        print(f'Error: missing filename argument')
        sys.exit(1)
        
    with open(sys.argv[1]) as f:
        for line in f:
            split_line = line.split("#")[0]
            stripped_split_line = split_line.strip()
        
        if stripped_split_line != '':
            command = int(stripped_split_line, 2)
            print(command)

except FileNotFoundError:
    print(f'Your file {sys.argv[1]} could not be found in {sys.argv[0]}')

#print(sys.argv)