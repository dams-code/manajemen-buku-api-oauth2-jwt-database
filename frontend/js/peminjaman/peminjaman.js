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
            await Swal.fire({
                icon: "success",
                title: "Berhasil",
                text: "Proses Peminjaman Buku berhasil",
                timer: 1500,
                showConfirmButton: false            
            });

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