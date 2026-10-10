import { cek_auth_token } from '../token/cek_token.js';
import {convTanggalPinjamBuku, convTanggalKembali} from './control.js';
import {hideAlertMember} from './pencarian.js';

function setTanggalISO(){
    const iso_tanggalPinjamBuku = convTanggalPinjamBuku.selectedDates[0];
    const iso_tanggalKembali = convTanggalKembali.selectedDates[0];

    if(iso_tanggalPinjamBuku && iso_tanggalKembali){
        return {
            tanggalPinjam: iso_tanggalPinjamBuku.toISOString(),
            tanggalKembali: iso_tanggalKembali.toISOString(),
        }
    }

    return null;
}

async function prosesPinjamBuku(){

    const tbody = document.getElementById("listPinjamBuku");
    const listBuku = tbody.querySelectorAll("tr[data-id]");
    const member_id = document.getElementById("IDMemberInfo");

    const userAktif = document.getElementById("userAktif");

    const hasilGetListBuku = [];

    const tanggalISO = setTanggalISO();

    listBuku.forEach((data) => {
        const idBuku = parseInt(data.dataset.id);
        const qtyBukuPinjam = data.querySelector(".qty-buku");
        const convQtyBukuPinjam = parseInt(qtyBukuPinjam.value);

        hasilGetListBuku.push({
            buku_id: idBuku,
            qty: convQtyBukuPinjam
        });
    });

    const hasilProsesPinjamBuku = {
        // no_pinjam: no_pinjam,
        member_id: member_id.innerHTML ? parseInt(member_id.innerHTML) : null,
        tanggal_pinjam: tanggalISO.tanggalPinjam,
        tanggal_kembali: tanggalISO.tanggalKembali,
        created_at: new Date(Date.now()).toISOString(),
        created_by: userAktif.innerText,
        details: hasilGetListBuku
    }

    // console.log(JSON.stringify(hasilProsesPinjamBuku));

    try{
        const response = await cek_auth_token("/peminjaman", {
            method: "POST",
            body: JSON.stringify(hasilProsesPinjamBuku)
        });

        if(!response) return;

        if(response.ok){

            const result = await response.json();

            const notifProsesPinjaman = await Swal.fire({
                icon: "success",
                title: "Berhasil",
                text: "Proses Peminjaman Buku berhasil",
                // timer: 1500,
                // showConfirmButton: false
                showCancelButton: true,
                confirmButtonText: '<i class="bi bi-printer"></i> Cetak Struk',
                cancelButtonText: 'Selesai',
                confirmButtonColor: '#198754',
                cancelButtonColor: '#6c757d',
                allowOutsideClick: false            
            });

            if(notifProsesPinjaman.isConfirmed){
                cetakStrukPeminjamanBuku(result.data);
            }

            resetTampilanPeminjaman();

        } else {
            const errorDetail = await response.json();

            console.error(errorDetail);

            Swal.fire({
                icon: "error",
                title: "Gagal",
                text: `${errorDetail.pesan} | Gagal proses peminjaman buku, terjadi error.`
            });
        }


    } catch(error){
        console.error("Error Proses Peminjaman Buku", error)

        Swal.fire({
            icon: "error",
            title: "Gagal",
            text: `TIdak dapat terhubung ke FastAPI endpoint`
        });
    }

}

