# ViPE Demo - 3D Reconstruction Tool

This repository provides a complete setup and demonstration for using [ViPE (Video Pose Engine)](https://github.com/nv-tlabs/vipe), a powerful open-source spatial AI tool for annotating camera poses and dense depth maps from raw videos.

## About ViPE

ViPE is developed by NVIDIA and efficiently estimates:
- Camera intrinsics
- Camera motion
- Dense, near-metric depth maps from unconstrained raw videos

It supports diverse scenarios including dynamic selfie videos, cinematic shots, dashcams, and various camera models (pinhole, wide-angle, and 360° panoramas).

## Prerequisites

- **CUDA-capable GPU**: NVIDIA GPU with CUDA 12.8 support
- **Conda**: Anaconda or Miniconda installed
- **Git**: For cloning repositories

## Installation

Follow these steps to set up the ViPE environment:

### 1. Clone this Repository

```bash
git clone https://github.com/Michael89/vipe_demo.git
cd vipe_demo
```

### 2. Create Conda Environment

Create a new conda environment with all necessary dependencies:

```bash
conda env create -f environment.yml
conda activate vipe
```

### 3. Install Python Dependencies

Install the required Python packages with PyTorch CUDA support:

```bash
pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu128
```

### 4. Clone and Install ViPE

Clone the official ViPE repository and install it:

```bash
# Clone the ViPE repository
git clone https://github.com/nv-tlabs/vipe.git
cd vipe

# Install ViPE in editable mode
pip install --no-build-isolation -e .
cd ..
```

## Usage

### Basic Usage with CLI

Once installed, you can process videos using the `vipe` command:

```bash
# Process a video (replace YOUR_VIDEO.mp4 with your video file)
vipe infer YOUR_VIDEO.mp4
```

**Common Options:**
- `--output`: Specify output directory (default: `vipe_results`)
- `--visualize`: Enable visualization of results
- `--pipeline`: Choose pipeline configuration (default: `default`)

### Pipeline Configurations

ViPE supports several pipeline configurations:

- `default`: Standard pipeline for pinhole cameras
- `lyra`: Configuration for Lyra paper results
- `dav3`: Uses Depth-Anything-V3 model (newest)
- `no_vda`: Less memory-intensive, produces less temporally-stable but more 3D consistent depth maps
- `wide_angle`: For videos with wide-angle or fisheye distortion
- `panorama`: For 360° videos (available in panorama branch)

**Example:**

```bash
vipe infer my_video.mp4 --output my_results --visualize --pipeline dav3
```

### Visualizing Results

View the 3D reconstruction results using the built-in visualizer:

```bash
vipe visualize vipe_results/
```

This will launch an interactive visualization tool (powered by `viser`) in your browser.

### Advanced Usage with run.py

For more control and batch processing, use the `run.py` script:

```bash
# Navigate to the ViPE directory
cd vipe

# Run the full pipeline
python run.py pipeline=default streams=raw_mp4_stream streams.base_path=YOUR_VIDEO.mp4

# Run pose-only pipeline (without depth estimation)
python run.py pipeline=default streams=raw_mp4_stream streams.base_path=YOUR_VIDEO.mp4 pipeline.post.depth_align_model=null
```

### Converting to COLMAP Format

Convert ViPE results to COLMAP format for further processing:

```bash
cd vipe
python scripts/vipe_to_colmap.py ../vipe_results/ --sequence my_sequence

# For lightweight 3D consistent point cloud (requires full pipeline run with save_slam_map=true)
python scripts/vipe_to_colmap.py ../vipe_results/ --sequence my_sequence --use_slam_map
```

## Example Workflow

Here's a complete example workflow:

```bash
# 1. Activate the environment
conda activate vipe

# 2. Process your video
vipe infer my_video.mp4 --output my_results --visualize --pipeline dav3

# 3. View the results
vipe visualize my_results/

# 4. (Optional) Convert to COLMAP format
cd vipe
python scripts/vipe_to_colmap.py ../my_results/ --sequence my_video
```

## Downloading Pre-annotated Datasets

ViPE provides large-scale annotated datasets. To download:

```bash
cd vipe

# Download specific dataset (replace PREFIX with one below)
# - dpsp: Dynpose-100K++ (99,501 videos)
# - wsdg: Wild-SDG-1M (966,448 videos)
# - w360: Web360 (2,114 panoramic videos)

python scripts/download_dataset.py --prefix dpsp --output_base ./datasets --rgb --depth
```

**Note:** For Dynpose-100K++ RGB frames, install additional dependencies:
```bash
pip install yt_dlp ffmpeg-python
```

## Troubleshooting

### CUDA Out of Memory

If you encounter CUDA out of memory errors:
- Use the `no_vda` pipeline: `vipe infer video.mp4 --pipeline no_vda`
- Process shorter video clips
- Reduce video resolution

### Missing CUDA Libraries

If CUDA libraries are missing:
```bash
# Verify CUDA installation
nvidia-smi
nvcc --version

# Reinstall conda environment
conda env remove -n vipe
conda env create -f environment.yml
```

### Slow Processing

- Ensure you're using a CUDA-capable GPU
- Check GPU utilization: `nvidia-smi`
- Try a lighter pipeline configuration like `no_vda`

### Import Errors

If you get import errors after installation:
```bash
# Reinstall ViPE
cd vipe
pip install --no-build-isolation --force-reinstall -e .
```

## Resources

- **Official ViPE Repository**: https://github.com/nv-tlabs/vipe
- **Project Page**: https://research.nvidia.com/labs/toronto-ai/vipe
- **Technical Paper**: [ViPE Whitepaper](https://research.nvidia.com/labs/toronto-ai/vipe/assets/paper.pdf)
- **Datasets**: Available on [Hugging Face](https://huggingface.co/nvidia)

## License

ViPE is released under the Apache 2.0 License. This demo repository follows the same license. Note that ViPE downloads additional third-party models and software with their own licenses - review those before use.

## Citation

If you use ViPE in your research, please cite:

```bibtex
@inproceedings{huang2025vipe,
    title={ViPE: Video Pose Engine for 3D Geometric Perception},
    author={Huang, Jiahui and Zhou, Qunjie and Rabeti, Hesam and Korovko, Aleksandr and Ling, Huan and Ren, Xuanchi and Shen, Tianchang and Gao, Jun and Slepichev, Dmitry and Lin, Chen-Hsuan and Ren, Jiawei and Xie, Kevin and Biswas, Joydeep and Leal-Taixe, Laura and Fidler, Sanja},
    booktitle={NVIDIA Research Whitepapers arXiv:2508.10934},
    year={2025}
}
```

## Acknowledgments

ViPE is built on many open-source projects including DROID-SLAM, Depth Anything V2, Metric3Dv2, and others. See the [official repository](https://github.com/nv-tlabs/vipe) for full acknowledgments.
