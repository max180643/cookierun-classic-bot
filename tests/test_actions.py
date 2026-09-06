import unittest
from unittest.mock import call, patch

import actions


class RecoverFriendOverlayTests(unittest.TestCase):
    @patch("actions.time.sleep")
    @patch("actions.safe_device_tap")
    @patch("actions.detect_templates")
    def test_closes_friend_cookie_before_friend_info(self, detect_templates, tap, _sleep):
        detect_templates.side_effect = lambda _screen, templates, _region: (
            [(500, 25, 285, 65)]
            if templates == actions.FRIEND_COOKIE_DIALOG_TEMPLATE
            else []
        )

        recovered = actions.recover_friend_overlay(object())

        self.assertTrue(recovered)
        tap.assert_called_once_with(
            actions.DEVICE_IP,
            actions.DEVICE_PORT,
            actions.FRIEND_COOKIE_DIALOG_CLOSE_BUTTON[0],
            actions.FRIEND_COOKIE_DIALOG_CLOSE_BUTTON[1],
        )

    @patch("actions.time.sleep")
    @patch("actions.safe_device_tap")
    @patch("actions.detect_templates")
    def test_cancels_leftover_send_confirmation(self, detect_templates, tap, _sleep):
        detect_templates.side_effect = lambda _screen, templates, region: (
            [(505, 305, 275, 50)]
            if templates == actions.SEND_LIFE_CONFIRM_DIALOG_TEMPLATE
            and region == actions.SEND_LIFE_CONFIRM_DIALOG_REGION
            else []
        )

        recovered = actions.recover_friend_overlay(object())

        self.assertTrue(recovered)
        tap.assert_called_once_with(
            actions.DEVICE_IP,
            actions.DEVICE_PORT,
            actions.CANCEL_SEND_LIFE_BUTTON[0],
            actions.CANCEL_SEND_LIFE_BUTTON[1],
        )


class SendOneFriendLifeTests(unittest.TestCase):
    @patch("actions.safe_device_tap")
    @patch("actions._wait_for_template_to_clear", return_value=object())
    @patch("actions._wait_for_template", side_effect=[object(), object()])
    def test_each_tap_requires_its_expected_dialog(self, _wait, _wait_clear, tap):
        sent = actions._send_one_friend_life((609, 450, 111, 69))

        self.assertTrue(sent)
        self.assertEqual(
            tap.call_args_list,
            [
                call(actions.DEVICE_IP, actions.DEVICE_PORT, 664, 484),
                call(
                    actions.DEVICE_IP,
                    actions.DEVICE_PORT,
                    actions.CONFIRM_SEND_LIFE_BUTTON[0],
                    actions.CONFIRM_SEND_LIFE_BUTTON[1],
                ),
                call(
                    actions.DEVICE_IP,
                    actions.DEVICE_PORT,
                    actions.CLOSE_SEND_LIFE_DIALOG_BUTTON[0],
                    actions.CLOSE_SEND_LIFE_DIALOG_BUTTON[1],
                ),
            ],
        )

    @patch("actions.safe_device_tap")
    @patch("actions._wait_for_template", return_value=None)
    def test_missing_confirmation_prevents_blind_follow_up_taps(self, _wait, tap):
        sent = actions._send_one_friend_life((609, 450, 111, 69))

        self.assertFalse(sent)
        tap.assert_called_once_with(actions.DEVICE_IP, actions.DEVICE_PORT, 664, 484)


if __name__ == "__main__":
    unittest.main()
