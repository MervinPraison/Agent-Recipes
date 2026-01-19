"""
Event Bus Example - OpenCode Parity Feature

Demonstrates the typed event system for PraisonAI Agents.
"""

from praisonaiagents.bus import EventBus, Event, EventType


def main():
    # Create an event bus
    bus = EventBus()
    
    # Track received events
    events_received = []
    
    # Subscribe to all events
    def on_any_event(event):
        events_received.append(event)
        print(f"[{event.type}] {event.data}")
    
    bus.subscribe(on_any_event)
    
    # Subscribe to specific event type
    def on_tool_complete(event):
        print(f"Tool completed: {event.data.get('tool_name')}")
    
    bus.subscribe(on_tool_complete, event_types=EventType.TOOL_COMPLETED.value)
    
    # Publish events
    print("Publishing events...")
    
    bus.publish(
        EventType.AGENT_STARTED,
        data={"agent_name": "Assistant", "task": "Code review"}
    )
    
    bus.publish(
        EventType.TOOL_STARTED,
        data={"tool_name": "read_file", "args": {"path": "main.py"}}
    )
    
    bus.publish(
        EventType.TOOL_COMPLETED,
        data={"tool_name": "read_file", "result": "success"}
    )
    
    bus.publish(
        EventType.AGENT_COMPLETED,
        data={"agent_name": "Assistant", "status": "success"}
    )
    
    print(f"\nTotal events received: {len(events_received)}")
    
    # Get event history
    history = bus.get_history(limit=10)
    print(f"Events in history: {len(history)}")


if __name__ == "__main__":
    main()
