#Mengimport modul Union dari typing untuk memberikan hint tipe data. 
from typing import Union
#Mengimport kelas FastAPI dari modul fastapi.
from fastapi import FastAPI

#Membuat instance FastAPI baru dengan nama app.
app = FastAPI()

#--------------------------------------------------------------------
# GET

#Mendefinisikan route untuk URL root menggunakan metode HTTP GET.
@app.get("/")
#Mendefinisikan fungsi read_root untuk menangani permintaan.
def read_root():
    #Mengembalikan sebuah kamus dengan kunci "Hello" dan 
    #nilai "World".
    return{"Hello" : "World"}

#Mendefinisikan rute "/mahasiswa/{npm}" menggunakan metode HTTP GET 
#untuk mengakses data.
@app.get("/mahasiswa/{npm}")
#Mendefinisikan sebuah fungsi bernama ambil_mhs yang mengambil 
#sebuah parameter string npm
def ambil_mhs(npm:str):
    #Mengembalikan sebuah kamus dengan kunci "nama" dan 
    #nilai "Talia Aprianti".
    return{"nama" : "Talia Aprianti"}

#Mendefinisikan rute "/mahasiswa2/" menggunakan metode HTTP GET 
#untuk mengakses data.
@app.get("/daftar_mhs/")
#Mendefinisikan fungsi daftar_mhs yang mengambil 
#dua parameter string, id_prov dan angkatan.
def daftar_mhs(id_prov:str,angkatan:str):
    #Mengembalikan sebuah kamus yang berisi query dan data mahasiswa.
    #Mendefinisikan string query dengan nilai id_prov dan angkatan.
    return{"query" :" idprov: {} ; angkatan: {}"
        #Contoh data mahasiswa lainnya dengan NPM "1234".
        .format(id_prov,angkatan),
        "data":[{"npm":"1234"}, {"npm":"1234"}]}

#--------------------------------------------------------------------
# POST

#Mengimpor modul sqlite3 untuk melakukan operasi database SQLite.
import sqlite3 

#Mendefinisikan rute untuk "/init/" menggunakan metode HTTP GET.
@app.get("/init/") 
#Mendefinisikan fungsi init_db yang menginisialisasi database. 
def init_db():
    #Memulai blok try untuk menangkap potensi exception.
    try:
        #Mendefinisikan nama database SQLite.
        DB_NAME = "upi.db"
        #Membuat koneksi ke database SQLite.
        con = sqlite3.connect(DB_NAME)
        #Membuat objek kursor untuk menjalankan perintah SQL.
        cur = con.cursor()
        
        #Mendefinisikan perintah SQL untuk membuat tabel mahasiswa.
        create_table = """
        CREATE TABLE mahasiswa (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            nim TEXT NOT NULL,
            nama TEXT NOT NULL,
            id_prov TEXT NOT NULL,
            angkatan TEXT NOT NULL,
            tinggi_badan INTEGER
        )
        """
        #Menjalankan perintah SQL untuk membuat tabel.
        cur.execute(create_table)
        #Melakukan commit untuk menyimpan perubahan ke database.
        con.commit()
    
    #Menangkap exception jika terjadi kesalahan.
    except:
        #Mengembalikan pesan error jika terjadi kesalahan.
        return {"status": "Terjadi error"}  
    
    #Blok finally untuk menutup koneksi database.
    finally:
        #Menutup koneksi database setelah selesai.
        con.close() 
    #Mengembalikan pesan sukses jika tabel berhasil dibuat.
    return {"status": "OK, database dan tabel berhasil dibuat"}

#Impor kelas BaseModel dari modul pydantic untuk mendefinisikan 
#model data dengan kemampuan validasi dan serialisasi.
from pydantic import BaseModel
#Menentukan model data bernama Mhs yang diwarisi dari BaseModel untuk 
#merepresentasikan struktur objek Mahasiswa (siswa).
class Mhs(BaseModel):
    #Menentukan bidang untuk kelas Mhs yang mewakili berbagai 
    #atribut dari seorang mahasiswa, seperti NPM, nama, ID provinsi, 
    #tahun masuk, dan tinggi badan. Field tinggi_badan bersifat opsional 
    #dengan nilai default Tidak Ada.
    npm: str
    nama: str
    id_prov: str
    angkatan: str
    tinggi_badan: int | None = None

