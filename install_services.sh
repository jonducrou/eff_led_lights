sudo cp effweb.service /lib/systemd/system
sudo chmod 644 /lib/systemd/system/effweb.service


sudo systemctl daemon-reload
sudo systemctl enable effweb.service
sudo systemctl start effweb.service

