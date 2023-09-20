# Tugas 3

## Membuat input form untuk menambahkan objek model pada app sebelumnya.
1. Buat berkas baru pada direktori main dengan nama forms.py untuk membuat struktur form yang dapat menerima data item baru. Tambahkan kode berikut ke dalam berkas forms.py.
```
from django.forms import ModelForm
from main.models import Item

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["name", "amount", "description"]
```
2. Menambahkan fungsi import berikut ke views.py di main
```
from django.http import HttpResponseRedirect
from main.forms import ProductForm
from django.urls import reverse
```
3. Buat fungsi create_product di views.py yang menerima parameter request untuk menambah item secara otomatis ketika di-submit
```
def create_product(request):
    form = ItemForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "create_product.html", context)
```
4. Ubah fungsi show_main yang sudah ada pada berkas views.py
```
def show_main(request):
    items = Item.objects.all()
    context = {
        'name': 'Daffa Al Fathan Zaki',
        'class': 'PBP A',
        'items': items,
    }

    return render(request, "main.html", context)
```
Fungsi Item.objects.all() digunakan untuk mengambil seluruh object Item yang tersimpan pada database.

5. Import fungsi create_product dan tambahkan path url ke urlpatterns di urls.py di main
```
from main.views import show_main, create_product
```
```
path('create-product', create_product, name='create_product'),
```

6. Buat berkas HTML baru dengan nama create_product.html pada direktori main/templates untuk membuat tampilan form saat user menginput data baru
```
{% extends 'base.html' %} 

{% block content %}
<h1>Add New Item</h1>

<form method="POST">
    {% csrf_token %}
    <table>
        {{ form.as_table }}
        <tr>
            <td></td>
            <td>
                <input type="submit" value="Add Item"/>
            </td>
        </tr>
    </table>
</form>

{% endblock %}
```

## Melihat objek yang sudah ditambahkan dalam format HTML, XML, JSON, XML by ID, dan JSON by ID.
**HTML**
Modifikasi main.html dalam block content agar bisa menampilkan data baru
```
<table>
    <tr>
        <th>Name</th>
        <th>Amount</th>
        <th>Description</th>
        <th>Date Added</th>
    </tr>

    {% comment %} Berikut cara memperlihatkan data produk di bawah baris ini {% endcomment %}

    {% for item in items %}
        <tr>
            <td>{{item.name}}</td>
            <td>{{item.amount}}</td>
            <td>{{item.description}}</td>
            <td>{{item.date_added}}</td>
        </tr>
    {% endfor %}
</table>

<br />

<a href="{% url 'main:create_product' %}">
    <button>
        Add New Item
    </button>
</a>
```

**XML dan JSON**
Tambahkan fungsi show_xml dan show_json di views.py di main yang masing-masing akan mereturn HTTPResponse menjadi XML/JSON
```
def show_xml(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
```

**XML by ID dan JSON by ID**
Tambahkan fungsi show_xml_by_id dan show_json_by_id di views.py di main yang masing-masing akan mereturn HTTPResponse menjadi XML/JSON tetapi hanya salah satu ID
```
def show_xml_by_id(request, id):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
```

**Menambah path masing-masing fungsi di urls.py di main**
```
from django.urls import path
from main.views import show_main, create_product, show_xml, show_json, show_xml_by_id, show_json_by_id

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-product', create_product, name='create_product'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
]
```
## Perbedaan antara form POST dan form GET dalam Django
Dalam Django, seperti dalam web development pada umumnya, terdapat dua metode HTTP yang umum digunakan untuk mengirim data dari sebuah form ke server: POST dan GET. Berikut adalah perbedaan utama antara keduanya:

1. Metode HTTP:
   - **POST**: Ini adalah metode HTTP yang digunakan untuk mengirim data ke server. Data yang dikirimkan melalui metode POST tidak akan terlihat di URL, sehingga lebih aman untuk data sensitif seperti kata sandi. Metode ini digunakan saat Anda ingin mengirim data yang akan mengubah sesuatu di server, seperti menambahkan data ke database atau melakukan aksi yang lain yang memodifikasi data di server.
   - **GET**: Ini adalah metode HTTP yang digunakan untuk mengambil data dari server. Data yang dikirimkan melalui metode GET akan muncul di URL dan dapat dilihat oleh siapa saja yang melihatnya. Metode ini digunakan saat Anda ingin mengambil data dari server tanpa melakukan perubahan pada server. Misalnya, ketika Anda melakukan pencarian di situs web atau mengakses halaman dengan parameter tertentu.

