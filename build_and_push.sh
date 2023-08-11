sudo docker build -t monitoring-station-backend .
sudo docker tag monitoring-station-backend connorcorso/monitoring-station-backend:latest
sudo docker push connorcorso/monitoring-station-backend:latest