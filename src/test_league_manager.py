import unittest, logging, sys

from lib.league_manager import LeagueManager
from lib.database_service import InMemoryDatabase

logger4 = logging.getLogger('league')
logger4.setLevel(logging.DEBUG)
handler4 = logging.StreamHandler(sys.stdout)
handler4.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger4.addHandler(handler4)

class TestLeagueManager(unittest.TestCase):
    def test_empty_games(self):
        with InMemoryDatabase() as db:
            with LeagueManager(db) as lm:
                results = lm.show_current_game()
                self.assertIsNone(results)

    def test_add_game_for_week(self):
        with InMemoryDatabase() as db:
            with LeagueManager(db) as lm:
                results = lm.show_current_game()
                self.assertIsNotNone(results)


if __name__ == '__main__':
    unittest.main()