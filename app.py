from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import _mysql_connector
import psycopg2
import psycopg2.extras

app = Flask(__name__)
CORS(app)

# Veritabanı bağlantı bilgileri
db_config = {
    'host': 'dpg-d1n3ng6mcj7s73bjqhog-a',
    'dbname': 'ev_postgres',
    'user': 'ev_postgres_user',
    'password': 'crJGKAzxdrCejo66A4cXry2kMl6WFrFZ', 
    'port': 5432
}

@app.route('/veri', methods=['GET'])
def get_data():
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        sql = """
            SELECT tarih, deger
            FROM veriler
            WHERE veri_tipi = 'batarya_isi'
            ORDER BY tarih
        """
        cur.execute(sql)
        rows = cur.fetchall()

        result = []
        for row in rows:
            result.append({
                'tarih': row['tarih'].strftime('%Y-%m-%d'),
                'saat': row['tarih'].strftime('%H:%M:%S'),
                'deger': row['deger']
            })

        cur.close()
        conn.close()
        return jsonify(result)

    except Exception as e:
        print(f"[HATA] {e}")
        return jsonify({'error': 'Sunucu hatası'}), 500
    
@app.route('/veri-ekle', methods=['GET'])
def veri_ekle():
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO veriler (veri_tipi, deger, tarih) VALUES
            ('batarya_isi', 35.2, '2025-07-01 10:00:00'),
            ('batteryVoltage', 13.5, '2025-07-01 10:01:00'),
            ('cellAvgVoltage', 3200.0, '2025-07-01 10:02:00'),
            ('chargingCurrent', 70.0, '2025-07-01 10:03:00'),
            ('hiz', 40.0, '2025-07-01 10:04:00')
        """)
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "✅ Veriler başarıyla eklendi"})
    except Exception as e:
        print(f"[HATA] {e}")
        return jsonify({'error': 'Veri ekleme hatası'}), 500


@app.route('/ozet', methods=['GET'])  # BU satır ve altı GET_DATA DIŞINDA olmalı
@app.route('/ozet', methods=['GET'])
def get_summary():
    try:
        return jsonify([
            {"veri_tipi": "batarya_isi", "deger": 35.2},
            {"veri_tipi": "hiz", "deger": 42.5}
        ])
    except Exception as e:
        print(f"[HATA] {e}")
        return jsonify({'error': 'Sunucu hatası'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
