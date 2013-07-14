import collections
def formatData(fileName):
    saveFile = open('format_'+fileName,'w')
    formatFile = open(fileName,'r')
    line = formatFile.readline()
    string = ''
    count = 0
    while line != None and len(line) > 0:
        friendship = line.split(':')
        userId = friendship[0]
        string += userId+'\t'
        follows = friendship[1].split('\t')
        followers = '\n'
        if len(follows) == 4:
            followers = follows[3]
        string += followers
        line = formatFile.readline()        
        count += 1
        if count % 1000 == 0:
            print count
    saveFile.write(string)
    saveFile.flush()
    formatFile.close()
    saveFile.close()
        

    
def userRank(fileName,k=0.8):
    userNum = 1000
    initWeight = 1.0
    P = collections.defaultdict(lambda:1.0)
    userFile = open(fileName,'r')
    
    for i in range(20):
        userFile.seek(0)
        line = userFile.readline()
        while line != None and len(line) > 0:
            friendship = line.split("\t")
            user = friendship[0]
            user = user.replace('\n','')
            followers = friendship[1].split(' ')
            if '' in followers or '\n' in followers:
                followers.pop()
            sumValue = 0.0
            for follower in followers:
                sumValue += P[follower]
            line = userFile.readline()
            P[user] = k * sumValue/(1+len(followers))+(1-k) * 1
    saveFile = open('pagerank.txt','w')
    for k,v in P.items():
        saveFile.write(k+'\t'+str(v)+"\n")
    saveFile.flush()
    saveFile.close()
if __name__ == "__main__":
    #formatData('friendships.txt')
    userRank('format_friendships.txt')
            
    
