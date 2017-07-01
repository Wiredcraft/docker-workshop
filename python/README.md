## Example

Create virtualenv

```
virtualenv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

## Prepare redis

```
docker pull redis:alpine
```

## No persistant storage

### Spawn redis

```
docker run -d --rm -p 6379:6379 --name redis redis
```

### Run the code

```
shell> python script.py
before: 0
after: 1

shell> python script.py
before: 1
after: 1
```

### Remove container + restart container

```
docker stop redis

docker run -d --rm -p 6379:6379 --name redis redis
```

### Re-run the code

```
# Note as before is still 0
shell> python script.py
before: 0
after: 1

shell> python script.py
before: 1
after: 1
```

### Cleanup

```
docker stop redis
```

## With persistant storage

### Spawn redis

```
docker run -d --rm -p 6379:6379 --name redis -v $(pwd)/storage:/data redis --appendonly yes
```

### Run the code

```
shell> python script.py
before: 0
after: 1

shell> python script.py
before: 1
after: 1
```

### Remove container + restart container

```
docker stop redis

docker run -d --rm -p 6379:6379 --name redis -v $(pwd)/storage:/data redis --appendonly yes
```

### Re-run the code

```
# Note as before is now
shell> python script.py
before: 1
after: 1

shell> python script.py
before: 1
after: 1
```

### Cleanup

```
docker stop redis

