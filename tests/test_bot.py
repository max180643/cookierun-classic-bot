import unittest

import bot


class UnknownStageWatchdogTests(unittest.TestCase):
    def test_unknown_stage_times_out_at_group_limit(self):
        timeout = bot.UNKNOWN_STAGE_RESET_TIMEOUT["PRE_GAME"]

        self.assertFalse(bot.unknown_stage_timed_out(100.0, "PRE_GAME", 100.0 + timeout - 0.1))
        self.assertTrue(bot.unknown_stage_timed_out(100.0, "PRE_GAME", 100.0 + timeout))

    def test_known_stage_has_no_watchdog_start(self):
        self.assertFalse(bot.unknown_stage_timed_out(None, "PRE_GAME", 999.0))


if __name__ == "__main__":
    unittest.main()
