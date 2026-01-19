"""
Permissions Example - OpenCode Parity Feature

Demonstrates pattern-based permissions and doom loop detection.
"""

import tempfile
import shutil
from praisonaiagents.permissions import (
    PermissionManager,
    PermissionRule,
    PermissionAction,
    DoomLoopDetector
)


def main():
    # Create temporary storage for permissions
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Create permission manager
        manager = PermissionManager(storage_dir=temp_dir)
        
        # Add permission rules
        print("=== Setting up permission rules ===")
        
        manager.add_rule(PermissionRule(
            pattern="read:*",
            action=PermissionAction.ALLOW,
            description="Allow all read operations"
        ))
        
        manager.add_rule(PermissionRule(
            pattern="bash:rm *",
            action=PermissionAction.DENY,
            description="Block rm commands"
        ))
        
        manager.add_rule(PermissionRule(
            pattern="bash:*",
            action=PermissionAction.ASK,
            description="Ask for other bash commands"
        ))
        
        # Check permissions
        print("\n=== Checking permissions ===")
        
        targets = [
            "read:config.py",
            "bash:rm -rf /tmp",
            "bash:ls -la",
            "write:output.txt"
        ]
        
        for target in targets:
            result = manager.check(target)
            print(f"{target}: {result.action.value}")
        
        # Doom loop detection
        print("\n=== Doom Loop Detection ===")
        
        detector = DoomLoopDetector(loop_threshold=3)
        
        for i in range(5):
            result = detector.record_and_check("bash", {"cmd": "ls"})
            if result.is_loop:
                print(f"Loop detected after {result.loop_count} calls!")
                print(f"Recommendation: {result.recommendation}")
                break
            else:
                print(f"Call {i+1}: OK")
        
        print("\n=== Done ===")
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
