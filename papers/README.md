vespa 立ち上げ
```
docker run --detach --name vespa --hostname vespa-container \
  --publish 8080:8080 --publish 19071:19071 \
  vespaengine/vespa
```
cd papers
```
cd papers
```
vespa application デプロイ
```
vespa deploy --wait 300
```
vespa データ投入
```
vespa feed ext/data.jsonl

```
