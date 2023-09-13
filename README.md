Cara mengimplementasikan checklist:
1. Membuat sebuah proyek Django baru.
    Jalankan perintah "django-admin startproject <nama_proyek>" di direktori utama
2. Membuat aplikasi dengan nama main pada proyek tersebut.
    Jalankan perintah "python manage.py startapp main" di direktori utama
3. Melakukan routing pada proyek agar dapat menjalankan aplikasi main.
    Buka berkas urls.py di direktori proyek, lalu impor fungsi include dari django.urls
    dan tambahkan path('main/', include('main.urls')), pada variabel urlpatterns.
    Include digunakan untuk mengimpor rule URL dari main.urls dan path 'main/' akan
    diarahkan ke rute yang ada di urls.py aplikasi main
4. Membuat model pada aplikasi main dengan nama Item dan memiliki atribut wajib name, amount, description
    Buat kelas Item yang memiliki superclass models.Model yang diimport dari django.db
    dan setidaknya memiliki tiga atribut name, amount, dan description (saya tambahkan
    date_added dan price)
5. Membuat sebuah fungsi pada views.py untuk dikembalikan ke dalam sebuah template HTML yang menampilkan nama aplikasi serta nama dan kelas kamu.
    Di sini dibuat fungsi show_main(request) yang menerima parameter request dari HTTP dan mengembalikan tampilan yang sesuai.
    Fungsi tersebut akan mereturn render(request, "main.html", context) yang akan me-render tampilan dari main.html dengan data yang 
    ada dalam dictionary bernama context (seperti name, class, amount, dan description)
6. Membuat sebuah routing pada urls.py aplikasi main untuk memetakan fungsi yang telah dibuat pada views.py.
    Buat berkas urls.py di dalam direktori main untuk mengatur rute URL yang
    terkait dengan aplikasi main, lalu isi urls.py tersebut dengan:
    
    from django.urls import path
    from main.views import show_main // Untuk tampilan

    app_name = 'main'

    urlpatterns = [
        path('', show_main, name='show_main'),
    ]