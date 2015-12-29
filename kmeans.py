from random import randrange
import math
import pandas
import matplotlib
import matplotlib.pyplot as plt
import glob
import os
import time
os.chdir('C:/Users/user/Desktop/iPython/')

folders = [ item for item in glob.glob('*') if os.path.isdir(item) ]
print folders
#folders.remove('.ipynb_checkpoints')
folders = map(lambda x:int(x) , folders)
new_folder = int(sorted(folders)[len(folders)-1]) + 1

os.mkdir(str(new_folder))
os.chdir(str(new_folder) + '/')

files = [ item for item in glob.glob('*.jpg')]


for item in files :
  os.remove(item)

num_points = 60000

X = [ { 'x':randrange(1000) , 'y':randrange(1000) } for i in range(num_points) ]

for i in X:
  pass#print "%s %s" % (i['x'], i['y'])

K = 10

color = matplotlib.colors.cnames.keys()

centroid = [ X[randrange(len(X))] for i in range(K) ]

lastCoord = [ {'x':0,'y':0} for i in range(K) ]

count = 0

last_clust_avg = [ 0 for i in range(K) ]

content = '''
Report 
  Parameters
    K ''' + str(K) + '''
    Number of Points Used '''  + str(num_points) + '''
    Colors''' + ''.join([ '\n\t\t\tCluster ' + str(k+1) + '\t' + str(color[k]).capitalize() for k in range(len(color[:K])) ]) +  '''

'''

start = time.time()

while True :
  loop_start = time.time()
  for point in X:

    minDist = 10000000
    cluster = 0
    for i in range(K) :
      dist = math.sqrt((point['x'] - centroid[i]['x'])**2 + (point['y'] - centroid[i]['y'])**2)
      if dist < minDist :
        minDist = dist
        cluster = i
    point.update( { 'cluster':str(cluster)} )
  
  
  cluster_avg = [ 0 for i in range(K)]
  cluster_xsum = [ 0 for i in range(K)]
  cluster_ysum = [ 0 for i in range(K)]

  
  for i in X:
    for j in range(K) :
      if i['cluster'] == str(j):
        cluster_avg[j] += 1
        cluster_xsum[j] += i['x']
        cluster_ysum[j] += i['y']
  
  if count == 0 :
    pass
  else :
    #print  '' .join([ str(cluster_avg[x]) + '  ' + str(last_clust_avg[x]) for x in range(K-1)])
    print "Iteration Number " + str(count) + ' : ' + ''.join([ '\n\tCluster' + str(x+1) + ' - ' + str( float((cluster_avg[x] - last_clust_avg[x])) * 100  / last_clust_avg[x] )[:4]  + ' %   ' for x in range(K)  ])
    print '\n\tTime for Iteration\t'+str(time.time()-loop_start)+'\n'
    content += "\n\tIteration Number " + str(count) + ' : ' + ''.join([ '\n\t\tCluster' + str(x+1) + '\t' + str( float((cluster_avg[x] - last_clust_avg[x])) * 100  / last_clust_avg[x] )[:4]  + ' %   ' for x in range(K)  ])
    content += '\n\tTime for Iteration\t'+str(time.time()-loop_start)+'\n'

  for i in range(K) :
    cluster_xsum[i] = cluster_xsum[i] / cluster_avg[i]
    cluster_ysum[i] = cluster_ysum[i] / cluster_avg[i]
    centroid[i]['x'] = cluster_xsum[i]
    centroid[i]['y'] = cluster_ysum[i]
  


  fig = plt.figure()
  add = fig.add_subplot(111)
  for i in range(K) :
    points = [ {'x':point['x'] ,'y':point['y'] } for point in X if point['cluster'] == str(i) ]
    frame = pandas.DataFrame(points)
    add.scatter(frame.x,frame.y , label='Cluster ' + str(i+1) , s=75 , c=color[i])
  plt.legend()
  #plt.show()
  fig.set_size_inches(20,20)
  fig.savefig( str(count)  + '.jpg',dpi=100)

  
  for i in range(K) :
    last_clust_avg[i] = cluster_avg[i]

  completed = True
  for i in range(K) :
    if lastCoord[i]['x'] == cluster_xsum[i] and lastCoord[i]['y'] == cluster_ysum[i] :      
      pass
    else :      
      completed = False

  if completed :  
    print "ENDED!"
    content += '\nTotal elasped time\t' + str(time.time() - start)
    with open('report.txt','w') as f :
      f.write(content)
    break

  for i in range(K) :
    lastCoord[i]['x'] = cluster_xsum[i]
    lastCoord[i]['y'] = cluster_ysum[i]
  count += 1