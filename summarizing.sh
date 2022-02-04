cd ~/
mkdir summarization_experiment
cd summarization_experiment
#download my scripts
git clone https://github.com/olexandryermilov/privacy-preserving.git
pip install --upgrade pip
pip install transformers[torch]
pip install sentencepiece
#download data
pip install gdown
gdown --id 0BwmD_VLjROrfTTljRDVZMFJnVWM
gdown --id 0BwmD_VLjROrfM1BxdkxVaTY2bWs
tar zxvf cnn_stories.tgz
tar zxvf dailymail_stories.tgz
git clone https://github.com/artmatsak/cnn-dailymail.git
python3 cnn-dailymail/make_datafiles.py cnn/stories dailymail/stories
#preprocess data
python3 privacy-preserving/ner_1.py cnn_dm
#download glm
git clone https://github.com/THUDM/GLM
cd GLM
#change ds_finetune in case I have my own dataset path
yes | cp -rf ../privacy-preserving/ds_finetune_seq2seq.sh ./scripts/
pip install pytorch
pip install requirements.txt
#run training
bash scripts/ds_finetune_seq2seq.sh \
   config_tasks/model_blocklm_10B.sh \
   config_tasks/seq_cnndm_org.sh