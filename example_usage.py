#!/usr/bin/env python3
"""
Example script for using ViPE to process videos for 3D reconstruction.

This script demonstrates basic usage of the ViPE tool for camera pose estimation
and dense depth map generation from video files.

Usage:
    python example_usage.py --video path/to/video.mp4
    python example_usage.py --video path/to/video.mp4 --pipeline dav3 --visualize
"""

import argparse
import subprocess
import sys
from pathlib import Path


def check_vipe_installed():
    """Check if ViPE is installed and accessible."""
    try:
        result = subprocess.run(
            ["vipe", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def process_video(video_path, output_dir="vipe_results", pipeline="default", visualize=False):
    """
    Process a video using ViPE.
    
    Args:
        video_path (str): Path to the input video file
        output_dir (str): Output directory for results
        pipeline (str): Pipeline configuration to use
        visualize (bool): Whether to enable visualization
    
    Returns:
        bool: True if processing was successful, False otherwise
    """
    video_path = Path(video_path)
    
    if not video_path.exists():
        print(f"Error: Video file not found: {video_path}")
        return False
    
    # Build the command
    cmd = ["vipe", "infer", str(video_path), "--output", output_dir, "--pipeline", pipeline]
    
    if visualize:
        cmd.append("--visualize")
    
    print(f"Processing video: {video_path}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        # Run ViPE inference
        result = subprocess.run(cmd, check=True)
        
        print("-" * 60)
        print(f"✓ Processing completed successfully!")
        print(f"Results saved to: {output_dir}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error during processing: {e}")
        return False


def visualize_results(results_dir):
    """
    Visualize ViPE results using the built-in visualizer.
    
    Args:
        results_dir (str): Directory containing ViPE results
    
    Returns:
        bool: True if visualization started successfully, False otherwise
    """
    results_path = Path(results_dir)
    
    if not results_path.exists():
        print(f"Error: Results directory not found: {results_path}")
        return False
    
    print(f"Launching visualizer for: {results_path}")
    print("This will open a web browser with interactive 3D visualization...")
    
    try:
        subprocess.run(["vipe", "visualize", str(results_path)], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during visualization: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Example script for processing videos with ViPE",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python example_usage.py --video my_video.mp4
  
  # Use Depth-Anything-V3 pipeline with visualization
  python example_usage.py --video my_video.mp4 --pipeline dav3 --visualize
  
  # Process with custom output directory
  python example_usage.py --video my_video.mp4 --output my_results
  
  # Just visualize existing results
  python example_usage.py --visualize-only --results vipe_results

Pipeline options:
  - default: Standard pipeline for pinhole cameras
  - dav3: Uses Depth-Anything-V3 (newest, recommended)
  - lyra: Configuration for Lyra paper results
  - no_vda: Less memory-intensive option
  - wide_angle: For wide-angle or fisheye videos
  - panorama: For 360° videos
        """
    )
    
    parser.add_argument(
        "--video",
        type=str,
        help="Path to input video file"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="vipe_results",
        help="Output directory for results (default: vipe_results)"
    )
    
    parser.add_argument(
        "--pipeline",
        type=str,
        default="default",
        choices=["default", "dav3", "lyra", "no_vda", "wide_angle", "panorama"],
        help="Pipeline configuration to use (default: default)"
    )
    
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Enable visualization during processing"
    )
    
    parser.add_argument(
        "--visualize-only",
        action="store_true",
        help="Only visualize existing results (skip processing)"
    )
    
    parser.add_argument(
        "--results",
        type=str,
        help="Results directory to visualize (use with --visualize-only)"
    )
    
    args = parser.parse_args()
    
    # Check if ViPE is installed
    if not check_vipe_installed():
        print("Error: ViPE is not installed or not in PATH!")
        print("\nPlease install ViPE first:")
        print("  1. Clone the repository: git clone https://github.com/nv-tlabs/vipe.git")
        print("  2. Install dependencies: pip install -r requirements.txt")
        print("  3. Install ViPE: cd vipe && pip install --no-build-isolation -e .")
        sys.exit(1)
    
    # Handle visualization-only mode
    if args.visualize_only:
        if not args.results:
            print("Error: --results must be specified when using --visualize-only")
            sys.exit(1)
        success = visualize_results(args.results)
        sys.exit(0 if success else 1)
    
    # Check if video path is provided
    if not args.video:
        print("Error: --video argument is required")
        parser.print_help()
        sys.exit(1)
    
    # Process the video
    success = process_video(
        args.video,
        args.output,
        args.pipeline,
        args.visualize
    )
    
    if not success:
        sys.exit(1)
    
    # Ask if user wants to visualize results
    if not args.visualize:
        response = input("\nWould you like to visualize the results now? (y/n): ")
        if response.lower() in ['y', 'yes']:
            visualize_results(args.output)
    
    print("\n✓ Done!")


if __name__ == "__main__":
    main()
