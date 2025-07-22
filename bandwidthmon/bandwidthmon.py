#!/usr/bin/env python3

import psutil
import time

#Replace this with your active interface
ACTIVE_INTERFACE = "wlp1s0f0"

def bytes_to_mbps(bytes_val):
    """Convert bytes to megabits per second."""
    return (bytes_val * 8) / (1024 * 1024)

def monitor_bandwidth(interval=1):
    print("Monitoring bandwidth usage on {ACTIVE_INTERFACE} Press Ctrl+C to stop.")
    old_stats = psutil.net_io_counters(pernic=True)

    if ACTIVE_INTERFACE not in old_stats:
        print(f"Interface {ACTIVE_INTERFACE} not found.")
        return

    try:
        while True:
            time.sleep(interval)
            new_stats = psutil.net_io_counters(pernic=True)

            sent_diff = new_stats[ACTIVE_INTERFACE].bytes_sent - old_stats[ACTIVE_INTERFACE].bytes_sent
            recv_diff = new_stats[ACTIVE_INTERFACE].bytes_recv - old_stats[ACTIVE_INTERFACE].bytes_recv

            sent_mbps = bytes_to_mbps(sent_diff / interval)
            recv_mbps = bytes_to_mbps(recv_diff / interval)

            print(f" {recv_mbps:.2f} Mbps received, {sent_mbps:.2f} Mbps sent on {ACTIVE_INTERFACE}")
            print("-" * 30)

            old_stats = new_stats

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    monitor_bandwidth()
