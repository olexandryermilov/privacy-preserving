DATA_ROOT=~/summarization_experiment/cnn_dm
CHECKPOINT_PATH="/dataset/c07bd62b/finetune_checkpoints"
SAVE_PATH=~/summarization_experiment/cnn_dm/finetune_checkpoints
DATESTR=$(date +"%m-%d-%H-%M")

source $1    # Model
source $2    # Task

NUM_WORKERS=1
NUM_GPUS_PER_WORKER=1
HOST_FILE_PATH="./hostfile"
MP_SIZE=1
MASTER_PORT=12345
TASK_NAME=cnn_dm
DATA_PATH=~/summarization_experiment/cnn_dm/
TRAIN_ARGS="--epochs 15 \
            --batch-size 8 \
            --lr 3e-5 \
            --lr-decay-style linear \
            --warmup 0.06 \
            --weight-decay 1.0e-1 \
            --label-smoothing 0.1"

COMMON_ARGS="--save-interval 10000 \
             --log-interval 50 \
             --eval-interval 1000 \
             --eval-iters 100"

TASK_ARGS="--src-seq-length 608 \
           --tgt-seq-length 160 \
           --min-tgt-length 55 \
           --length-penalty 0.7 \
           --no-repeat-ngram-size 3 \
           --num-beams 5 \
           --select-topk \
           --eval-batch-size 4"

OPTIONS_NCCL="NCCL_DEBUG=info NCCL_IB_DISABLE=0 NCCL_NET_GDR_LEVEL=2"
DISTRIBUTED_ARGS="${OPTIONS_NCCL} deepspeed --hostfile ${HOST_FILE_PATH} --master_port ${MASTER_PORT} --num_nodes ${NUM_WORKERS} --num_gpus ${NUM_GPUS_PER_WORKER}"

EXPERIMENT_NAME=${EXPERIMENT_NAME}_${DATESTR}
mkdir logs
run_cmd="${DISTRIBUTED_ARGS} finetune_glm.py \
       --deepspeed \
       --deepspeed_config config_tasks/config_blocklm_10B_cnndm.json \
       --finetune \
       --experiment-name ${EXPERIMENT_NAME} \
       --task ${TASK_NAME} \
       --data-dir ${DATA_PATH} \
       --save ${CHECKPOINT_PATH} \
       --checkpoint-activations \
       --num-workers 1 \
       --no-load-lr-scheduler \
       $MODEL_ARGS \
       $TRAIN_ARGS \
       $COMMON_ARGS \
       $TASK_ARGS \
       --fp16 \
       --model-parallel-size ${MP_SIZE} \
       --overwrite \
       2>&1 | tee logs/log-${EXPERIMENT_NAME}.txt"

echo ${run_cmd}
eval ${run_cmd}