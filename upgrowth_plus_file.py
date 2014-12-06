# Data Mining UO-Growth+ Algorithm 
# By Magus Verma , 2012141
# Written in python 2.7

import Queue


class Node:
	name 	= ""	# Node's Item Name
	count	= None	# Node's Support Count
	nu		= None	# Node's Overestimated Utility
	parent	= None	# Node's Parent
	hlink	= None	# Points to node whose item name is same as N.name
	children = None	# Children node's of current node
	level 	= None
	mnu 	= None

	def __init__(self,name,parent = None,nu=0,mnu=999999999):
		self.name = name
		self.count = 1
		self.nu = nu
		self.parent = parent
		self.children = {}
		self.mnu = mnu
		if self.parent!=None:
			self.level = self.parent.level + 1
		else:
			self.level = 0

	def show2(self):
		#print self.name,self.count,self.nu,self.children.keys()
		# if(self.parent != None):
			#print "parent: ",self.parent.name
		# print ".", 
		return 

	def show(self):
		return 
		# print ".",
		# if(self.parent != None):
			#print "([^"+str(self.parent.name)+","+str(self.parent.nu)+"],",
		#print self.name,self.nu,self.count,self.mnu,")",
	
	def insert_child_node(self,i,val,mnu):
		if i in self.children.keys():
			node = self.children[i]
			node.count += 1
			node.nu += val
			node.mnu = min(node.mnu,mnu)
		else:
			self.children[i] = Node(i,self,val,mnu)
		return self.children[i]


class HeaderTable:
	table = None

	def __init__(self,items):
		self.table = {item : {"utility":0,"link":None,"last":None} for item in items}

	def show(self):
		#print "_"*21+"Header Table"+"_"*21
		#print "name","utility","link"
		# for item in self.table.keys():
			#print item , "    ",self.table[item]["utility"] ,"    ", self.table[item]["link"]
		#print "_"*55
		print ".",

	def increment_utility(self,item_name,increment):
		if item_name in self.table.keys():
			self.table[item_name]["utility"] += increment
			return True
		else:
			return False

	def dgu(self,min_util):
		self.table = {k: v for k, v in self.table.iteritems() if v["utility"] >= min_util}

	def dlu(self,min_util):
		self.table = {k: v for k, v in self.table.iteritems() if v["utility"] >= min_util}

