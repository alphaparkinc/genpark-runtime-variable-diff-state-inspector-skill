"""
Demonstration of genpark-runtime-variable-diff-state-inspector-skill
"""

from client import NamespaceVariableDiffInspectorClient

def main():
    inspector = NamespaceVariableDiffInspectorClient()

    # Initial state
    ns = {"user_id": 42, "role": "viewer"}
    snap_before = inspector.take_snapshot(ns)

    # State modification after agent step
    ns["role"] = "administrator"
    ns["auth_token"] = "tok_sec_9918"
    del ns["user_id"]

    snap_after = inspector.take_snapshot(ns)
    diff = inspector.compute_diff(snap_before, snap_after)

    print("=== VARIABLE STATE DIFF REPORT ===")
    print(f"Added Variables: {list(diff['added'].keys())}")
    print(f"Modified Variables: {list(diff['modified'].keys())}")
    print(f"Removed Variables: {list(diff['removed'].keys())}")
    print(f"Role mutation: {diff['modified']['role']['old']['repr']} -> {diff['modified']['role']['new']['repr']}")

if __name__ == "__main__":
    main()
