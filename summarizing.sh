cd ~/oleksandry
mkdir summarization_experiment
cd summarization_experiment
sudo apt install libopenmpi-dev
pip install mpi4py
git clone https://github.com/NVIDIA/apex
cd apex
pip install -v --disable-pip-version-check --no-cache-dir \
--global-option="--cpp_ext" --global-option="--cuda_ext" ./
#download my scripts
git clone https://github.com/olexandryermilov/privacy-preserving.git
pip install --upgrade pip
pip install transformers[torch]
pip install sentencepiece
#download data
pip install gdown
#gdown --id 0BwmD_VLjROrfTHk4NFg2SndKcjQ
#gdown --id 0BwmD_VLjROrfM1BxdkxVaTY2bWs
tar zxvf cnn_stories.tgz
tar zxvf dailymail_stories.tgz
git clone https://github.com/artmatsak/cnn-dailymail.git
python3 cnn-dailymail/make_datafiles.py cnn/stories dailymail/stories
#preprocess data
python3 privacy-preserving/ner_roberta.py cnn_dm
#download glm
git clone https://github.com/THUDM/GLM
cd GLM
#change ds_finetune in case I have my own dataset path
yes | cp -rf ../privacy-preserving/ds_finetune_seq2seq.sh ./scripts/
pip3 install torch
pip3 install deepspeed
pip3 install -r requirements.txt
#run training
bash scripts/ds_finetune_seq2seq.sh \
   config_tasks/model_blocklm_10B.sh \
   config_tasks/seq_cnndm_org.sh
bash scripts/evaluate_seq2seq.sh \
 ./runs/experiment_name/test.jsonl.hyps ./runs/experiment_name/test.jsonl.refs