"""Script to be used as a command in the terminal to set up an alarm."""

import time
import tkinter as tk
from datetime import datetime, timedelta

import click
import playsound


@click.command()
@click.option(
    "--at",
    type=str,
    # prompt="When should the alarm go off?",
    help="Time when the alarm should go off",
)
@click.option(
    "--after",
    type=str,
    help="Time to wait from now until the alarm goes off. \
    Format: HH:MM or just the number of seconds.",
)
# @click.option(
# "--repeatfor", type=int, help="Time interval after which alarm stops repeating."
# )
# @click.option("--repeatinterval", type=int, help="Time interval between repetitions.")
@click.option("--sound", type=str, help="Sound file to play when alarm rings")
@click.option("--message", type=str, help="Message to display in the dialog box")
def alarm_clock(at, after, sound, message):
    """Set an alarm."""
    # Calculate the time to wait (in seconds) until the alarm goes off
    if at:
        delta = _compute_time_to_wait(target_time=at)
        time_to_wait = delta.total_seconds()
    elif after:
        # delta = _convert_to_datetime(after)
        # time_to_wait = delta.total_seconds()
        if ":" in after:
            time_to_wait = _after_to_seconds(after)
        else:  # Already in seconds
            time_to_wait = int(after)

    else:
        raise TypeError("You must provide either the --at or --in argument")

    win = tk.Tk()
    win.withdraw()

    # Start the alarm loop
    # if repeatfor:  # False if alarm should not repeat at all
    #     keep_repeating = True
    #     time_since_alarm_started = 0
    # else:
    #     keep_repeating = False
    # while True:
    # Wait until the alarm goes off
    time.sleep(time_to_wait)

    # Play the alarm sound
    playsound.playsound(sound, block=False)

    # # Note the change to this line
    # frame = tk.Frame(win, width=500, height=500)
    # frame.pack()  # Note the parentheses added here

    # stop_button = tk.Button(my_frame, text="I am at (100x150)")
    # button1.place(x=100, y=150)

    # Display the dialog box with the message and a stop button
    messagebox = tk.Toplevel(win)
    # messagebox = tk.Toplevel(frame)
    messagebox.title("Alarm")
    label = tk.Label(messagebox, text=message, width=200, height=50)
    label.pack()
    stop_button = tk.Button(
        messagebox,
        text="Stop Alarm",
        command=lambda: _stop_alarm(win),
        height=20,
        width=20,
        background="red",
    )
    stop_button.pack()

    # Start the GUI event loop
    win.mainloop()

    # if keep_repeating:
    #     time_since_alarm_started += time_to_wait  # Update
    #     print(time_since_alarm_started)
    #     if time_since_alarm_started >= repeatfor:
    #         break
    # else:
    #     break
    # # Calculate the time to wait until the next alarm
    # time_to_wait = repeatinterval


def _compute_time_to_wait(target_time):
    """Compute time to wait until `target_time`, in seconds.

    Arguments:
        target_time: str
            Time when alarm should go off. Format: HH:MM.

    Returns:
        delta: int
    """
    target_date = _convert_to_datetime(target_time)
    delta = target_date - datetime.now()
    return delta


def _convert_to_datetime(time_string):
    """Convert time HH:MM to datetime.

    Assumed date will be today if time has not passed yet and tomorrow otherwise.
    """
    time_only = datetime.strptime(time_string, "%H:%M").time()
    today = datetime.now().date()
    date_and_time = datetime.combine(today, time_only)
    now = datetime.now().time()
    if time_only < now:  # If time has already passed, alarm will go off tomorrow
        date_and_time += timedelta(days=1)
    return date_and_time


def _after_to_seconds(time_str):
    time = datetime.strptime(time_str, "%H:%M").time()
    today = datetime.now().date()
    target = datetime.combine(today, time)
    zero = datetime.min.time()
    minimum = datetime.combine(today, zero)
    return int((target - minimum).total_seconds())


def _stop_alarm(window):
    window.destroy()


if __name__ == "__main__":
    alarm_clock()
