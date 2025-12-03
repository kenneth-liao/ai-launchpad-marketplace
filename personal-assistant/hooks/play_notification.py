#!/usr/bin/env python3
"""Cross-platform notification sound player."""

import platform
import subprocess
import sys


def play_sound() -> None:
    """Play a notification sound appropriate for the current OS."""
    system = platform.system()

    if system == "Darwin":  # macOS
        subprocess.run(
            ["afplay", "/System/Library/Sounds/Funk.aiff"],
            check=False,
            capture_output=True,
        )
    elif system == "Windows":
        try:
            import winsound
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        except Exception:
            # Fallback to PowerShell if winsound fails
            subprocess.run(
                [
                    "powershell",
                    "-c",
                    "(New-Object Media.SoundPlayer 'C:\\Windows\\Media\\chimes.wav').PlaySync()",
                ],
                check=False,
                capture_output=True,
            )
    elif system == "Linux":
        # Try paplay (PulseAudio) first, then aplay (ALSA)
        sound_files = [
            "/usr/share/sounds/freedesktop/stereo/complete.oga",
            "/usr/share/sounds/freedesktop/stereo/message.oga",
            "/usr/share/sounds/sound-icons/prompt.wav",
        ]
        for sound in sound_files:
            result = subprocess.run(
                ["paplay", sound],
                check=False,
                capture_output=True,
            )
            if result.returncode == 0:
                break
        else:
            # Try aplay as fallback
            subprocess.run(
                ["aplay", "-q", "/usr/share/sounds/sound-icons/prompt.wav"],
                check=False,
                capture_output=True,
            )


if __name__ == "__main__":
    play_sound()

