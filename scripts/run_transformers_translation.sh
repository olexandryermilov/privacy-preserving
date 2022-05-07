python3 ~/summarization_experiment/transformers/examples/pytorch/translation/run_translation.py \
    --model_name_or_path facebook/bart-base \
    --do_train \
    --do_predict \
    --source_lang en \
    --target_lang de \
    --source_prefix "translate English to Deutsch: " \
    --train_file ~/translation/train_placeholders_spacy_translation.json \
    --test_file ~/translation/newstest2015.json \
    --output_dir ./tst-translation-anon \
    --per_device_train_batch_size=8 \
    --per_device_eval_batch_size=8 \
    --predict_with_generate \
    --save_steps 1000 \
    --resume_from_checkpoint checkpoint-1660000

python3 ~/summarization_experiment/transformers/examples/pytorch/translation/run_translation.py \
    --model_name_or_path facebook/bart-base \
    --do_train \
    --do_predict \
    --source_lang en \
    --target_lang de \
    --source_prefix "translate English to Deutsch: " \
    --train_file ~/translation/train.json \
    --test_file ~/translation/newstest2015.json \
    --output_dir ./tst-translation-anon \
    --per_device_train_batch_size=8 \
    --per_device_eval_batch_size=8 \
    --predict_with_generate \
    --save_steps 20000 \
    --resume_from_checkpoint checkpoint-560000