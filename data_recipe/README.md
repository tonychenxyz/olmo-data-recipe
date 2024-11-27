# Generate training config files

This do random sampling of data mixture and generate olmo config files with corresponding data files

```bash
python uniform_sample_configs.py \
    --categories category1 category2 category3 \
    --template path/to/template.yaml \
    --output-dir path/to/output/directory \
    --total-files total number of training data files \
    --root-data-dir path/to/data \
    --num-configs 5
```

# Training
Then run the training script with the generated config files:

```bash
torchrun --nproc_per_node=2 scripts/train.py configs/tiny/copy-OLMo-20M.yaml --no_pre_train_checkpoint
```

# Outputs
- workspace/runname contains weight checkpoints
- workspace/runname/train_data/global_indices.npy contains pointers to training data (still figuring out how this works)

# TODO:
- Set up WandB
- Select right downstream eval in template yaml file