#Menentukan rute untuk "/tambah_mhs/" menggunakan HTTP POST 
#untuk menangani penambahan mahasiswa baru.
@app.post("/tambah_mhs/")
#Mendefinisikan sebuah fungsi bernama tambah_mhs yang mengambil sebuah objek 
#bertipe Mhs (mewakili mahasiswa) sebagai parameter.
def tambah_mhs(m: Mhs):
    #Mulai blok try: untuk menangkap potensi pengecualian.
    try:
        #menentukan nama basis data SQLite.
        DB_NAME = "upi.db"
        #Membuat koneksi ke database SQLite.
        con = sqlite3.connect(DB_NAME)
        #Membuat objek kursor untuk menjalankan perintah SQL.
        cur = con.cursor()
        #menjalankan perintah SQL untuk menyisipkan record baru 
        #ke dalam tabel mahasiswa dengan menggunakan data dari 
        #objek Mhs yang telah disediakan.
        cur.execute("""insert into mahasiswa (nim,nama,id_prov,angkatan,tinggi_badan)
        values
        ( "{}","{}","{}","{}",{})""".format(m.npm,m.nama,m.id_prov,m.angkatan,
                                            m.tinggi_badan))
        #Komit transaksi untuk menyimpan perubahan ke database.
        con.commit()
    #Menangkap setiap pengecualian yang terjadi selama operasi database.
    except:
        #Mengembalikan kamus yang mengindikasikan kesalahan yang terjadi 
        #selama operasi basis data.
        return ({"status":"terjadi error"})
    #menjalankan blok kode ini terlepas dari apakah pengecualian terjadi 
    #untuk memastikan koneksi database ditutup.
    finally:
        #Tutup koneksi database.
        con.close()
    #Mengembalikkan sebuah kamus yang mengindikasikan keberhasilan 
    #dalam memasukkan satu record ke dalam database.
    return {"status":"ok berhasil insert satu record"}

#Mendefinisikan rute untuk "/tampilkan_semua_mhs/" menggunakan 
#metode HTTP GET untuk menampilkan semua mahasiswa.
@app.get("/tampilkan_semua_mhs/")
#Definisikan sebuah fungsi bernama tampil_semua_mhs untuk 
#menangani permintaan untuk menampilkan semua mahasiswa.
def tampil_semua_mhs():
    #Memulai blok try untuk menangkap potensi exception
    try:
        #Mendefinisikan nama database SQLite
        DB_NAME = "upi.db"
        #Membuat koneksi ke database SQLite
        con = sqlite3.connect(DB_NAME)
        #Membuat objek cursor untuk menjalankan perintah SQL
        cur = con.cursor()
        #Menginisialisasi sebuah list kosong untuk menyimpan 
        #data record
        recs = []
        #Mengulangi hasil dari query SQL untuk mengambil 
        #semua record dari tabel mahasiswa
        for row in cur.execute("select * from mahasiswa"):
            #Menambahkan setiap record ke dalam list
            recs.append(row)
    #Menangkap exception yang terjadi
    except:
        #Mengembalikan sebuah dictionary yang menunjukkan 
        #terjadi error
        return ({"status":"terjadi error"})
    #Menjalankan blok kode ini tanpa memperdulikan apakah 
    #terjadi exception atau tidak untuk memastikan koneksi 
    #database ditutup
    finally:
        #Menutup koneksi database
        con.close()
    #Mengembalikan sebuah dictionary yang berisi data 
    #record yang telah diambil
    return {"data":recs}

#--------------------------------------------------------------------
# PUT

#Mengimpor modul Response dari FastAPI untuk mengelola respons HTTP.
from fastapi import FastAPI, Response, Request, HTTPException
import sqlite3

#Mendefinisikan rute untuk update data mahasiswa menggunakan metode 
#PUT dengan path parameter nim dan mengembalikan objek Mhs sebagai respons.
@app.put("/update_mhs_put/{npm}", response_model=Mhs)
#Mendefinisikan fungsi update_mhs_put yang menerima objek Response, 
#nim (NPM mahasiswa yang akan diupdate), dan objek Mhs (data mahasiswa yang baru).
def update_mhs_put(response: Response, npm: str, m: Mhs):
    #Memulai blok try untuk menangkap potensi exception.
    try:
        #Mendefinisikan nama database SQLite.
        DB_NAME = "upi.db"
        #Membuat koneksi ke database SQLite.
        con = sqlite3.connect(DB_NAME)
        #Membuat objek cursor untuk menjalankan perintah SQL.
        cur = con.cursor()
        #Mendefinisikan query SQL untuk update data mahasiswa.
        sqlstr = "update mahasiswa set nama = ?, id_prov = ?, angkatan = ?, tinggi_badan = ? where nim = ?"
        #Menjalankan query SQL dengan menggunakan data yang diberikan.
        cur.execute(sqlstr, (m.nama, m.id_prov, m.angkatan, m.tinggi_badan, m.npm))
        #Melakukan commit untuk menyimpan perubahan ke database.
        con.commit()
        #Mengatur header location untuk respons HTTP.
        response.headers["location"] = "/mahasiswa/{}".format(m.npm)
    #Menangkap exception yang terjadi.
    except:
        #Mengembalikan sebuah dictionary yang menunjukkan terjadi error.
        return ({"status": "terjadi error"})
    #Menjalankan blok kode ini tanpa memperdulikan apakah terjadi 
    #exception atau tidak untuk memastikan koneksi database ditutup.
    finally:
        #Menutup koneksi database.
        con.close()
    #Mengembalikan objek Mhs yang telah diupdate.
    return m