function cetakStrukPeminjamanBuku(data){
    const printWindow = window.open('', '_blank', 'width: 600, height: 600');

    const htmlData = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Struk Peminjaman - ${data.no_pinjam}</title>
            <style>
                body {
                    font-family: 'Courier New', Courier, monospace;
                    font-size: 12px;
                    width: 300px; /* Lebar kertas */
                    margin: 0 auto;
                    padding: 10px;
                }
                .text-center { text-align: center; }
                .fw-bold { font-weight: bold; }
                .line { border-bottom: 1px dashed #000; margin: 10px 0; }
                table { width: 100%; border-collapse: collapse; }
                th, td { font-size: 11px; text-align: left; padding: 3px 0; }
                .right { text-align: right; }
            </style>
        </head>
        <body>
            <div class="text-center">
                <span class="fw-bold">Manajemen Buku</span><br>
                <div class="line"></div>
            </div>

            <div>
                <span>No. Pinjam : ${data.no_pinjam}</span><br>
                <span>Tanggal Pinjam  : ${new Date(data.tanggal_pinjam).toLocaleDateString("id-ID", {
                    day: "2-digit",
                    month: "long",
                    year: "numeric"
                })}</span><br>
                <span>Tanggal Kembali : ${new Date(data.tanggal_kembali).toLocaleDateString("id-ID", {
                    day: "2-digit",
                    month: "long",
                    year: "numeric"
                })}</span><br>
                <span>Peminjam : ${data.nama_member || '-'}</span><br>
                <span>Petugas  : ${data.created_by}</span>
            </div>

            <div class="line"></div>

            <table>
                <thead>
                    <tr>
                        <th>Buku</th>
                        <th class="right">Qty</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.details.map(item => `
                        <tr>
                            <td>${item.buku ? item.buku.judul : 'Buku ID: ' + item.buku_id}</td>
                            <td class="right">${item.qty}</td>
                        </tr>
                    `).join("")}
                </tbody>
            </table>
            <div class="line"></div>
            
            <div>
                Total buku yang dipinjam : ${
                    data.details.reduce((n, {qty}) => n + qty, 0)
                } <br>
                Dicetak tanggal : ${new Date().toLocaleDateString("id-ID", {
                    day: "2-digit",
                    month: "long",
                    year: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                    second: "2-digit",
                    hour12: false
                    }).replace("pukul", " - ")
                }
            </div>

            <div class="line"></div>

            <div class="text-center" style="margin-top: 15px;">
                <span>Terima Kasih!</span><br>
                <span>Harap kembalikan buku tepat waktu.</span>
            </div>
        </body>
        </html>
    `

    printWindow.document.write(htmlData);
    printWindow.document.close();

    printWindow.focus();

    setTimeout(() => {
        printWindow.print();
    }, 500);
}

function setTransisiBatalBuatDetail(id){
    if(!id) return;

    id.style.opacity = "0";
    id.style.transform = "translateY(-8px)";

    setTimeout(() => {
        id.style.display = "none";
    }, 400);
}

function resetTampilanPeminjaman() {
    try {
        const tbody = document.getElementById("listPinjamBuku");
        if (tbody) {
            tbody.innerHTML = `
                <tr id="RowsKosong">
                    <td colspan="3" class="text-center text-muted py-3">
                        Belum ada buku yang dipilih
                    </td>
                </tr>
            `;

            const totalPinjamBuku = document.getElementById("totalPinjamBuku");

            totalPinjamBuku.textContent = "0 item buku";
        }

        const cariBuku = document.getElementById("cariBuku");
        const cariMember = document.getElementById("cariMember");

        const namaMember = document.getElementById("namaMember");
        const IDMemberInfo = document.getElementById("IDMemberInfo");
        const namaMemberInfo = document.getElementById("namaMemberInfo");
        const alamatMemberInfo = document.getElementById("alamatMemberInfo");
        const notelpMemberInfo = document.getElementById("notelpMemberInfo");
        const statusMemberInfo = document.getElementById("statusMemberInfo");

        if (cariBuku) cariBuku.value = "";
        
        if (namaMember) namaMember.innerText = "";
        if (IDMemberInfo) IDMemberInfo.innerHTML = "";
        if (namaMemberInfo) namaMemberInfo.innerHTML = "";
        if (alamatMemberInfo) alamatMemberInfo.innerHTML = "";
        if (notelpMemberInfo) notelpMemberInfo.innerHTML = "";
        if (statusMemberInfo) statusMemberInfo.innerHTML = "";

        if (cariMember) {
            cariMember.value = "";
            cariMember.removeAttribute("disabled");
            hideAlertMember();
        }

        const batalBtn = document.getElementById("batalBuatPeminjamanBukuId");
        const buatDetailBtn = document.getElementById("buatDetailPeminjamanBukuId");

        const prosesPinjamBukuId = document.getElementById("prosesPinjamBukuId");

        prosesPinjamBukuId.setAttribute("disabled", true);

        if (batalBtn) batalBtn.disabled = true;
        if (buatDetailBtn) buatDetailBtn.disabled = false;

        if (typeof setTransisiBatalBuatDetail === "function") {
            const cariTambahBuku = document.getElementById("cariTambahBuku");
            const daftarBuku = document.getElementById("daftarPeminjaman");
            if (cariTambahBuku) setTransisiBatalBuatDetail(cariTambahBuku);
            if (daftarBuku) setTransisiBatalBuatDetail(daftarBuku);
        }

        if (typeof hideListBuku === "function") hideListBuku();

    } catch (err) {
        console.warn("Peringatan saat reset tampilan:", err);
    }
}

window.prosesPinjamBuku = prosesPinjamBuku;