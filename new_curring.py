from functools import partial

custom_collate_fn = partial(custom_collate_fn, device=device, allowed_max_length=1024)	# 参数预填充pre-filled	# curring!!!