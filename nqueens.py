from copy import copy, deepcopy

class CSP: # full csp with variabless, domain, and constraints
	def __init__(self, queens, doms, cons, rows):
		self.queens = queens   # list of all queens, the number of the queen is the column it will be placed in
		self.doms = doms       # dict mapping queen to its domain, the domain is all the possible rows it can be placed in
		self.cons = cons       # lisf of lists mapping queen to list of constraints (first item in list if the pair of queens)
		self.rows = rows       # the row the queen is assigned to
	# for printing
	def __str__(self):
		return "queens: " + str(self.queens) + "\ndomain: " + str(self.doms) + "\nconstraints " + str(self.cons) + "\nrow: " + rows
	def __repr__(self):
		return "queens: " + str(self.queens) + "\ndomain: " + str(self.doms) + "\nconstraints " + str(self.cons) + "\nrow: " + rows


# constructs a constraint satisfaction problem with the given number of queens (nqueens)
def make_csp(nqueens):
	queens = []  # list of queens,  numbered 1-n
	doms = {}    # domains of the queens
	rows = {}    # rows the queens will be placed in
	cons = []    # list of constraints for each queen
	for i in range(1, nqueens+1): # set list of queens
		queens.append(i)
	for i in range(1, nqueens+1): # set list of domains for each queen
		doms.update({i : queens})
	for i in range(1, nqueens+1): # set all row assignments to 0 (no row assigned yet)
		rows.update({i: 0})
	for i in range(1, nqueens):   # find and set constraints for each pair of queens
		for j in range(i+1, nqueens+1):
			if i != j:
				cons.append(set_constraints(i, j, nqueens))
	csp = CSP(queens, doms, cons, rows)
	return csp


def set_constraints(q1, q2, nqueens): # q2 represents the columns
	cons = []
	row2 = 1
	dcol = abs(q1 - q2)
	cons.append([q1, q2])
	for row1 in range(1, nqueens+1):
		for row2 in range(1, nqueens+1):
			drow = abs(row1 - row2)
			if row1 != row2 and q1 != q2 and drow != dcol:
				cons.append([row1, row2])
	return cons


def revise(csp, q1, q2):
	revised = False
	d1 = copy(csp.doms[q1]) # domain of first queen to be modified
	d2 = copy(csp.doms[q2]) # domain of second queen
	new_d2 = []

	# find the index of the constraints for q1 and q2
	count = 0
	for i in csp.cons:  # find the index of the constraint list between q1 and q2
		check = copy(csp.cons[count][0])
		if check == [q1, q2]:
			index = count
			break
		count+=1
	cons = copy(csp.cons[index])
	cons.pop(0) # remove the list that contains the pair of queens

	what = []
	for i in cons:
		if [i[0]] == d1:
			what.append(i)

	#print "what: ", what

	for j in what: # for each of the constraints between the two queens
		#if j[1] not in d2:
		#	revised = False
		#else:
		if j[1] in d2:
			if j[1] not in new_d2:
				new_d2.append(j[1])
				revised = True


	csp.doms[q2] = new_d2 # modify q1's domain

	return revised



def ac_3(csp, q1):
	arc_q = []
	for i in csp.cons:
		#print i[0]
		check = copy(i[0])
		#print "check=", check
		if check[0] == q1:
			if check not in arc_q:
				arc_q.append(check)
		elif check[1] == q1:
			if check not in arc_q:
				arc_q.append(check)

	while len(arc_q) != 0:
		chk = copy(arc_q[0]) # arc to check
		arc_q.pop(0)     # pop from queue
		if revise(csp, chk[0], chk[1]):
			if len(csp.doms[chk[0]]) == 0: # if no values left in domain
				return False
			if len(csp.doms[chk[1]]) == 0: # if no values left in domain
				return False

	for i, j in csp.doms.items(): # i = queen, j = [row]
		if len(j) == 0:
			return False
		elif len(j) == 1:
			if csp.doms[i] not in csp.rows.values():
				csp.rows[i] = csp.doms[i]
				#return True

	return True

def min_rem_vals(csp):
	check = []  # list of queens who are unassigned/no row
	min_len = 100
	val = 1
	for i, j in csp.rows.items(): # find all unassigned queen to be checked
		if j == 0:
			check.append(i)

	for i in check: # check to find the domain with the least values
		if len(check) == 1:
			return check[0]
		dom = copy(csp.doms[i])
		for j in check: # for all other queens, see if domain of i is smaller
			if i == j:
				continue
			if len(dom) < min_len:
				min_len = len(dom)
				val = i
	return val



def backtracking_search(csp):
	result = backtrack(csp, 1)
	if result == True:
		print "success: solution found"
		ret = list(csp.rows.values());
		ret2 = []
		for i in ret:
			ret2.append(i)
		return ret2
	print "failed: no possible solutions"
	return False


def backtrack(csp, index):
	mod_csp = deepcopy(csp)

	if 0 not in mod_csp.rows.values():
		csp.rows = mod_csp.rows
		#print mod_csp.rows
		return True

	domain = copy(mod_csp.doms[index])
	#random.shuffle(domain)

	for value in domain:
		mod_csp = deepcopy(csp)
		mod_csp.doms[index] = [value]

		if ac_3(mod_csp, index) != False:
			if 0 not in mod_csp.rows.values():
				csp.rows = mod_csp.rows
				return True
			result = backtrack(mod_csp, min_rem_vals(mod_csp))
			if result == True:
				csp.rows = mod_csp.rows
				return True
	return False


csp = make_csp(12)
backtracking_search(csp)
print csp.rows


