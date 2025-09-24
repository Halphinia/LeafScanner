create a new folder called "model"

inside folder, run the following:

# Make sure git-lfs is installed (https://git-lfs.com)
git lfs install

git clone https://huggingface.co/microsoft/trocr-base-handwritten

# If you want to clone without large files - just their pointers

GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/microsoft/trocr-base-handwritten

# Make sure hf CLI is installed: pip install -U "huggingface_hub[cli]"
hf download microsoft/trocr-base-handwritten