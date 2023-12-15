from flask import Flask, render_template, request, redirect, url_for
import mysql.connector as mysql

app = Flask(__name__)
app.secret_key = '1234'

#connect to DB
db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    db = "responsi",
)

@app.route ("/", methods=['GET'])
def dataMahasiswa():
    cursor = db.cursor()
    query = ("SELECT * FROM mahasiswa")
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return render_template('index.html', mahasiswa=data)

@app.route('/form', methods=['GET', 'POST'])
def formMahasiswa():
    if request.method == 'POST':
        inpNama = request.form['nama']
        inpProdi = request.form['prodi']
        inpTahunMasuk = request.form['tahun_masuk']
        inpAlamat = request.form['alamat']

        cursor = db.cursor()
        query = "INSERT INTO mahasiswa VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(query,('',inpNama,inpProdi,inpTahunMasuk,inpAlamat))

        db.commit()
        cursor.close()
        return redirect(url_for('dataMahasiswa'))
    
    else:
        return render_template('form.html')

@app.route("/update-mahasiswa-page", methods=['POST'])
def updateMahasiswaPage():
    nim = request.form['nim']
    nama = request.form['nama']
    prodi = request.form['prodi']
    tahun_masuk = request.form['tahun_masuk']
    alamat = request.form['alamat']
    return render_template("update.html", nim=nim, nama=nama, prodi=prodi, tahun_masuk=tahun_masuk, alamat=alamat)

@app.route("/update", methods=['POST'])
def updateMahasiswa():
    if request.method == 'POST':
        getNim = request.form['nim']
        updNama = request.form['nama']
        updProdi = request.form['prodi']
        updTahunMasuk = request.form['tahun_masuk']
        updAlamat = request.form['alamat']
        cursor = db.cursor()
        query = "UPDATE mahasiswa SET nama = %s, prodi = %s, tahun_masuk = %s, alamat = %s WHERE nim = %s"
        cursor.execute(query, (updNama, updProdi, updTahunMasuk, updAlamat, getNim))
        db.commit()
        cursor.close()
        return redirect(url_for("dataMahasiswa"))
    else:
        return render_template("update.html")

@app.route('/delete', methods=['GET', 'POST'])
def deleteMahasiswa():
    index = request.form["delete-nim"]
    cursor = db.cursor()
    query = "DELETE FROM mahasiswa WHERE nim=%s"
    cursor.execute(query,(index,))
    db.commit()
    return redirect(url_for("dataMahasiswa"))


if __name__ == "__main__" :
    app.run(debug=True)