
import math
import json
import random

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

def List2Rad(degree):
	rad=[]
	for d in degree:
		rad += [(d*math.pi)/180]
	return rad

def List2Degree(rad):
	degree=[]
	for r in rad:
		degree += [(r*180)/math.pi]
	return degree

def toRad(degree):
	return (degree*math.pi)/180

class Problem:
		def __init__(self, env, robot):
			self.env = env
			self.robot = robot
		def toVector(self, configuration):
			points = []
			points += [{'x' : self.robot['position'][0], 'y' : self.robot['position'][1]}]
			angle = 0;
			for i in range(0, len(configuration)):
				angle += configuration[i];
				points += [{'x' : points[i]['x']+self.robot['links'][i]*math.cos(angle), 
			    			'y' : points[i]['y']+self.robot['links'][i]*math.sin(angle)}]
			return points

		def isCollide(self, robot_vector):
			for obs in self.env['obsticles']:
				obs_segs = [[obs['p1'], obs['p2']], [obs['p2'], obs['p3']], [obs['p3'], obs['p1']]]
				for i in range(0, len(obs_segs)):
					for j in range(0, len(robot_vector)-1):
						if segment2segment(obs_segs[i][0], obs_segs[i][1], robot_vector[j], robot_vector[j+1]):
							return True

			return False

		def isGoal(self, robot_vector, goal):
			if goal[0]+10 >= robot_vector[-1]['x'] and goal[0] <= robot_vector[-1]['x'] and \
				goal[1]+10 >= robot_vector[-1]['y'] and goal[1] <= robot_vector[-1]['y']:
				return True
			return False

		def getNeighbors(self, state):
			neighbors = list()
			dn_list = [toRad(-10), toRad(-5), 0, toRad(5), toRad(10)]

			return neighbors;

		def isActive(self, probability):
			return (random.random() < probability)

		def find_configuration(self, state_conf, goal):
			d_joints = self.robot['djoints']

			for i in range(0, 1000000):
				conf = state_conf[:]
				for j in range(0, len(conf)):
					if self.isActive(self.robot['activations'][j]):
						djoint_len = len(d_joints[j])
						conf[j] += toRad(d_joints[j][random.randint(0, djoint_len-1)])

				vr = pr.toVector(conf)
				if self.isGoal(vr, goal):
					if not self.isCollide(vr):
						return List2Degree(conf)
			return False



# =============================================================================================

# Load environment map
with open('map.json') as data_file:    
	env_map = json.load(data_file)

# Load Robot
with open('robot.json') as data_file:    
	robot = json.load(data_file)

# Load Robot
with open('paths.json') as data_file:  
	paths = json.load(data_file)
paths = paths['paths']

firstPath = paths[0]

print "Path length: ", len(firstPath)

pr = Problem( env_map, robot )

configurations = list()
conf = pr.find_configuration( List2Rad(robot['joints']), [firstPath[1][0]*10, firstPath[1][1]*10] );
print conf
configurations += [conf]

for i in range(2, len(firstPath)):
	conf = pr.find_configuration( List2Rad(conf), [firstPath[i][0]*10, firstPath[i][1]*10] )
	configurations += [conf]
	print conf
	if not conf:
		break

dataout = {'configurations': configurations}

with open('data/configurations.json', 'w') as outfile:
    json.dump(dataout, outfile)			