# Bot Shopee Affiliate
Sewa Bot Shopee Affiliate. Price: 50k/bulan
# Installation
```
$ apt update && apt upgrade
$ apt install python3 (skip aja kalo udh)
$ apt install python3-pip
$ apt install git
$ git clone https://github.com/revan-ar/shopee-affiliate
$ cd new-sopi-affiliate
$ python3 -m pip install python-dotenv
```
edit file **.env**, isi semuanya kecuali **AUTHORIZATION**. Untuk kategori produk, cek file **kategori.txt**

# .ENV
- SHOPEE = COOKIE SHOPEE AFFILIATE
- TWITTER = COOKIE TWITTER
- PRODUCT_CATEGORY = CEK FILE **kategori.txt**
- TOKEN = **x-csrf-token** TWITTER

# Termux
```
$ rm get_product.so
$ mv aarch64_get_product.so get_product.so 
```
# Running
```
$ python3 reply.py
```
