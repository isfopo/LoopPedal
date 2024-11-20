install:
	python3 scripts/install.py --name LoopPedal

watch:
	python3 scripts/watch.py --version 'Live 12.1.1'

close-set:
	pkill -x Ableton Live 12 Suite

open-set:
	open set/set.als

reload:
	just install && just close-set && sleep 1 && just open-set
