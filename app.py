from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

# Veritabanı bağlantı bilgileri
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YeniSifre123!',  # Kendi root şifreni buraya yaz
    'database': 'elektrikli_arac',
    'cursorclass': pymysql.cursors.DictCursor
}

@app.route('/veri', methods=['GET'])
def get_data():
    try:
        return jsonify([
            {"tarih": "2025-07-01", "saat": "12:00:00", "deger": 35.2},
            {"tarih": "2025-07-01", "saat": "13:00:00", "deger": 36.1},
            {"tarih": "2025-07-01", "saat": "14:00:00", "deger": 34.9}
        ])
    except Exception as e:
        print(f"[HATA] {e}")
        return jsonify({'error': 'Sunucu hatası'}), 500

    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql = """
                SELECT tarih, saat, deger
                FROM veriler
                WHERE veri_tipi = %s
                AND CONCAT(tarih, ' ', saat) BETWEEN %s AND %s
                ORDER BY tarih, saat
            """
            cursor.execute(sql, (veri_tipi, start_date, end_date))
            result = cursor.fetchall()

            for row in result:
                if not isinstance(row['saat'], str):
                    row['saat'] = str(row['saat'])
                if not isinstance(row['tarih'], str):
                    row['tarih'] = row['tarih'].strftime('%Y-%m-%d')

        connection.close()
        return jsonify(result)
    except Exception as e:
        print(f"[HATA] {e}")
        return jsonify({'error': 'Sunucu hatası'}), 500


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
