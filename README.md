# 内分泌干扰物相关文章

内分泌干扰物（EDCs）相关文章 一个持续更新的专有领域知识库,聚焦内分泌干扰物（Endocrine Disrupting Chemicals）

网址：<https://single-cell-papers.bioinfo-assist.com/>

![](static/images/qrcode-website.png)

---

## 动机

本仓库从 [what-deep-learning-does-in-biomedicine](https://github.com/yanlinlin82/what-deep-learning-does-in-biomedicine/) 拷贝和修改而来。

## 如何使用

1. 克隆本仓库：

    ```sh
    git clone https://github.com/yanlinlin82/single-cell-papers.git
    ```

2. 准备环境

    ```sh
    python -m venv .venv
    . .venv/bin/activate
    pip install -U -r requirements.txt
    ```

3. 配置环境参数

    ```sh
    vi .env
    ```


  
4. 初始化并运行Django

    ```sh
    python manage.py migrate
    python manage.py collectstatic
    ```

5. PubMed数据获取

    ```sh
    lftp -c "mirror -c https://ftp.ncbi.nlm.nih.gov/pubmed/" # 注意全套下载有超过50G
    ```

    PubMed数据每日更新，在相同目录中运行上述命令，即可自动增量下载

6. 扫描PubMed文件，提取文献信息，导入数据库

    ```sh
    python scripts/scan-pubmed.py /path/to/pubmed/updatefiles/pubmedXXnXXXX.xml.gz
    ```

    上述命令每次只导入一个`pubmedXXnXXXX.xml.gz`文件（通常含有上万篇文献）中的匹配关键词的文献信息。如果希望扫描并导入全部PubMed数据，则可以使用如下bash循环：

    ```sh
    find /path/to/pubmed/{baseline,updatefiles}/ -type f -name 'pubmed*.xml.gz' \
        | sort -r \
        | while read f; do
        python scripts/scan-pubmed.py "$f"
        sleep 1
    done
    ```

## 免责声明

本项目信息由手工或AI整理，信息难免存在错漏，请使用时务必注意核实。此外，由于各种原因，项目可能会不定期断档停更，还请见谅！

## 许可证

本仓库基于 [MIT协议](LICENSE) 发布，允许自由修改和传播。
