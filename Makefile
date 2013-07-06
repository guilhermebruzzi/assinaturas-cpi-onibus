root_dir		= $(realpath .)
src_dir			= ${root_dir}

help:
	@echo "Rode make mongo, make export, make import"

kill_mongo:
	@ps aux | awk '(/mongod/ && $$0 !~ /awk/){ system("kill -9 "$$2) }'

mongo: kill_mongo
	@rm -rf /tmp/assinatura_cpi/mongodata && mkdir -p /tmp/assinatura_cpi/mongodata
	@mongod --dbpath /tmp/assinatura_cpi/mongodata --logpath /tmp/assinatura_cpi/mongolog --port 7777 --quiet &

install:
	@pip install -r requirements.txt
	@pip install -r requirements-local.txt

clean:
	@find . -type f -name "*.pyc" -exec rm -rf {} \;

kill_run:
	@ps aux | awk '(make run && $$0 !~ /awk/){ system("kill -9 "$$2) }'

run: clean
	@python ${root_dir}/app.py

redis-server:
	@redis-server redis.conf

redis-cli:
	@redis-cli
