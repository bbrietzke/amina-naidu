.PHONY: run

run:
	python src/main.py

test:
	rm -rf /tmp/test_add_game_for_week.sqlite3
	python src/test_league_manager.py