out_dir = 'out-twitter-char'
eval_interval = 250
eval_iters = 200
log_interval = 10

always_save_checkpoint = False

dataset = 'twitter_char'
gradient_accumulation_steps = 1
batch_size = 12
block_size = 64

n_layer = 4
n_head = 4
n_embd = 128
dropout = 0.0

learning_rate = 1e-3
max_iters = 2000
lr_decay_iters = 2000
min_lr = 1e-4
beta2 = 0.99

warmup_iters = 100