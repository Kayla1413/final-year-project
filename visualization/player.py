#用一个长度为2的字符串表示一张牌：(D,C,H,S) + (A,2,3,4,5,6,7,8,9,0,J,Q,K)   用"jk"、"JK"分别表示小王、大王player模块设计：
# (D,C,H,S) + (A,2,3,4,5,6,7,8,9,0,J,Q,K)   用"jk"、"JK"分别表示小王、大王
# 黑桃-spade 红桃-heart 方快-diamond 草花-club

class Player(object):
	"""docstring for Player"""
	def __init__(self, role):
		self.roles = ('East', 'North', 'West', 'South')
		self.points = ('5', '10', 'K')
		self.colors = ('D', 'C', 'H', 'S')
		self.nums = ('A', 'K', 'Q', 'J', '0', '9','8','7','6','5','4','3','2')
		self.nums_order = {num: power for power, num in enumerate(self.nums)}

		self.cards = {color: [] for color in self.colors}
		# record all cards had been pushed out
		self.cards_record = {color: [] for color in self.colors}

		self.role = role
	
	def judge_snatch(self):
		main_color = None
		Max = -1
		for color in self.colors:
			if self.main_value in self.cards[color]:
				n = len(self.cards[color])
				if Max < n:
					main_color = color
					Max = n

		if not main_color:
			return ''
		else:
			return main_color + self.main_value

	def add_card(self, current_card):
		# add card
		color, num = current_card
		self.cards[color].append(num)

	def remove_card(self, current_card, cards):
		# remove card from cards
		color, num = current_card
		self.cards[color].remove(num)
		

	def add_left_cards(self, left_cards):
		'''
		只需要庄家才会用到，表示底牌是left_cards，left_cards是一个长度为2的字符串的list
		需要返回玩家准备埋到底牌的牌，返回值也是一个长度为2的字符串的list
		'''
		# left sequence: main_point, point, num_small, main_color_small
		for card in left_cards:
			self.add_card(card, self.cards)
		cards, count = [], 0
		# main_point
		for num in self.cards[self.main_color]:
			card = self.main_color + num
			if num in self.points:
				self.remove_card(card, self.cards)
				cards.append(card)
				if count == 5:
					return cards
				else:
					count += 1

		# point
		for color in self.colors[:-1]:
			for num in self.cards[color]:
				card = color + num
				if num in self.points:
					self.remove_card(card, self.cards)
					cards.append(card)
					if count == 5:
						return cards
					else:
						count += 1

		# num_small
		for color in self.colors[:-1]:
			if color == self.main_color:
				continue
			nums = sorted(self.cards[color], key=lambda num: self.nums_order[num])
			for num in nums:
				card = color + num
				self.remove_card(card, self.cards)
				cards.append(card)
				if count == 5:
					return cards
				else:
					count += 1
		# otherwise
		nums = sorted(self.cards[self.main_color], key=lambda num: self.nums_order[num])
		for num in nums:
			card = self.main_color + num
			self.remove_card(card, self.cards)
			cards.append(card)
			if count == 5:
				return cards
			else:
				count += 1

		return cards

	def finish_one_round(self, current_cards, turn):
		'''
		表示这一轮出牌结束，玩家被告知这一轮的出牌信息，
		current_turn_out_cards表示一个三元组(order,role,card)的list，
		每一个三元组表示这一轮你出牌之前的某一个人出的牌的信息，
		order是一个整数，表示出牌顺序(1,2,3,4)
		role是一个字符串，表示角色("banker","banker_opposite","banker_left","banker_right")
		card是一张牌
		'''
		for card in current_cards:
			self.add_card(card, self.cards_record)


	def play_out_cards(self, turn, current_turn_out_cards):
		pass

	def show_cards(self):
		'''
		return the player's cards
		'''
		cards = []
		for color in self.colors[:-1]:
			for num in self.cards[color].values():
				card = color + num
				cards.append(card)

		for card in self.cards['K']:
			card.append(card)

		return cards
