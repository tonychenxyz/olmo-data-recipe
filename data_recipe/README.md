# Generate training config files with uniform mixture weight sampling

```bash
python uniform_sample_configs.py \
    --categories category1 category2 category3 \
    --template path/to/template.yaml \
    --output-dir path/to/output/directory \
    --total-files 1000 \
    --root-data-dir path/to/data \
    --num-configs 5
```

Then run the training script with the generated config files:

```bash
torchrun --nproc_per_node=2 scripts/train.py configs/tiny/copy-OLMo-20M.yaml --no_pre_train_checkpoint
```