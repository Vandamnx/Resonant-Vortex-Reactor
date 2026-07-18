#!/usr/bin/env python3
"""
Grok Project App
Main entry point for the Resonant Vortex Reactor / Gali-Spinal Tube tools.
"""

import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Grok - Resonant Vortex Reactor Tools")
    parser.add_argument("--sim", choices=["dashboard", "fluid", "torque", "nodes"], 
                        help="Run a specific simulation")
    parser.add_argument("--analyze", help="Analyze a CSV file from simulations")
    args = parser.parse_args()

    if args.sim == "dashboard":
        print("Running Full Multi-Test Dashboard...")
        # Import and run your dashboard script here
        from simulations.full_multi_test_dashboard_dmso_tree_sap import run_dashboard
        run_dashboard()
    elif args.sim == "fluid":
        print("Running Fluid Dynamics Simulation...")
        # Add import and call
    elif args.analyze:
        print(f"Analyzing CSV: {args.analyze}")
        # Add pandas analysis here
    else:
        print("Welcome to Grok Project Tools")
        print("Use --help for options")

if __name__ == "__main__":
    main()