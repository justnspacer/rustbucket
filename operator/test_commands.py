"""
Test script for the command processor.

Run this to test command parsing and execution without SMS.
"""

import asyncio
from command_processor import CommandProcessor
from config import MONITOR_CONFIG


async def test_commands():
    """Test various commands."""
    processor = CommandProcessor(MONITOR_CONFIG)
    
    test_cases = [
        ("help", "Should show available commands"),
        ("status", "Should show system status"),
        ("health", "Should check all systems"),
        ("health prometheus", "Should check Prometheus specifically"),
        ("metrics up", "Should query Prometheus metrics"),
        ("logs error", "Should search logs for errors"),
        ("db", "Should show database stats"),
        ("gateway", "Should show gateway stats"),
        ("unknown", "Should show error for unknown command"),
        ("", "Should show help message"),
    ]
    
    print("=" * 60)
    print("TESTING COMMAND PROCESSOR")
    print("=" * 60)
    
    for command, description in test_cases:
        print(f"\n{'=' * 60}")
        print(f"Command: '{command}'")
        print(f"Expected: {description}")
        print("-" * 60)
        
        response = await processor.process(command)
        print(f"Response:\n{response}")
    
    print("\n" + "=" * 60)
    print("TESTING COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    asyncio.run(test_commands())
