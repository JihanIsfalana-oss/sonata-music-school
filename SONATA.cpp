#include <iostream>
#include <string>
#include <iomanip>
#include <fstream>
using namespace std;

class Daftar{
    public:
        string nama;
        string kelas[4] = {"Progressive", "Rock", "Pop", "Blues"};
        string alat[4] = {"Gitar", "Drum", "Bass", "Keyboard/Piano"};
        int umur;
        string lahir;
};

class Guru{
    private:
        long gaji;

    public:
        string nama, kelas, alat;
    
    long setGaji(long n){
        gaji = n;
        n = 5000000;
        return n;
    }
};

void Pendaftaran();

void Riwayat_Guru();

void Tentang_Kami();

int main(){
    int pilih;

    system("cls");
    do{
        cout << "\n=======================================================================\n";
        cout << "                       SONATA MUSIC SCHOOL SYSTEM                          ";
        cout << "\n=======================================================================\n";
        cout << "1. Pendaftaran\n";
        cout << "2. Riwayat Guru\n";
        cout << "3. Tentang Kami\n";
        cout << "4. Keluar Sistem\n";
        cout << "Pilihan anda (1-4) : "; cin >> pilih;

        switch (pilih){
            case 1 : {
                Pendaftaran();
                cin.get();
                break;
            }
            case 2 : {
                Riwayat_Guru();
                cin.get();
                break;
            }
            case 3 : {
                Tentang_Kami();
                cin.get();
                break;
            }
            case 4 : {
                cout << "\nTerima Kasih telah mengunjungi SONATA MUSIC SCHOOL!\n";
                system("pause");
                return 0;
                break;
            }
            default : {
                cout << "\nPilihan anda tidak valid!\n";
                cin.get();
            }    
        }
    }while(pilih != 4);
}

void Pendaftaran(){
    ofstream file ("Data murid baru.txt", ios::app);
    Daftar muridBaru;
    int n,y;

    system("cls");
    cout << "\n       ===== Pilihan Kelas =====       \n";
    for (int i = 0; i < 4; i++){
        cout << i+1 << ". " << muridBaru.kelas[i] << endl;
    }
    cout << "       ===== Pilihan Alat Musik =====       \n";
    for (int i = 0; i < 4; i++){
        cout << i+1 << ". " << muridBaru.alat[i] << endl;
    }
    
    cout << "\nPilih dengan angka sesuai pilihan anda!\n";

    cin.ignore();
    cout << left 
    << setw(20) << "Nama " << " : "; getline (cin, muridBaru.nama);
    cout << left
    << setw(20) << "Kelas " << " : "; cin >> n ; if (n > 4 || n < 1) {cout << "Pilihan tidak valid!\n"; return;}
    cout << left
    << setw(20) << "Alat Musik " << " : "; cin >> y ; if (y > 4 || y < 1) {cout << "Pilihan tidak valid!\n"; return;}
    cout << left
    << setw(20) << "Umur " << " : "; cin >> muridBaru.umur ;
    cin.ignore();
    cout << left
    << setw(20) << "Tanggal Lahir " << " : "; getline (cin, muridBaru.lahir) ;

    file << "\n           ======== Data Murid Baru ========           \n";
    file << left << setw(20) << "Nama : " << muridBaru.nama << "|\n"
         << setw(20) << "Kelas : " << muridBaru.kelas[n] << "|\n"
         << setw(20) << "Alat Musik : " << muridBaru.alat[y] << "|\n"
         << setw(20) << "Umur : " << muridBaru.umur << "|\n"
         << setw(20) << "Tanggal Lahir : " << muridBaru.lahir << endl;

    file.close();
    system("pause");

}

void Riwayat_Guru(){

}

void Tentang_Kami(){

}