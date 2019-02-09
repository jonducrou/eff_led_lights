sudo cp effweb.service /lib/systemd/system
sudo chmod 644 /lib/systemd/system/effweb.service

sudo cp efflight.service /lib/systemd/system
sudo chmod 644 /lib/systemd/system/efflight.service


sudo systemctl daemon-reload
sudo systemctl enable efflight.service
sudo systemctl start efflight.service