#--------------------------------------------------------------------
# PATCH

#Mengimpor tipe data Optional untuk mendefinisikan nilai opsional
from typing import Optional

#Mendefinisikan atribut nama dengan tipe data str atau None,
#default value "kosong"
class MhsPatch(BaseModel):
    nama: str | None = "kosong"  
    #Mendefinisikan atribut id_prov dengan tipe data str atau None, 
    #default value "kosong"
    id_prov: str | None = "kosong"  
    #Mendefinisikan atribut angkatan dengan tipe data str atau None, 
    #default value "kosong"
    angkatan: str | None = "kosong"  
    #Mendefinisikan atribut tinggi_badan dengan tipe data int opsional 
    #atau None, default value -9999
    tinggi_badan: Optional[int] | None = -9999 

#Mendefinisikan rute untuk update data mahasiswa menggunakan metode PATCH 
#dan mengembalikan objek MhsPatch sebagai respons
@app.patch("/update_mhs_patch/{npm}", response_model=MhsPatch)
#Mendefinisikan fungsi untuk update data mahasiswa
def update_mhs_patch(response: Response, npm: str, m: MhsPatch):
    try:
        #Mencetak objek MhsPatch
        print(str(m)) 
        #Mendefinisikan nama database SQLite
        DB_NAME = "upi.db"
        #Membuat koneksi ke database SQLite
        con = sqlite3.connect(DB_NAME) 
        #Membuat objek cursor untuk menjalankan perintah SQL 
        cur = con.cursor()  
        #Menjalankan query SQL untuk mengambil data mahasiswa 
        #berdasarkan NPM
        cur.execute("select * from mahasiswa where nim = ?", (npm,))  
        #Mengambil hasil query pertama
        existing_item = cur.fetchone() 
    #Menangkap exception yang terjadi 
    except Exception as e:
        #Mengembalikan HTTPException dengan status code 500 
        #jika terjadi exception
        raise HTTPException(status_code=500, detail="Terjadi exception: {}"
        .format(str(e)))  

    #Memeriksa apakah item sudah ada di database   
    if existing_item: 
        #Mendefinisikan query SQL untuk update data mahasiswa
        sqlstr = "update mahasiswa set "  
        #Memeriksa apakah atribut nama pada objek MhsPatch bukan "kosong"
        if m.nama != "kosong": 
            #Memeriksa apakah atribut nama pada objek MhsPatch 
            #tidak bernilai None
            if m.nama != None: 
                #Menggabungkan atribut nama ke dalam query SQL
                sqlstr = sqlstr + " nama = '{}' ,".format(m.nama) 
            #Menggabungkan nilai NULL untuk atribut nama ke dalam query SQL 
            else:
                sqlstr = sqlstr + " nama = null ," 
        #Memeriksa apakah atribut angkatan pada objek MhsPatch bukan "kosong"
        if m.angkatan != "kosong": 
            #Memeriksa apakah atribut angkatan pada objek MhsPatch 
            #tidak bernilai None 
            if m.angkatan != None:
                #Menggabungkan atribut angkatan ke dalam query SQL
                sqlstr = sqlstr + " angkatan = '{}' ,".format(m.angkatan)
            #Menggabungkan nilai NULL untuk atribut angkatan 
            #ke dalam query SQL
            else:
                #Menggabungkan nilai NULL untuk atribut angkatan 
                #ke dalam query SQL
                sqlstr = sqlstr + " angkatan = null ,"

        #Memeriksa apakah atribut id_prov pada objek MhsPatch bukan "kosong"
        if m.id_prov != "kosong":  
            #Memeriksa apakah atribut id_prov pada objek MhsPatch tidak 
            #bernilai None
            if m.id_prov != None:
                #Menggabungkan atribut id_prov ke dalam query SQL
                sqlstr = sqlstr + " id_prov = '{}' ,".format(m.id_prov)
            #Menggabungkan nilai NULL untuk atribut id_prov 
            #ke dalam query SQL
            else:
                sqlstr = sqlstr + " id_prov = null, "
        #Memeriksa apakah atribut tinggi_badan pada objek MhsPatch 
        #bukan -9999
        if m.tinggi_badan != -9999: 
            #Memeriksa apakah atribut tinggi_badan pada objek MhsPatch 
            #tidak bernilai None
            if m.tinggi_badan != None:
                #Menggabungkan atribut tinggi_badan ke dalam query SQL
                sqlstr = sqlstr + " tinggi_badan = {} ,".format(m.tinggi_badan)
            #Menggabungkan nilai NULL untuk atribut tinggi_badan ke dalam 
            #query SQL
            else:
                sqlstr = sqlstr + " tinggi_badan = null ,"
        #Menghapus koma terakhir dari query SQL dan menambahkan 
        #kondisi WHERE berdasarkan NPM
        sqlstr = sqlstr[:-1] + " where nim='{}' ".format(npm)  
        #Mencetak query SQL yang akan dieksekusi
        print(sqlstr)  
        
        #Memulai blok try untuk menangkap potensi exception
        try:
            #Menjalankan query SQL untuk update data mahasiswa
            cur.execute(sqlstr)  
            #Melakukan commit untuk menyimpan perubahan ke database
            con.commit()  
            #Mengatur header location untuk respons HTTP
            response.headers["location"] = "/mahasiswa/{}".format(npm) 
        #Menangkap exception yang terjadi 
        except Exception as e:
            raise HTTPException(
            status_code=500, detail="Terjadi exception: {}"
            .format(str(e)))  
    #Jika tidak ada exception yang terjadi pada blok try sebelumnya          
    else:  
        #Mengembalikan HTTPException dengan status code 404 jika data 
        #mahasiswa tidak ditemukan
        raise HTTPException(status_code=404, 
        detail="Data mahasiswa dengan nim {} tidak ditemukan.".format(npm))  
    # Menutup koneksi database
    con.close()
    # Mengembalikan objek MhsPatch yang telah diupdate
    return m

