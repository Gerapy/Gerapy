cat ./host | while read line
do
    echo "正在处理：${line}"
    ssh-copy-id -i ~/.ssh/id_rsa.pub -o StrictHostKeyChecking=no root@${line}    
done