2. Keamanan:
   - **POST**: Lebih aman untuk mengirim data sensitif karena data tidak terlihat di URL. Ini membuatnya cocok untuk operasi-operasi yang melibatkan perubahan data atau aksi yang memerlukan otentikasi.
   - **GET**: Kurang aman karena data ditampilkan di URL dan dapat dengan mudah dilihat oleh siapa saja yang melihatnya. Oleh karena itu, tidak dianjurkan untuk mengirim data sensitif melalui metode GET.

3. Kapasitas Data:
   - **POST**: Tidak ada batasan kapasitas data yang ketat pada metode POST. Anda dapat mengirim data yang cukup besar melalui metode ini.
   - **GET**: Terdapat batasan kapasitas data yang lebih ketat pada metode GET. Beberapa browser dan server dapat memiliki batasan pada panjang URL, sehingga tidak cocok untuk mengirim data yang sangat besar.

4. Bookmarking:
   - **POST**: Tidak cocok untuk membuat bookmark atau meng-share URL dengan data tertentu karena data tidak terlihat di URL.
   - **GET**: Cocok untuk membuat bookmark atau meng-share URL dengan data tertentu karena data ditampilkan di URL dan dapat digunakan untuk mengakses halaman dengan parameter yang sama.

Dalam pengembangan web dengan Django, Anda dapat menggunakan metode POST atau GET sesuai dengan kebutuhan aplikasi Anda. Biasanya, form yang digunakan untuk mengirim data sensitif atau melakukan perubahan pada server akan menggunakan metode POST, sementara form yang digunakan untuk pencarian atau mengambil data dari server akan menggunakan metode GET.

## Perbedaan utama antara XML, JSON, dan HTML dalam konteks pengiriman data
XML, JSON, dan HTML adalah tiga format yang berbeda yang digunakan untuk mengirim data dalam konteks pengembangan web dan komunikasi data. Berikut adalah perbedaan utama antara ketiganya:

1. **XML (eXtensible Markup Language)**:
   - **Tujuan Utama**: XML digunakan untuk merepresentasikan dan mengirimkan data dalam format teks yang dapat dibaca oleh manusia dan mesin. Ini sering digunakan dalam pertukaran data antara aplikasi yang berbeda.
   - **Struktur**: XML menggunakan markup tags yang mendefinisikan struktur data hierarkis. Ini memungkinkan definisi yang sangat kustom dan lebih kompleks daripada JSON atau HTML.
   - **Penggunaan Umum**: XML sering digunakan dalam protokol seperti SOAP (Simple Object Access Protocol) untuk layanan web, konfigurasi berkas, dan pertukaran data yang memerlukan struktur yang sangat terperinci.

2. **JSON (JavaScript Object Notation)**:
   - **Tujuan Utama**: JSON digunakan untuk merepresentasikan data dalam format ringkas dan ringan yang mudah dibaca oleh manusia dan diuraikan oleh mesin. JSON umumnya digunakan dalam pengembangan web dan pertukaran data antara klien dan server dalam format yang lebih ringkas daripada XML.
   - **Struktur**: JSON menggunakan pasangan "nama-nilai" (key-value pairs) yang mendefinisikan objek dan daftar (arrays) untuk struktur data. Formatnya lebih sederhana dibandingkan XML.
   - **Penggunaan Umum**: JSON digunakan dalam pertukaran data API, konfigurasi, menyimpan pengaturan pada berkas konfigurasi JavaScript, dan dalam banyak aplikasi web modern.

3. **HTML (Hypertext Markup Language)**:
   - **Tujuan Utama**: HTML digunakan untuk membuat halaman web yang dapat ditampilkan di peramban web. Ini bukan format pertukaran data, tetapi format yang digunakan untuk mengatur dan menampilkan konten web.
   - **Struktur**: HTML menggunakan markup tags yang mendefinisikan struktur konten web, seperti teks, gambar, tautan, dan elemen lainnya yang dibutuhkan dalam halaman web.
   - **Penggunaan Umum**: HTML digunakan untuk membuat halaman web, memformat konten, menampilkan gambar, membuat formulir, dan memfasilitasi interaksi antara pengguna dan aplikasi web.

Perbedaan utama antara ketiga format ini terletak pada tujuan penggunaan, struktur, dan cara data diwakili. XML lebih kompleks dan sering digunakan untuk pertukaran data yang sangat struktural, JSON lebih ringkas dan umumnya digunakan dalam pengembangan web, sementara HTML digunakan untuk membuat halaman web. Pilihan format tergantung pada kebutuhan spesifik dan konteks penggunaannya dalam pengembangan perangkat lunak dan komunikasi data.

