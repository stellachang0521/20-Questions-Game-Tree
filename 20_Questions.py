#
# Name: Stella Chang
#

#
# The following two trees are useful for testing.
#
smallTree = \
    ("Is it bigger than a breadbox?",
        ("an elephant", None, None),
        ("a mouse", None, None))
mediumTree = \
    ("Is it bigger than a breadbox?",
        ("Is it gray?",
            ("an elephant", None, None),
            ("a tiger", None, None)),
        ("a mouse", None, None))

def main():
    '''
    Runs the main program that implements the 20 Questions Game.
    '''
    print('Welcome to 20 Questions!')
    load = yes('Would you like to load a tree from a file?')
    if load == True:
        filename = input("What's the name of the file?")
        treeFile = open(filename, 'r')
        tree = loadTree(treeFile)
        treeFile.close()
    elif load == False:
        tree = smallTree
        
    replay = True
    while replay:
        tree = play(tree)
        replay = yes('Would you like to play again?')
        
    save = yes('Would you like to save this tree for later?')
    if save == True:
        filesave = input('Please enter a file name: ')
        treeFile = open(filesave, 'w')
        saveTree(tree, treeFile)
        treeFile.close()
        print('Thank you! The file has been saved.')
        print('Bye!')
    elif save == False:
        print('Bye!')
        
def simplePlay(tree):
    '''
    Plays the game once by using the tree to guide its questions. 
    Returns True if the correct answer is guessed.
    '''
    text, left, right = tree
    if left is None and right is None: # is a leaf
        boolean = yes(f"Is it {text}?")
        if boolean == True:
            print('I got it!')
            return True
        elif boolean == False:
            print("Darn it! I really don't know!")
            return False
    else: # is a node
        boolean = yes(text)
        if boolean == True:
            simplePlay(left)
        elif boolean == False:
            simplePlay(right)

def play(tree):
    '''
    Plays the game once by using the tree to guide its questions. 
    Returns a new tree that is the result of playing the game on the original tree and learning from the answers.
    '''
    text, left, right = tree
    if left is None and right is None: # is a leaf
        boolean = yes(f"Is it {text}?")
        if boolean == True:
            print('I got it!')
            return tree
        elif boolean == False:
            item = input('What was it?')
            question = input(f"What's the question that distinguishes between {item} and {text}?")
            answer = yes(f"And what's the answer for {item}?")
            if answer == True:
                newNode = (question, (item, None, None), (text, None, None))
                return newNode
            elif answer == False:
                newNode = (question, (text, None, None), (item, None, None))
                return newNode
    else: # is a node
        leftTree = left
        rightTree = right
        boolean = yes(text)
        if boolean == True:
            subTree = play(left)
            return (text, subTree, rightTree)
        elif boolean == False:
            subTree = play(right)
            return (text, leftTree, subTree)

def isLeaf(tree):
    '''
    Returns True if the tree is a leaf and False if it is an internal node.
    '''
    text, left, right = tree
    if left is None and right is None:
        return True
    else:
        return False
        
def yes(prompt):
    boolean = input(prompt)
    if boolean.lower() == 'yes' or boolean.lower() == 'y' or boolean.lower() == 'yeah' or boolean.lower() == 'yup' or boolean.lower() == 'sure':
        return True
    elif boolean.lower() == 'no' or boolean.lower() == 'n' or boolean.lower() == 'nah' or boolean.lower() == 'nope' or boolean.lower() == 'wrong':
        return False
        
def playLeaf():
    pass

# Support functions for the 20 Questions problem
def printTree(tree, prefix = '', bend = '', answer = ''):
    '''
    Recursively prints a 20 Questions tree in a human-friendly form. 
       TREE is the tree (or subtree) to be printed.
       PREFIX holds characters to be prepended to each printed line.
       BEND is a character string used to print the "corner" of a tree branch.
       ANSWER is a string giving "Yes" or "No" for the current branch.
    '''
    text, left, right = tree
    if left is None and right is None:
        print(f'{prefix}{bend}{answer}It is {text}')
    else:
        print(f'{prefix}{bend}{answer}{text}')
        if bend == '+-':
            prefix = prefix + '| '
        elif bend == '`-':
            prefix = prefix + '  '
        printTree(left, prefix, '+-', "Yes: ")
        printTree(right, prefix, '`-', "No:  ")

#treeFile = open('tree.txt', 'w')
def saveTree(tree, treeFile):
    '''
    Saves given tree in specified file.
    '''
    text, left, right = tree
    if left is None and right is None: # is a leaf
        print('Leaf', file = treeFile)
        print(text, file = treeFile)
        
    else: # is a node
        print('Internal Node', file = treeFile)
        print(text, file = treeFile)
        saveTree(left, treeFile)
        saveTree(right, treeFile)
#treeFile.close()

#treeFile = open('tree.txt', 'r')
def loadTree(treeFile):
    '''
    Loads tree from specified file.
    '''
    inputList = treeFile.readlines()  # Generates a list with lines from treeFile

    # Removes the \n symbols
    cleanList = [x.strip("\n") for x in inputList]
    groupList = []
    
    for i in range(0, len(cleanList), 2):
        groupList.append((cleanList[i], cleanList[i+1]))
        
    for i in range(len(groupList)):
        if groupList[i][0] == 'Leaf':
            groupList[i] = (groupList[i][1], None, None)
    
    status = True
    while status:
        popList = []
        for i in range(len(groupList)-1, -1, -1):
            if len(groupList[i]) == 2 and groupList[i][0] == 'Internal Node':
                groupList[i] = (groupList[i][1], groupList[i+1], groupList[i+2])
                popList.append(i+1)
                popList.append(i+2)
                break
    
        for i in reversed(popList):
            groupList.pop(i)
            
        counter = 0
        for i in range(len(groupList)):
            if groupList[i][0] == 'Internal Node':
                counter += 1
        
        if counter == 0:
            status = False
            
    loaded = groupList[0]
    
    return loaded
#treeFile.close()

# "magic sequence"
if __name__ == '__main__':
    main()
