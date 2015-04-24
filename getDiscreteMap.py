import json
from pprint import pprint


def segment2segment(p11, p12, p21, p22):
	a1 = p12['y'] - p11['y'];
	b1 = p11['x'] - p12['x'];
	c1 = a1*p11['x'] + b1*p11['y'];
 
	a2 = p22['y'] - p21['y'];
	b2 = p21['x'] - p22['x'];
	c2 = a2*p21['x'] + b2*p21['y'];
	det = a1*b2 - a2*b1;
	if det == 0 :
		#Lines are parallel
		return False
	else:
		xi = (b2*c1 - b1*c2)/det;
		yi = (a1*c2 - a2*c1)/det;
		if(((p11['x']<=xi and xi<=p12['x']) or (p12['x']<=xi and xi<=p11['x'])) and 
			((p11['y']<=yi and yi<=p12['y']) or (p12['y']<=yi and yi<=p11['y'])) and 
			((p21['x']<=xi and xi<=p22['x']) or (p22['x']<=xi and xi<=p21['x'])) and 
			((p21['y']<=yi and yi<=p22['y']) or (p22['y']<=yi and yi<=p21['y']))):
			return True
		else:
			return False



with open('map.json') as data_file:    
    data = json.load(data_file)

oLines = [];
gridSize = 10;

for obst in data['obsticles']:
	oLines += [{'p1': obst['p1'], 'p2': obst['p2']}]
	oLines += [{'p1': obst['p1'], 'p2': obst['p3']}]
	oLines += [{'p1': obst['p2'], 'p2': obst['p3']}]

grid = [];
for i in range(0, data['width'], gridSize):
	for j in range(0, data['height'], gridSize):
		isColide = 0
		for l in oLines:
			if(segment2segment(l['p1'], l['p2'], 
				{'x':i, 'y':j}, 
				{'x':i, 'y':j+gridSize})):
				isColide = 1
				break
			if(segment2segment(l['p1'], l['p2'], 
				{'x':i, 'y':j+gridSize},
				{'x':i+gridSize, 'y':j+gridSize})):
				isColide = 1
				break
			if(segment2segment(l['p1'], l['p2'], 
				{'x':i+gridSize, 'y':j+gridSize},
				{'x':i+gridSize, 'y':j})):
				isColide = 1
				break
			if(segment2segment(l['p1'], l['p2'], 
				{'x':i+gridSize, 'y':j},
				{'x':i, 'y':j})):
				isColide = 1
				break
		grid += [isColide]

obsticles = []
for obs in data['obsticles']:
	obsticles += [[(0.0 + obs['p1']['x']+obs['p2']['x']+obs['p3']['x'])/(3*gridSize), 
			(0.0 + obs['p1']['y']+obs['p2']['y']+obs['p3']['y'])/(3*gridSize)]]

dataout = {'width': data['width']/gridSize, 
		'height': data['height']/gridSize, 
		'gridSize': gridSize, 
		'grid':grid,
		'obsticles': obsticles}

with open('grid.json', 'w') as outfile:
    json.dump(dataout, outfile)			

print "DONE."
#pprint(data)