## Alasan JSON sering digunakan dalam pertukaran data antara aplikasi web modern
JSON (JavaScript Object Notation) sering digunakan dalam pertukaran data antara aplikasi web modern karena memiliki beberapa keunggulan yang membuatnya sangat cocok untuk keperluan tersebut:

1. **Ringkas dan Mudah Dibaca**: JSON memiliki format yang ringkas dan mudah dibaca oleh manusia. Struktur data JSON menggunakan pasangan "nama-nilai" (key-value pairs) yang serupa dengan struktur data dalam bahasa pemrograman. Ini membuatnya lebih mudah untuk dimengerti dan diuraikan oleh manusia.

2. **Ringan**: JSON adalah format data yang ringan dalam arti bahwa penggunaan karakter dalam format ini minim. Hal ini mengurangi penggunaan bandwidth dan meningkatkan kecepatan pertukaran data antara klien dan server. Hal ini sangat penting untuk aplikasi web yang berfokus pada kinerja.

3. **Parsial Parsing**: JSON memungkinkan parsial parsing, yang berarti klien dapat mengambil hanya bagian-bagian tertentu dari data yang diberikan oleh server. Ini mengurangi beban pada jaringan dan memungkinkan aplikasi web untuk menjadi lebih responsif.

4. **Dukungan oleh Banyak Bahasa Pemrograman**: JSON didukung oleh sebagian besar bahasa pemrograman, baik dalam hal pembuatan data JSON maupun parsing data JSON. Hal ini membuatnya sangat serbaguna untuk pertukaran data antara berbagai bahasa pemrograman.

5. **Kompatibilitas dengan JavaScript**: Karena JSON memiliki asal-usulnya dalam JavaScript, itu bekerja dengan sangat baik dengan JavaScript, yang merupakan bahasa pemrograman yang dominan dalam pengembangan web modern. Hal ini memungkinkan penggunaan yang mudah dalam aplikasi web yang berbasis JavaScript.

6. **Dukungan oleh Banyak API**: Banyak layanan web dan API modern menggunakan JSON sebagai format pertukaran data mereka. Ini membuatnya lebih mudah untuk mengintegrasikan aplikasi dengan layanan-layanan pihak ketiga dan mengambil data dari mereka.

7. **Kemampuan untuk Merepresentasikan Struktur Data yang Kompleks**: JSON mendukung representasi struktur data yang kompleks, termasuk objek bersarang dan larik (arrays), sehingga cocok untuk mewakili berbagai jenis data.

8. **Mendukung Tipe Data Primitif**: JSON mendukung tipe data primitif seperti string, angka, boolean, null, dan objek. Ini memungkinkan representasi yang fleksibel dari berbagai jenis data.

Kesimpulannya, JSON adalah format pertukaran data yang populer dalam aplikasi web modern karena ringkas, ringan, mudah dibaca, dan memiliki dukungan luas di berbagai bahasa pemrograman. Keunggulan-keunggulannya ini membuatnya menjadi pilihan yang kuat untuk komunikasi antara klien dan server dalam konteks pengembangan web.

## Postman
1. HTML
![](./Tugas%202/html.png)

2. XML
![](./Tugas%202/xml.png)

3. JSON
![](./Tugas%202/json.png)

4. XML by ID
![](./Tugas%202/xml_by_id.png)

5. JSON by ID
![](./Tugas%202/json_by_id.png)

# Tugas 2

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


![](./Tugas%202/models.py.png "Bagan Django")

Virtual environment digunakan untuk mengisolasi package serta dependencies dari aplikasi sehingga tidak bertabrakan dengan proyek-proyek lain yang ada pada komputer. Kita tetap dapat membuat aplikasi web berbasis Django tanpa menggunakan virtual environment namun hal ini beresiko karena terpengaruh dependensi dari proyek-proyek lainnya.

MVC (Model-View-Controller) memisahkan Model dengan View dan Controller, pengembangan Model tidak mempengaruhi tampilan dan sebaliknya juga berlaku. MVT (Model-View-Template) menggunakan Template untuk mengatur tampilan dan presentasi data. MVVM (Model-View-ViewModel) digunakan dalam pengembangan aplikasi berbasis klien (JavaScript) karena memungkinkan pengembangan tampilan yang lebih dinamis dan reaktif.