#--------------------------------------------------------------------
# DELETE

#Mendefinisikan rute untuk menghapus data mahasiswa berdasarkan NPM
@app.delete("/delete_mhs/{npm}")  
#Mendefinisikan fungsi untuk menghapus data mahasiswa
def delete_mhs(npm: str):  
    #Memulai blok try untuk menangkap potensi exception
    try:  
       #Mendefinisikan nama database SQLite
       DB_NAME = "upi.db"  
       #Membuat koneksi ke database SQLite
       con = sqlite3.connect(DB_NAME)  
       #Membuat objek cursor untuk menjalankan perintah SQL
       cur = con.cursor()  
       #Mendefinisikan query SQL untuk menghapus data mahasiswa berdasarkan NPM
       sqlstr = "delete from mahasiswa  where nim='{}'".format(npm)  
       #Mencetak query SQL (untuk debugging)
       print(sqlstr)  
       #Menjalankan query SQL untuk menghapus data mahasiswa
       cur.execute(sqlstr)  
       #Melakukan commit untuk menyimpan perubahan ke database
       con.commit()  
     #Menangkap exception yang terjadi
    except: 
        #Mengembalikan pesan error jika terjadi exception
       return ({"status":"terjadi error"}) 
    #Blok finally akan selalu dieksekusi, digunakan untuk menutup koneksi database
    finally:  
       #Menutup koneksi database
       con.close()  
       #Mengembalikan status OK jika operasi penghapusan berhasil
    return {"status":"ok"}  

#--------------------------------------------------------------------
# POST AND GET IMAGE

#Mengimpor modul File dan UploadFile dari fastapi untuk mengelola file
from fastapi import File, UploadFile  
#Mengimpor modul FileResponse dari fastapi.responses untuk mengirim file sebagai response
from fastapi.responses import FileResponse  

#Mendefinisikan fungsi upload yang menerima file dengan tipe UploadFile
@app.post("/uploadimage")
def upload(file: UploadFile = File(...)):  
    #Memulai blok try untuk menangkap potensi exception
    try:  
        #Mencetak pesan "mulai upload" untuk debugging
        print("mulai upload") 
        #Mencetak nama file untuk debugging
        print(file.filename)  
        #Membaca isi file yang diunggah
        contents = file.file.read()  
        # Membuka file baru dengan nama yang sama di folder 'data_file'
        #untuk menyimpan file yang diunggah
        with open("data_file/" + file.filename, 'wb') as f:  
            #Menulis isi file yang diunggah ke file baru
            f.write(contents)  
    #Menangkap exception yang terjadi
    except Exception:  
        #Mengembalikan pesan error jika terjadi exception
        return {"message": "Error upload file"}  
    #Blok finally akan selalu dieksekusi, digunakan untuk menutup 
    #file yang diunggah
    finally:  
        #Menutup file yang diunggah
        file.file.close()  
    #Mengembalikan pesan sukses jika upload berhasil
    return {"message": "Upload berhasil: {file.filename}"}  

#Endpoint untuk mendapatkan gambar berdasarkan nama file
@app.get("/getimage/{nama_file}")
#Mendefinisikan fungsi getImage yang menerima nama_file sebagai parameter
async def getImage(nama_file: str):  
    #Mengembalikan FileResponse yang berisi file dengan nama yang 
    #diberikan dari folder 'data_file'
    return FileResponse("data_file/" + nama_file)  
