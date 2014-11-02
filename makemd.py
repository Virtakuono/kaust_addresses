#!/usr/bin/python

f = open('./map.osm')
lines = f.readlines()
f.close()

houseNums = []
nodeSets = []

print('Identifying corners of houses...')
for lineInd in range(len(lines)):
        compString = '<tag k=\'addr:housenumber\' v=\''
        if compString in lines[lineInd]:
                houseNum = lines[lineInd].find('v=\'')
                houseNum = lines[lineInd][houseNum+3:]
                houseNum = houseNum[:houseNum.find('\'')]
                print('Found house number %s'%(houseNum,))
                houseNums.append(houseNum)
                shift = -2
                nodeSet = []
                while '<nd ref=\'' in lines[lineInd+shift]:
                        node = lines[lineInd+shift]
                        node = node[node.find('\'')+1:]
                        node = node[:node.find('\'')]
                        node = int(node)
                        print(' This house has a corner at node %d'%(node,))
                        nodeSet.append(node)
                        shift -= 1
                nodeSets.append(nodeSet)

lats = [0.0]*len(houseNums)
lons = [0.0]*len(houseNums)

for line in lines:
    if '<node id=\'' in line:
        node = line[line.find('\'')+1:]
        node = node[:node.find('\'')]
        node = int(node)
        lat = line[line.find('lat=\'')+5:]
        lat = lat[:lat.find('\'')]
        lat = float(lat)
        lon = line[line.find('lon=\'')+5:]
        lon = lon[:lon.find('\'')]
        lon = float(lon)
        print('  Node %d is situated at (%f, %f).'%(node,lat,lon))
        for houseInd in range(len(houseNums)):
            if node in nodeSets[houseInd]:
                lats[houseInd] += lat
                lons[houseInd] += lon

print('Computing coordinates for each house...')

osmlink = lambda lat,lon: 'http://www.openstreetmap.org/?mlat=%.7f&mlon=%.7f&zoom=15'%(lat,lon)
mdlink = lambda title,url: '[%s](%s)'%(title,url)

for houseInd in range(len(houseNums)):
        if not len(nodeSets[houseInd]):
                print('house %s has no nodes'%(houseNums[houseInd]))
        lats[houseInd] /= len(nodeSets[houseInd])
        lons[houseInd] /= len(nodeSets[houseInd])
        print('  House %s is located at (%.7f, %.7f) - %s'%(houseNums[houseInd],lats[houseInd],lons[houseInd],osmlink(lats[houseInd],lons[houseInd])))

mdLines = ['#KAUST Directory\n\n']
mdLines.append('Based on %s data and distributed under the relevant license terms. Big thanks to Heikki Lehvaslaiho. For feedback, email juho.happola@iki.fi.\n\n'%(mdlink('open street map','http://openstreetmap.org/')))
mdLines.append('#Island\n\n')
for houseInd in range(len(houseNums)):
    if houseNums[houseInd][0] == 'I':
        mdLines.append('%s\n\n'%(mdlink(houseNums[houseInd],osmlink(lats[houseInd],lons[houseInd])),))

mdLines.append('#Gardens\n\n')
for houseInd in range(len(houseNums)):
    if houseNums[houseInd][0] == 'G':
        mdLines.append('%s\n\n'%(mdlink(houseNums[houseInd],osmlink(lats[houseInd],lons[houseInd])),))

mdLines.append('#Harbour\n\n')
for houseInd in range(len(houseNums)):
    if houseNums[houseInd][0] == 'H':
        mdLines.append('%s\n\n'%(mdlink(houseNums[houseInd],osmlink(lats[houseInd],lons[houseInd])),))

f = open('README.md','w')
f.writelines(mdLines)
f.close()


                
            
