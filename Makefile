.PHONY: run

run:
	python src/main.py

test:
	rm -f /tmp/test_add_game_for_week.sqlite3 /tmp/test_empty_games.sqlite3
	python src/test_league_manager.py