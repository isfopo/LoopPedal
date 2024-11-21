install:
	python3 runners/install.py --name LoopPedal

watch:
	python3 runners/watch.py --version 'Live 12.1.1' --name 'LoopPedal'

close-set:
	pkill -x Ableton Live 12 Suite

open-set:
	open set/set.als

reload:
	just install && just close-set && sleep 1 && just open-set
