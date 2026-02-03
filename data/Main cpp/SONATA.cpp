#include <iostream>
#include <string>
#include <iomanip>
#include <fstream>
#include <vector>
#include <map>
#include <sstream>
using namespace std;

class Daftar{
    public:
        string nama;
        vector<string> list_kelas = {"Progressive", "Rock", "Pop", "Blues"};
        vector<string> list_alat  = {"Gitar", "Drum", "Bass", "Keyboard/Piano"};
        int umur;
        string lahir;
};

class Guru{
    protected:
        vector<long> listGaji;

    public:
        map<string, string> relasiGuru;
        map<string, string> spesialisAlat;

        Guru(){
            relasiGuru["Progressive"] = "Dr.Ir.Falan, S.Kom.,M.M.,Ph.D";
            relasiGuru["Pop"]         = "Yurika, S.Ikom";
            relasiGuru["Blues"]       = "Ernest, S.T., M.Sn";
            relasiGuru["Rock"]        = "Ir. Arraya Bey, S.Pd";

            spesialisAlat["Dr.Ir.Falan, S.Kom.,M.M.,Ph.D"] = "Drum";
            spesialisAlat["Yurika, S.Ikom"]               = "Keyboard/Piano";
            spesialisAlat["Ernest, S.T., M.Sn"]           = "Gitar";
            spesialisAlat["Ir. Arraya Bey, S.Pd"]         = "Bass";
        }
    
    void Guru_SMS(){
        listGaji = {3500000,1250000,5000000,2300000};
    }
};

class pilih_Guru: public Guru{
    public:
        string guruTerpilih;
        void pilihanGuru(string namaKelas){
            cout << string(40, '-') << endl;
            if (relasiGuru.count(namaKelas)) {
            guruTerpilih = relasiGuru[namaKelas];
            cout << "Guru yang tersedia untuk kelas " << namaKelas << ":" << endl;
            cout << ">> " << guruTerpilih << " (Spesialis: " << spesialisAlat[guruTerpilih] << ")" << endl;
        } else {
            cout << "Maaf, belum ada guru untuk kelas tersebut.\n";
        }
        cout << string(40, '-') << endl;
        }
};

void Pendaftaran();

void Riwayat_Guru();

void Tentang_Kami();

void Murid_SMS();

int main(){
    int pilih;

    do{
        system("cls");
        cout << "\n=======================================================================\n";
        cout << "                       SONATA MUSIC SCHOOL SYSTEM                          ";
        cout << "\n=======================================================================\n";
        cout << "1. Pendaftaran\n";
        cout << "2. Riwayat Guru\n";
        cout << "3. Tentang Kami\n";
        cout << "4. Murid Sonata Music School\n";
        cout << "5. Keluar Sistem\n";
        cout << string(60, '-') << endl;
        cout << "Pilihan anda (1-4) : "; cin >> pilih;

        if (!(pilih)) {
            cin.clear();
            cin.ignore(1000, '\n');
            continue;
        }

        switch (pilih){
            case 1 : {
                Pendaftaran();
                break;
            }
            case 2 : {
                Riwayat_Guru();
                break;
            }
            case 3 : {
                Tentang_Kami();
                break;
            }
            case 4 : {
                Murid_SMS();
                break;
            }
            case 5 : {
                cout << "\nTerima Kasih telah mengunjungi SONATA MUSIC SCHOOL!\n";
                break;
            }
            default : {
                cout << "\nPilihan anda tidak valid!\n";
                system("pause");
            }    
        }
    }while(pilih != 5);
}

void Pendaftaran(){
    ofstream file ("Data_murid_baru.txt", ios::app);
    Daftar muridBaru;
    pilih_Guru sistemGuru;
    int n,y;

    system("cls");
    cout << "\n      ===== Pilihan Kelas =====       \n";
    for (int i = 0; i < muridBaru.list_kelas.size(); i++) {
        cout << i + 1 << ". " << muridBaru.list_kelas[i] << endl;
    }

    cout << "\nInput Pilihan Kelas (1-4): "; cin >> n;
    if (n < 1 || n > 4) return;
    
    string kelasDiambil = muridBaru.list_kelas[n-1];

    sistemGuru.pilihanGuru(kelasDiambil);

    cin.ignore();
    cout << left << setw(20) << "Nama Murid" << " : "; getline(cin, muridBaru.nama);
    cout << left << setw(20) << "Umur" << " : "; cin >> muridBaru.umur;
    cin.ignore();
    cout << left << setw(20) << "Tanggal Lahir" << " : "; getline(cin, muridBaru.lahir);

    // Simpan ke file
    if (file.is_open()) {
        file << muridBaru.nama << "|" 
             << kelasDiambil << "|" 
             << sistemGuru.guruTerpilih << "|" // Terisi otomatis lewat Map
             << muridBaru.umur << "|" 
             << muridBaru.lahir << endl;
        file.close();
        cout << "\nPendaftaran Berhasil!\n";
    }
    system("pause");
}

