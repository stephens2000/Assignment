from collections import defaultdict
from collections.abc import Callable
from typing import Any


class EventDispatcher:
    """
    A small synchronous event dispatcher based on the Observer Pattern.
    """

    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable[..., Any]]] = defaultdict(list)

    def subscribe(self, event_type: str, callback: Callable[..., Any]) -> None:
        """
        Subscribe a callback function to an event type.
        """
        if not isinstance(event_type, str) or not event_type:
            raise ValueError("event_type must be a non-empty string")

        if not callable(callback):
            raise TypeError("callback must be callable")

        self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable[..., Any]) -> None:
        """
        Remove a callback from an event type.
        """
        callbacks = self._subscribers.get(event_type)

        if not callbacks:
            return

        try:
            callbacks.remove(callback)
        except ValueError:
            return

        if not callbacks:
            del self._subscribers[event_type]

    def dispatch(self, event_type: str, *args, **kwargs) -> None:
        """
        Dispatch an event to all subscribed callbacks.
        """
        callbacks = list(self._subscribers.get(event_type, []))

        for callback in callbacks:
            try:
                callback(*args, **kwargs)

            except Exception as error:
                callback_name = getattr(
                    callback,
                    "__name__",
                    repr(callback)
                )

                print(
                    f"Error in callback '{callback_name}' "
                    f"for event '{event_type}': {error}"
                )


# --------------------------
# Example Usage / Test Code
# --------------------------

def email_notification(user: str) -> None:
    print(f"Email sent to {user}")


def sms_notification(user: str) -> None:
    print(f"SMS sent to {user}")


def faulty_notification(user: str) -> None:
    raise RuntimeError("Notification service unavailable")


if __name__ == "__main__":

    dispatcher = EventDispatcher()

    dispatcher.subscribe("user_registered", email_notification)
    dispatcher.subscribe("user_registered", sms_notification)
    dispatcher.subscribe("user_registered", faulty_notification)

    print("Dispatching event...\n")

    dispatcher.dispatch("user_registered", "Stephen Sunguro")

    print("\nRemoving SMS notification...\n")

    dispatcher.unsubscribe("user_registered", sms_notification)

    dispatcher.dispatch("user_registered", "Stephen Sunguro")  