class UPTree:
	item_set 				= None
	header_table 			= None
	tree_root				= None
	profit_hash 			= None
	min_util				= None
	current_pattern_base	= ""
	infinity = 9999999
	
	def __init__(self,profit_hash=None,min_util=None):
		self.profit_hash 			= profit_hash
		if profit_hash != None:
			self.item_set 				= profit_hash.keys()
			self.header_table 			= HeaderTable(self.item_set)
		self.min_util				= min_util
		self.tree_root				= Node("Root")
		
	def from_patterns(self,pattern_base,min_util,x):
		self.current_pattern_base = x
		#print "_"*10+"Constructing UP Tree for CPB - "+str(x)+"_"*10
		#print "patterns:",pattern_base
		item_set = []
		for patterns in pattern_base:
			[pattern,support,cost] = patterns
			# #print pattern,support,cost
			for [item,mnu] in pattern:
				if item not in item_set:
					item_set.append(item)
		#print item_set
		self.item_set = item_set
		self.header_table = HeaderTable(self.item_set)
		self.min_util = min_util
	
		#print "Running Pattern scan with DNU " 
		for patterns in pattern_base:
			[pattern,support,cost] = patterns
			for [item,mnu] in pattern:
				self.header_table.increment_utility(item,cost*support)
		
		self.header_table.dlu(self.min_util)
		self.header_table.show()

		for i in range(len(pattern_base)):
			[pattern,support,cost] = pattern_base[i]
			new_pattern = []
			for [item,mnu] in pattern:
				present = bool(item in self.header_table.table.keys())
				if present:
					new_pattern.append([item,mnu])
				if not present:
					pattern_base[i][2] -= (mnu*support) #TODO
			pattern_base[i][0] = new_pattern
		for i in range(len(pattern_base)):
			pattern_base[i][0] = sorted(pattern_base[i][0], cmp=lambda x,y: self.get_head_val(y) - self.get_head_val(x))

		#print "modified:",pattern_base

		#print "done.. \n Inserting sorted patterns in UPTREE using DNN "
		for patterns in pattern_base:
			[pattern,support,cost] = patterns
			if len(pattern)==0:
				continue
			# #print pattern
			current_node = self.tree_root
			sum_mnu_coming_after = 0 #TODO
			#print pattern
			for [i,mnu] in pattern[1:]:
				sum_mnu_coming_after += mnu*support #TODO
			current_val = cost - sum_mnu_coming_after #TODO
			current_node = current_node.insert_child_node(pattern[0][0],current_val,pattern[0][1]) #TODO

			for [item,mnu] in pattern[1:]:
				current_val += mnu*support #TODO
				current_node = current_node.insert_child_node(item,current_val,mnu) #TODO

		#print "_"*55
	def get_head_val(self,item_mnu):
		[item,mnu] = item_mnu
		return self.header_table.table[item]["utility"]

	# row format = [('A',1),('C',10),('D',1)]
	def calculate_tu(self,row):
		Transaction_Utility = 0
		for item in row:
			# if item[0] in self.header_table.table.keys():
			item_name = item[0]
			quantity  = item[1]
			# #print Profit_Table
			item_value = Profit_Table[item_name]*quantity
			Transaction_Utility += item_value
		return Transaction_Utility

	def insert_reorganized_transaction(self,transaction):
		current_node = self.tree_root
		current_val = 0
		for i in transaction:
			item = i[0]
			quantity = i[1]
			nu = self.profit_hash[item]*quantity
			current_val += nu
			current_node = current_node.insert_child_node(item,current_val,nu)

	def show_header_table(self):
		self.header_table.show()

	def takeinput(self,f):
		row = f.readline().split(" ")
		if ' ' in row:row.remove(' ')
		row = [(row[2*i],int(row[2*i+1])) for i in range(len(row)/2)]
		return row

	def dbscan(self):
		#print "Running First Database Scan for computing TWU values" 
		f = open(database_file)
		row = self.takeinput(f)	
		while(len(row)!=0):
			tu = self.calculate_tu(row)
			#print row,tu
			for item in row:
				self.header_table.increment_utility(item[0],tu)
			row = self.takeinput(f)	
		f.close()
		#print "Computed TWU values for all nodes in header table"

	def reorganized_dbscan_dgn(self,show=True):
		#print "Showing Reorganized DB and Applying DGN" 
		f = open(database_file)
		row = self.takeinput(f)	
		while(len(row)!=0):
			filtered_row = []
			for item in row:
				if item[0] in self.header_table.table.keys():
					filtered_row.append(item)
			# row = sorted(filtered_row, key=lambda tup: tup[1],reverse=True)
			row = sorted(filtered_row, cmp=lambda x,y: self.header_table.table[y[0]]["utility"] - self.header_table.table[x[0]]["utility"])
			tu = self.calculate_tu(row)
			self.insert_reorganized_transaction(row)
			# if(show):
				#print row,tu
			row = self.takeinput(f)	
		f.close()

	def dgu(self):
		#print "Applying Discarding Global Unpromising Rule .."
		self.header_table.dgu(self.min_util)

	def show_tree(self):
		#print "_"*21+"Showing Constructed UPTREE"+"_"*21
		q = Queue.Queue()
		current_level = 0
		q.put(self.tree_root)
		while not q.empty():
			n = q.get()
			if(n.level!=current_level):
				#print
				current_level=n.level
			n.show()
			if(n.name!="Root"):
				if (self.header_table.table[n.name]["link"]==None):
					self.header_table.table[n.name]["link"] = n
					self.header_table.table[n.name]["last"] = n
				else:
					self.header_table.table[n.name]["last"].hlink = n
					self.header_table.table[n.name]["last"] = n
			for child_node_name in n.children.keys():
				q.put(n.children[child_node_name])
		#print
		#print "_"*55

	def show_lists(self):
		#print "Showing Header Link List Traversals"
		for i in self.header_table.table.keys():
			current = self.header_table.table[i]["link"]
			if(current != None):
				while(True):
					current.show()
					if(current.hlink == None):
						break
					current = current.hlink
				#print
		#print "_"*55

	def upgrowth_plus(self):
		#print "Conditional Pattern Basis"
		phui = []
		for item in self.header_table.table.keys():
			if(self.header_table.table[item]["utility"]>self.min_util):
				item_potential_value = 0
				cpb = []
				current = self.header_table.table[item]["link"]
				if(current != None):
					# Traversing Right
					while(True):
						item_potential_value += current.nu
						pb =[[],0,0] # [ [ [pattern,mnu],..],support,cost]
						pb[1] = current.count
						pb[2] = current.nu
						up = current.parent
						while(up.parent!=None):
							##print up.name
							pb[0].append([up.name,up.mnu])
							up = up.parent
						if len(pb[0])!=0:
							cpb.append(pb)
						if(current.hlink == None):
							break
						current = current.hlink
					if(item_potential_value>self.min_util):
						phui.append([item,item_potential_value])
				# #print item,cpb
				tree = UPTree()
				tree.from_patterns(cpb,self.min_util,self.current_pattern_base+item)
				tree.show_tree()
				tree.show_lists()
				# tree.show_miu()
				retreived = tree.upgrowth_plus()
				for i in retreived:
					phui.append([item+i[0],i[1]])
		#print "returning",phui
		print ".",
		#print "_"*55
		return phui

	def solve(self):
		self.dbscan()
		self.show_header_table()
		self.dgu()
		self.show_header_table()
		self.reorganized_dbscan_dgn()
		self.show_tree()
		self.show_lists()
		return self.upgrowth_plus()


database_file = "spaced.dat"
utility_data_file = "mushroomUtility.dat"
Profit_Table = {}
#print "Getting up Utility Values" 
f = open(utility_data_file)
row = f.readline()	
while(len(row)!=0):
	row = row[:-1]
	# #print row
	row = row.split(" ")
	row = [int(x) for x in row]
	Profit_Table[str(row[0])] = row[1] 
	row = f.readline()
#print Profit_Table
f.close()


problem = UPTree(Profit_Table,50)
print problem.solve()