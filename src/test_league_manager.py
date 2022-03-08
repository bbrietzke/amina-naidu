import unittest
from datetime import date

from lib.league_manager import LeagueManager
from lib.database_service import InMemoryDatabase, DatabaseService

class TestLeagueManager(unittest.TestCase):
    def test_empty_games(self):
        with InMemoryDatabase() as db:
            with LeagueManager(db) as lm:
                results = lm.show_current_game()
                self.assertIsNone(results)

    def test_add_game_for_week(self):
        this_week:int = date.today().isocalendar().week
        with DatabaseService('/tmp/test_add_game_for_week.sqlite3') as db:
            db.executescript(DatabaseService.database_ddl())
            with LeagueManager(db) as lm:
                self.assertGreater(lm.save_game(0, start_week = this_week - 1, url = "https://example.org/game/1", title = "testing 1"), 0)
                self.assertGreater(lm.save_game(0, start_week = this_week, url = "https://example.org/game/2", title = "testing 2"), 0)
                self.assertGreater(lm.save_game(0, start_week = this_week + 1, url = "https://example.org/game/3", title = "testing 3"), 0)

                game = lm.show_current_game()
                self.assertIsNotNone(game, "we don't have a game to display")
                self.assertGreater(game.id, 0, "Game Id is not greater than zero")
                self.assertEqual(int(game.start_week), int(this_week), "Weeks are not equal")

if __name__ == '__main__':
    unittest.main()