void Riwayat_Guru() {
    Guru guru_SMS;
    system("cls");
    cout << "============================================================" << endl;
    cout << "                DAFTAR RELASI GURU & KELAS                  " << endl;
    cout << "============================================================" << endl;
    cout << left << setw(20) << "KATEGORI KELAS" << " | " << "NAMA GURU" << endl;
    cout << "------------------------------------------------------------" << endl;
    
    for (const auto& it : guru_SMS.relasiGuru) {
        cout << left << setw(20) << it.first  
             << " | " << it.second << endl;    
    }

   cout << "============================================================" << endl;
    cout << "                DAFTAR GURU SPESIALISASI ALAT               " << endl;
    cout << "============================================================" << endl;
    cout << left << setw(40) << "NAMA GURU" << " | " << "SPESIALISASI ALAT" << endl;
    cout << "------------------------------------------------------------" << endl;
    
    for (const auto& it : guru_SMS.spesialisAlat) {
        cout << left << setw(40) << it.first 
             << " | " << it.second << endl;
    }
    
    cout << "============================================================" << endl;
    system("pause");
}

void Tentang_Kami(){
    system("cls");
    cout << "\n=======================================================================\n";
    cout << "                         TENTANG SONATA MUSIC SCHOOL                   ";
    cout << "\n=======================================================================\n";
    cout << "Sonata Music School (SMS) didirikan dengan visi untuk mencetak musisi  \n";
    cout << "berbakat yang tidak hanya mahir secara teknis, tetapi juga memiliki    \n";
    cout << "jiwa seni yang mendalam. Kami menyediakan fasilitas alat musik lengkap \n";
    cout << "dan tenaga pengajar profesional bersertifikasi.\n\n";

    cout << "VISI KAMI:\n";
    cout << ">> Menjadi pusat pendidikan musik terdepan berbasis teknologi & seni.\n\n";

    cout << "MISI KAMI:\n";
    cout << "1. Menyediakan kurikulum musik yang adaptif (Rock, Jazz, Pop, Blues).\n";
    cout << "2. Mengembangkan potensi murid melalui praktik langsung & konser.\n";
    cout << "3. Membangun karakter disiplin dan kreatif melalui musik.\n";
    
    cout << "\n-----------------------------------------------------------------------\n";
    cout << "                           HUBUNGI KAMI                                \n";
    cout << "-----------------------------------------------------------------------\n";
    cout << left << setw(15) << "Alamat" << ": Pesanggrahan No. 88, Jakarta Selatan\n";
    cout << left << setw(15) << "Telepon" << ": (0821) 2265-2172\n";
    cout << left << setw(15) << "Email" << ": wallbreker22 @gmail.com\n";
    cout << left << setw(15) << "Jam Buka" << ": Senin - Jum'at (13.30 - 21.30 WIB)\n";
    cout << "=======================================================================\n";
    system("pause");
}

void Murid_SMS(){
    ifstream file("Data_murid_baru.txt");
    string line;
    
    system("cls");
    cout << "\n======================================================================================================\n";
    cout << "                                     DATA MURID SONATA MUSIC SCHOOL                                   ";
    cout << "\n======================================================================================================\n";
    
    cout << left << setw(4) << "No" 
         << setw(20) << "Nama Murid" 
         << setw(15) << "Kelas Diambil" 
         << setw(35) << "Guru Pengajar" 
         << setw(8) << "Umur" 
         << setw(15) << "Tanggal Lahir" << endl;
    cout << string(102, '-') << endl;

    if (!file.is_open()) {
        cout << "\n   [!] Belum ada data murid yang terdaftar atau file tidak ditemukan.\n";
        cout << "   Silakan lakukan pendaftaran terlebih dahulu pada menu utama.\n\n";
    } else {
        int nomor = 1;
        while (getline(file, line)) {
            stringstream ss(line);
            string segment;
            vector<string> data;

            while (getline(ss, segment, '|')) {
                data.push_back(segment);
            }

            if (data.size() >= 5) {
                cout << left << setw(4) << nomor++ 
                     << setw(20) << data[0].substr(0, 19) 
                     << setw(15) << data[1] 
                     << setw(35) << data[2] 
                     << setw(8) << data[3] 
                     << setw(15) << data[4] << endl;
            }
        }
        file.close();
    }
    
    cout << "======================================================================================================\n";
    cout << "Total Data: " << (file.is_open() ? "Selesai dimuat." : "0") << endl;
    system("pause");
}