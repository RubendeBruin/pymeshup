"""
Test script to verify that to_volume() doesn't modify the original workplane
"""
from pymeshup import STEP

# Replace with your actual STEP file path
filename = r"C:\data\gpsh0055rov.stp"

print("Loading STEP file...")
step = STEP(filename, scale=0.001)

# Get initial solid count
initial_solids = list(step._workplane.solids().vals())
initial_count = len(initial_solids)
print(f"Initial solid count: {initial_count}")

# Store the wrapped object IDs to check if they're the same objects
initial_ids = [id(s.wrapped) for s in initial_solids]
print(f"Initial wrapped object IDs: {initial_ids[:3]}...")

# Call to_volume multiple times
print("\nCalling to_volume() first time...")
volume1 = step.to_volume(angular_tolerance=0.1, linear_tolerance=1)

# Check if workplane was modified
after_solids = list(step._workplane.solids().vals())
after_count = len(after_solids)
after_ids = [id(s.wrapped) for s in after_solids]

print(f"After first to_volume() solid count: {after_count}")
print(f"After wrapped object IDs: {after_ids[:3]}...")

if initial_ids == after_ids:
    print("✓ Object IDs are the same - good!")
else:
    print("✗ Object IDs changed - workplane was modified!")

# Call to_volume again with different parameters
print("\nCalling to_volume() second time with different parameters...")
volume2 = step.to_volume(angular_tolerance=0.5, linear_tolerance=2)

final_solids = list(step._workplane.solids().vals())
final_count = len(final_solids)
final_ids = [id(s.wrapped) for s in final_solids]

print(f"After second to_volume() solid count: {final_count}")
print(f"Final wrapped object IDs: {final_ids[:3]}...")

if initial_ids == final_ids:
    print("✓ Object IDs are still the same - workplane not modified!")
else:
    print("✗ Object IDs changed - workplane was modified!")

# Summary
if initial_count == after_count == final_count and initial_ids == after_ids == final_ids:
    print("\n✓✓✓ SUCCESS: Original workplane was not modified! ✓✓✓")
else:
    print("\n✗✗✗ FAILURE: Original workplane was modified! ✗✗✗")

