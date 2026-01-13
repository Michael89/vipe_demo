# Quick Start Guide

This is a quick reference for getting started with ViPE.

## 1. Install (One-time Setup)

```bash
# Create and activate conda environment
conda env create -f environment.yml
conda activate vipe

# Install Python dependencies
pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu128

# Clone and install ViPE
git clone https://github.com/nv-tlabs/vipe.git
cd vipe
pip install --no-build-isolation -e .
cd ..
```

## 2. Process a Video

### Option A: Using the Example Script (Recommended for beginners)

```bash
python example_usage.py --video your_video.mp4 --pipeline dav3
```

### Option B: Using ViPE CLI Directly

```bash
vipe infer your_video.mp4 --output results --pipeline dav3
```

## 3. Visualize Results

```bash
vipe visualize results/
```

This opens an interactive 3D viewer in your browser.

## Common Pipelines

- `default` - Standard pinhole camera (good starting point)
- `dav3` - Best quality, uses Depth-Anything-V3 (recommended)
- `no_vda` - Lower memory usage, faster processing
- `wide_angle` - For wide-angle/fisheye lenses
- `panorama` - For 360° videos

## Tips

1. **Start small**: Test with a short video clip first
2. **GPU memory**: If you get OOM errors, use `no_vda` pipeline
3. **Video format**: MP4, AVI, MOV are all supported
4. **Output**: Results are saved with camera poses and depth maps

## Need Help?

See the full README.md for detailed documentation and troubleshooting.
