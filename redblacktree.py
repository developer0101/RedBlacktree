'''
Reza Fathi
University of Houston
Red Black Tree Data Structure
'''
import random, sys, time, unittest
RED = "R"
BLACK = "B"
class Node:
	def __init__(self, val=None, p = None, color=RED, left=None, rigth=None):
		self.val = val
		self.p = p
		self.color = color
		self.left = left
		self.rigth = rigth

	def __str__(self):
		v = self.val if self.val is not None else "N"
		p = self.p.val if self.p else "N"
		lc = self.left.val if self.left and self.left.hasVal() else ""
		rc = self.rigth.val if self.rigth and self.rigth.hasVal() else ""
		return "{0}{1}{2}({3},{4})".format(v,self.color, p, lc, rc)

	def hasVal(self):
		return self.val is not None

	def hasTwoChild(self):
		return self.left and self.left.hasVal() and self.rigth and self.rigth.hasVal()

	def hasTwoBchild(self):
		return (self.left is None or self.left.color==BLACK)\
			and (self.rigth is None or self.rigth.color==BLACK)

	def getMinNode(self):
		return self.left.getMinNode() if self.left and self.left.hasVal() else self

	def isvalid(self, minv=-sys.maxsize, maxv=sys.maxsize):
		res, bc = (self.val is None or minv <= self.val <= maxv), (1 if self.color == BLACK else 0)
		if res:
			lres, lbc = (True, 0) if self.left is None else self.left.isvalid(minv, self.val)
			rres, rbc = (True, 0) if self.rigth is None else self.rigth.isvalid(self.val, maxv)
			res = lres and rres and (lbc == rbc)
			bc += lbc
		return res, bc

	def inorder(self, detail=False):
		res = self.left.inorder(detail) if self.left else []
		if detail:
			res += [str(self)]
		else:
			res += [self.val] if self.val is not None else []
		res += self.rigth.inorder(detail) if self.rigth else []
		return res

class RBtree:
	def __init__(self):
		self.root = None

	def newNode(self, val, p):
		x = Node(val, p)
		if x.p is None:
			self.root = x
		elif val < p.val:
			p.left = x
		else:
			p.rigth = x
		x.left = Node(None, x, BLACK)
		x.rigth = Node(None, x, BLACK)
		return x

	def transplant(self, x, y):
		if x.p is None:
			self.root = y
		elif x.p.left == x:
			x.p.left = y
		else:
			x.p.rigth = y
		if y:
			y.p = x.p

	def leftRotate(self, x):
		root = x.rigth
		self.transplant(x, root)
		if root.left:
			root.left.p = x
			x.rigth = root.left
		else:
			x.rigth = Node(None, x, BLACK)
		x.p = root
		root.left = x

	def rigthRotate(self, x):
		root = x.left
		self.transplant(x, root)
		if root.rigth:
			root.rigth.p = x
			x.left = root.rigth
		else:
			x.left = Node(None, x, BLACK)
		x.p = root
		root.rigth = x

	def insfix(self, x):
		while x.color == RED and x.p and x.p.color == RED:
			p = x.p
			gp = p.p
			uncle = gp.left if gp.rigth == p else gp.rigth
			if uncle and uncle.color == RED:
				p.color = uncle.color = BLACK
				gp.color = RED
				x = gp
			else:
				if x.val < gp.val:
					if x.val >= p.val:
						self.leftRotate(p)
						p, x = x, p
					self.rigthRotate(gp)
				else:
					if x.val < p.val:
						self.rigthRotate(p)
						p, x= x, p
					self.leftRotate(gp)
				p.color = BLACK
				gp.color = RED
		self.root.color = BLACK

	def insert(self, val):
		p, x = None, self.root
		while x and x.hasVal():
			p, x = x, x.left if val < x.val else x.rigth
		x = self.newNode(val, p)
		self.insfix(x)

	def rotate(self, x, isLeft):
		if isLeft:
			self.leftRotate(x)
		else:
			self.rigthRotate(x)

	def delfix(self, x):
		while x != self.root and x.color == BLACK:
			w = x.p.left if x.p.rigth == x else x.p.rigth
			isLeft = True if x == x.p.left else False
			wleft, wrigth = (w.left, w.rigth) if isLeft else (w.rigth, w.left)
			if w and w.color == RED:
				w.color = BLACK
				x.p.color = RED
				self.rotate(x.p, isLeft)
			elif w.hasTwoBchild():
				w.color = RED
				x = x.p
			elif wrigth is None or wrigth.color == BLACK:
				wleft.color = BLACK
				w.color = RED
				self.rotate(w, isLeft^True)
			else:
				w.color = x.p.color
				x.p.color = BLACK
				wrigth.color = BLACK
				self.rotate(x.p, isLeft)
				x = self.root
		x.color = BLACK

	def deleteNode(self, x):
		if x.hasTwoChild():
			nn = x.rigth.getMinNode()
			x.val = nn.val
			self.deleteNode(nn)
		elif x.left is None or not x.left.hasVal():
			self.transplant(x, x.rigth)
			if x.color == BLACK:
				self.delfix(x.rigth)
		else:
			self.transplant(x, x.left)
			if x.color == BLACK:
				self.delfix(x.left)

	def delete(self, val):
		x = self.root
		while x and x.hasVal() and x.val != val:
			x = x.left if val < x.val else x.rigth
		if x and x.hasVal() and x.val == val:
			self.deleteNode(x)

	def isvalid(self):
		if self.root:
			res, bc = self.root.isvalid()
			return res and self.root.color == BLACK
		return True

	def inorder(self, detail=False):
		return self.root.inorder(detail) if self.root else []

class Test(unittest.TestCase):
	def test_all(self):
		random.seed(time.time())
		m = 1000
		nums = list(range(m))
		random.shuffle(nums)
		t = RBtree()
		for num in nums:
			t.insert(num)
		assert t.isvalid()

		random.shuffle(nums)
		for num in nums:
			t.delete(num)
			assert t.isvalid()

if __name__=="__main__":
	unittest.main()

