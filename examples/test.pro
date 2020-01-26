% SENTENCES: 
sent(0,['Bill', 'and', 'Joe', 'gave', 'the', 'blue', 'book', 'to', 'Mary', 'Poppins', 'in', 'New', 'York', '.']).
sent(1,['The', 'blue', 'book', 'is', 'about', 'machine', 'learning', '.']).
sent(2,['Mary', 'went', 'to', 'Paris', 'and', 'sold', 'the', 'book', 'to', 'a', 'bookseller', '.']).
sent(3,['When', 'Bill', 'and', 'Joe', 'went', 'to', 'Paris', 'they', 'bought', 'the', 'same', 'book', 'from', 'the', 'bookseller', '.']).

% LEMMAS: 
sent(0,['bill', 'and', 'joe', 'give', 'the', 'blue', 'book', 'to', 'mary', 'poppins', 'in', 'new', 'york', '.']).
sent(1,['the', 'blue', 'book', 'be', 'about', 'machine', 'learning', '.']).
sent(2,['mary', 'go', 'to', 'paris', 'and', 'sell', 'the', 'book', 'to', 'a', 'bookseller', '.']).
sent(3,['when', 'bill', 'and', 'joe', 'go', 'to', 'paris', 'they', 'buy', 'the', 'same', 'book', 'from', 'the', 'bookseller', '.']).

% RELATIONS: 
svo('joe', 'give', 'book', [0]).
svo('bill', 'give', 'book', [0]).
svo('bill', 'is_a', 'person', [0, 3]).
svo('joe', 'is_a', 'person', [0, 3]).
svo('mary', 'is_a', 'person', [0, 2]).
svo('poppins', 'is_a', 'person', [0]).
svo('new', 'is_a', 'state_or_province', [0]).
svo('york', 'is_a', 'state_or_province', [0]).
svo('blue', 'as_in', 'blue_book', [0, 1]).
svo('book', 'as_in', 'blue_book', [0, 1]).
svo('mary', 'as_in', 'mary_poppins', [0]).
svo('poppins', 'as_in', 'mary_poppins', [0]).
svo('new', 'as_in', 'new_york', [0]).
svo('york', 'as_in', 'new_york', [0]).
svo('book', 'is_a', 'learning', [1]).
svo('machine', 'as_in', 'machine_learning', [1]).
svo('learning', 'as_in', 'machine_learning', [1]).
svo('mary', 'go', 'paris', [2]).
svo('mary', 'sell', 'bookseller', [2]).
svo('mary', 'sell', 'book', [2]).
svo('paris', 'is_a', 'city', [2, 3]).
svo('bookseller', 'is_a', 'title', [2, 3]).
svo('bill', 'go', 'paris', [3]).
svo('joe', 'go', 'paris', [3]).
