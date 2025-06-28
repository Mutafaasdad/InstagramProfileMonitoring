#!/data/data/com.termux/files/usr/bin/bash

echo "[✔] Güncellemeler yapılıyor..."
pkg update -y && pkg upgrade -y

echo "[✔] Python ve termux-api kuruluyor..."
pkg install -y python termux-api termux-widget curl -y

echo "[✔] pip güncelleniyor..."
pip install --upgrade pip

echo "[✔] Python modülü 'instaloader' kuruluyor..."
pip install instaloader

echo "[⬇] Python scripti indiriliyor..."
curl -o $HOME/InstagramProfileMonitoring.py https://raw.githubusercontent.com/Mutafaasdad/InstagramProfileMonitoring/refs/heads/main/InstagramProfileMonitoring.py

SHORTCUT_DIR="$HOME/.shortcuts"
SHORTCUT_FILE="$SHORTCUT_DIR/takipci-kontrol"

echo "[📁] .shortcuts klasörü kontrol ediliyor..."
mkdir -p "$SHORTCUT_DIR"

echo "[📝] Widget kısayol scripti oluşturuluyor..."
cat > "$SHORTCUT_FILE" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
cd \$HOME
python InstagramProfileMonitoring.py
EOF

chmod +x "$SHORTCUT_FILE"

echo ""
echo "✅ Kurulum tamamlandı!"
echo "📱 Ana ekranına Termux:Widget ekle, oradan 'takipci-kontrol' scriptine tıkla."
echo "🔁 Script çalışınca takip değişikliklerini izlemeye başlar."
