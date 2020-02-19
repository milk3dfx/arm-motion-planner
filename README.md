# Motion planning: Decoupled motion planning algorithm for high DOF robot with topological re-planner

Motion planning for high degrees of freedom system is difﬁcult problem which is require sophisticated approaches and computational powerful equipment, since search problem in high dimensions has large branching factor. In order to simplify the high DOF problem it is possible to divide the problem on several low dimensional problems. This method called decoupling and actively applies for some classes of motion planning problems such as multiple robot motion planning or humanoid robots motion planning where planning happens separately for upper and lower parts of the robot body.

Motion planner usually use direct search methods and searches C-space with some commonly used algorithms such as A* for lower dimensional C-space or RRT (Rapidly exploring random tree) for high dimensional problem, or their modiﬁcations. 

Some of the search algorithms taking to account topological features of the work space. By extending C-space with topology class. Topology class is a parameter which is show how path relates to the objects in work space. This kind of search allows to ﬁnd different fusible path in work space as well as in C-space

[See report for details](./Decoupled%20motion%20planning%20algorithm%20for%20high%20DOF%20robot%20with%20topological%20re-planner.pdf)
