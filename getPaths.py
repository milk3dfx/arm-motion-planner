import json
import math
import operator

class Problem:
	def __init__(self, env_path, start, goal, heuristic, connections):
		with open(env_path) as data_file:    
    			data = json.load(data_file)
		self.env = data
		self.start = start
		self.goal = goal
		self.heuristic = heuristic
		self.grid = list()
		self.connections = connections
		self.expended = 0

		print self.env['obsticles']
		
	def getStart(self):
		return self.start

	def getGoal(self):
		return self.goal

	def getHeuristic(self, state1, state2):
		if self.heuristic == "euclidian":
			return math.sqrt(
					(state2[0]-state1[0])*(state2[0]-state1[0]) + \
					(state2[1]-state1[1])*(state2[1]-state1[1]))
		else:
			return abs(state2[0]-state1[0]) + abs(state2[1]-state1[1])

	def getDistance(self, state1, state2):
		return math.sqrt(
			(state2[0]-state1[0])*(state2[0]-state1[0]) + \
			(state2[1]-state1[1])*(state2[1]-state1[1]))

	def isStateValid(self, state):
		if state[0] < 0:
			return False;
		if state[0] >= self.env['width']:
			return False;

		if state[1] < 0:
			return False;
		if state[1] >= self.env['height']:
			return False;

		if self.env['grid'][state[0]*self.env['height']+state[1]] == 1:
			return False;
		return True
		

	def getNeighbors(self, state):

		neighbors = list();
		dState = [(-1, 0), (0, 1), (1, 0), (0, -1)]
		if self.connections == 8:
			dState += [(-1,-1), (1,1), (-1,1), (1,-1)]

		for ds in dState:
			s = (state[0]+ds[0], state[1]+ds[1])
			if self.isStateValid(s):
				neighbors += [s]

		return neighbors;


def reconstruct_path(came_from, current):
	total_path = [current]
    	while current in came_from:
       		current = came_from[current]
       		total_path.append(current)
    	return total_path

def get_topology_change(state1, state2, obsticles):
	t = []
	for obs in obsticles:
		v1 = (state1[0] - obs[0], state1[1] - obs[1])
		v2 = (state2[0] - obs[0], state2[1] - obs[1])

		dot = v1[0]*v2[0] + v1[1]*v2[1]
		l1 = math.sqrt(v1[0]*v1[0]+v1[1]*v1[1])
		l2 = math.sqrt(v2[0]*v2[0]+v2[1]*v2[1])

		#print v1, v2
		#print dot
		#print l1, l2
		cos = dot/(l1*l2)
		if cos > 1.0:
			cos=1.0
		if cos < -1.0:
			cos = -1.0
		angle = math.acos(cos)

		sign = math.copysign(1, v1[0]*v2[1]-v1[1]*v2[0])
		t += [angle*sign]
	return t;

def getTopologyClasses(topology_value):
	classes = []
	for i in range(0, len(topology_value)):
		classes += [int(math.copysign(1, topology_value[i]))]
	return classes

def getTopologyHash(classes):
	t_hash = 0
	for i in range(0, len(classes)):
		t_hash += ((classes[i]+1)/2)*int(math.pow(2, i))
	return t_hash

def AStarT(problem):
	closedset = list()
	openset = list()
	came_from = dict()
	topology = dict()
	g_score = dict()
	f_score = dict()

	goal = problem.getGoal()
	start = problem.getStart()
	g_score[start] = 0
	f_score[start] = g_score[start] + problem.getHeuristic(start, goal)
	topology[start] = [0]*len(problem.env['obsticles'])
	openset.append(start)

	while len(openset)>0:
		current = openset[0]
		for el in openset:
			if f_score[el] < f_score[current]:
				current = el
		#print current
		if current == goal:
			print "Topology: ", topology[current]
       			return reconstruct_path(came_from, goal)

		openset.remove(current)
		closedset.append(current)
		problem.expended = problem.expended+1

		for neighbor_pos in problem.getNeighbors(current):
			top_change = get_topology_change(current, neighbor_pos, problem.env['obsticles'])
			top_value = map(operator.add, topology[current], top_change)
			neighbor = (neighbor_pos[0], neighbor_pos[1],
					getTopologyHash(getTopologyClasses(top_value)))


       			if neighbor in closedset:
               			continue
       			tentative_g_score = g_score[current] + problem.getDistance(current, neighbor)
       			if neighbor not in openset or tentative_g_score < g_score[neighbor]:
               			came_from[neighbor] = current
				topology[neighbor] = top_value
       				g_score[neighbor] = tentative_g_score
				f_score[neighbor] = g_score[neighbor] + \
					problem.getHeuristic(neighbor, goal) 

				if neighbor not in openset:
					openset.append(neighbor)
	return []

def toRad(degree):
	return (degree*math.pi)/180

def get_end_effector_position(path_to_robot):
	with open(path_to_robot) as data_file:    
    		robot = json.load(data_file)
	position = robot['position']
	angle = 0

	for i in range(0, len(robot['links'])):
		angle = angle + robot['joints'][i];
		position = [position[0]+robot['links'][i]*math.cos(toRad(angle)),
			    position[1]+robot['links'][i]*math.sin(toRad(angle))];
	return position

end_position = get_end_effector_position("robot.json")
end_position = [int(end_position[0]/10), int(end_position[1]/10)]
print "End effector position: ", end_position


print "GetPath"
prob = Problem("grid.json", (end_position[0],end_position[1],getTopologyHash([1,1])), 
	(40, 50, getTopologyHash([1,-1])), "euclidian", 8)
path = AStarT(prob)
path = path[::-1]
print path


dataout = {'paths': [path]}

with open('paths.json', 'w') as outfile:
    json.dump(dataout, outfile)			






