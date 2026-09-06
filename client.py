"""
Runtime Variable State Diff Inspector.
Zero external dependencies, standard library only.
"""

from typing import Dict, Any

class NamespaceVariableDiffInspectorClient:
    """
    Inspects and computes deltas between consecutive namespace states:
    - Identifies newly instantiated variables
    - Tracks mutated values and type transformations
    - Detects deleted variable bindings
    """

    def take_snapshot(self, namespace: Dict[str, Any]) -> Dict[str, Any]:
        """Extracts serializable representation of non-dunder variables."""
        snapshot = {}
        for k, v in namespace.items():
            if k.startswith("__"):
                continue
            snapshot[k] = {
                "type": type(v).__name__,
                "repr": repr(v)[:100]
            }
        return snapshot

    def compute_diff(self, before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Any]:
        """Computes added, modified, and removed variables."""
        before_keys = set(before.keys())
        after_keys = set(after.keys())

        added = {k: after[k] for k in after_keys - before_keys}
        removed = {k: before[k] for k in before_keys - after_keys}

        modified = {}
        for k in before_keys.intersection(after_keys):
            if before[k]["repr"] != after[k]["repr"] or before[k]["type"] != after[k]["type"]:
                modified[k] = {
                    "old": before[k],
                    "new": after[k]
                }

        return {
            "has_changes": bool(added or removed or modified),
            "added_count": len(added),
            "modified_count": len(modified),
            "removed_count": len(removed),
            "added": added,
            "modified": modified,
            "removed": removed
        }
