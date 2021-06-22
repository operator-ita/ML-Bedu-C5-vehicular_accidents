# Dockerize a simple flask proyect template

## 1. Build image and execute it 

Build the image
`root@europan-gt-spdb:~/Bedu-C5-vehicular_accidents#`
```bash
sudo docker build -t beduc5 .
``` 

## 2. Run image

Run image
```bash
sudo docker run -p 9000:8501  beduc5 
```

```bash
sudo docker run -p EXTERNAL_PORT:INTERNAL_PORT   beduc5 
sudo docker run -p 8090:8501  beduc5 
```


## 3. Visualice changes 


## 9. Get the IP for db instant  
docker inspect europan-dashboar