echo $(date)
mkdir ./log
export http_proxy=http://10.201.28.145:10808
export https_proxy=http://10.201.28.145:10808
day=20250818

for i in 3; do
python B6_ls_data_culc_sentiment.py ./data/data${i} ./para/para${i} > ./log/B6_${day}.log
echo "B6 over $(date)"
python B11_culc_text_vector.py ./data/data${i} ./para/para${i} > ./log/B11_${day}.log
done

echo $(date)

# nohup sh ./auto_run.sh > ./log/auto_run_${day}.log 2>&1 &
# jobs -l
# ps -p 1076 -f

# tar -czvf B6_culc_sentiment_prompt1.tar.gz sentiment.xlsx
# tar -czvf B11_culc_vector_prompt1.tar.gz text_vector.xlsx