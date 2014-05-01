Nagidal's Poker Tool

1. Abbreviations:
1.1 Card values: 
- A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2
- ace, king, quee, ten, nine, eight, seven, six, five, four, trey, deuce

1.2. Card colors:
- C, D, H, S = clubs, diamonds, hearts, spades

1.3. Cards
- CA = ace of clubs
- C8 = eight of clubs
- D2 = deuce of diamonds
- ST = ten of spades

2. Statistics
- p = probability

2. Hand type notation:
- AA, KK, QQ ... = two aces, kings, queens, ...
- AKs = ace and king of the same suite
- AKo = ace and king not of the same suite
- AK = ace and king (no matter if suited or off-suite)

Always write the higher card first.
- JTo = jack ten off-suite
- TJo = invalid notation.

Connected cards:
Connected cards (connectors) are cards which can be members of a straight

- T9 = ten and nine are connectors because they can form a straight with 7, 8, J (result: 7, 8, 9, T, J)
- 62 = six and deuce are connectors because they can form a straight with 3, 4, 5 (result: 2, 3, 4, 5, 6)
- T5 = ten and five are no connectors because there is no straight which contains both T and 5

- 0G connectors without any gap have adjacent values (e.g. 87, QJ, 32, etc.)
- 1G one-gapped connectors. In a striaght they have one card between them (e.g. 75, KJ, A3)
- 2G two-gapped connectors. In a striaght they have two cards between them (e.g. Q9, 52, AJ)
- 3G three-gapped connectors. In a striaght they have there cards between them (e.g. 73, AT, J7)

Suited vs. Off-Suite Connectors:
- 0Gs = cuited connectors.
- 2Go = off-suite two-gapper

3. Terms
- Hand = Denotes one round of poker, rather than the two cards a player gets.
- Pocket cards, Hole cards = Cards dealt to a player.

List of features:
- Texas Hold'em No Limit play of 2-22 players, be it humans or computer AIs. (Interface: text in command line)
- Programmable computer AIs.
- Generate a table of probabilities for getting a certain type of hand (e.g. AA, AKs, KTo, 0G, 1G, 2G, 3G (X-gaped connectors))
- Generate a table of probabilities for Hand types to win against other types (e.g. p of JTo winning against AKs, AQs, QQ, ...)
- Generate hands where certain requirements are met: e.g. 8 players at the table, one has AKo, other has TT
- Play required hands, generate statistics (p of win for a player in a given scenario)
- Calculate the probability of outcome of a given situation (without playing such hands, pure math)
- Record the hands played, hand histories (data to save: how many players, what AIs, their budget, their buy-in, their money, table stakes, players' seat numbers at the table, players' position, players' cards, player's bets, community cards, pot size)
- Converter between compressed hand history and a human-readable hand history.