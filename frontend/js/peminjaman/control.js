import {cek_auth_token} from "../token/cek_token.js";
import {hideListBuku} from "./pencarian.js";

const tanggalPinjamBuku = document.getElementById("tanggalPinjamBuku");
const tanggalKembali = document.getElementById("tanggalKembali");

const convTanggalPinjamBuku = flatpickr(tanggalPinjamBuku, {
    dateFormat: "d-m-Y",
    defaultDate: new Date(),
    clickOpens: false,
    minDate: "today"
});

const convTanggalKembali = flatpickr(tanggalKembali, {
    dateFormat: "d-m-Y",
    defaultDate: new Date(Date.now() + 24 * 60 * 60 * 1000)
});

function perhitunganTotalQtyPinjamBuku(){
    const totalPinjamBuku = document.getElementById("totalPinjamBuku");
    const tbody = document.getElementById("listPinjamBuku");

    if(!tbody || !totalPinjamBuku) return;

    const cek_InputQtyPinjamBuku = tbody.querySelectorAll(".qty-buku");

    let totalQty = 0;

    cek_InputQtyPinjamBuku.forEach(input => {
        totalQty += parseInt(input.value) || 0;
    });

    totalPinjamBuku.textContent = `${totalQty} item buku`;
}

async function getDataBukuByID(data){
    const idBuku = data.dataset.id;
    // console.log("id buku : ", idBuku);

    try{

        const response = await cek_auth_token(`/buku/${idBuku}`);

        if(!response.ok){
            Swal.fire({
                icon: "error",
                title: "Gagal",
                text: `Gagal mengambil data buku id ${idBuku}`,
                timer: 1500,
                showConfirmButton: false
            });

            return;
        }

        const result = await response.json();
        const data_buku = result.data;
        const tbody = document.getElementById("listPinjamBuku");

        const cek_data_buku = tbody.querySelector(`tr[data-id="${idBuku}"]`);

        if(cek_data_buku){
            const btnTambahQtyBuku = cek_data_buku.querySelector(".btn-qty[onclick*='tambahQtyBuku']");
            tambahQtyBuku(btnTambahQtyBuku);

            return;
        }

        const rowsKosong = document.getElementById("RowsKosong");

        if(rowsKosong){
            rowsKosong.remove();
        }

        const hapusListPinjamBukuId = document.getElementById("hapusListPinjamBukuId");
        const prosesPinjamBukuId = document.getElementById("prosesPinjamBukuId");
        
        const htmlRows = document.createElement("tr");

        prosesPinjamBukuId.removeAttribute("disabled");

        htmlRows.setAttribute("data-id", data_buku.id);

        htmlRows.innerHTML = `
            <td>
                <div class="text-dark text-truncate" style="max-width: 180px;">
                    <span class="fs-6 fw-bold" data-judul="${data_buku.judul}">
                        ${data_buku.judul}
                    </span>
                    <span class="ms-2 qty-stok-buku" data-stok="${data_buku.qty}" style="font-size: 14px !important;">
                        (Stok : ${data_buku.qty})
                    </span>
                </div>
            </td>
            <td class="text-center">
                <div class="d-inline-flex align-items-center border rounded px-1">
                    <button class="btn btn-light btn-qty" onclick="kurangQtyBuku(this);"><i class="bi bi-dash"></i></button>
                    <input class="mx-2 fw-bold text-center form-control form-control-sm qty-buku" type="number" min="1" style="width: 50px; pointer-events: none;" readonly value="1"/>
                    <button class="btn btn-light btn-qty" onclick="tambahQtyBuku(this);"><i class="bi bi-plus"></i></button>
                </div>
            </td>
            <td class="text-end">
                <button class="btn btn-sm text-danger" onclick="hapusItemBuku(this);"><i class="bi bi-x-lg"></i></button>
            </td>
        `

        tbody.appendChild(htmlRows);

        perhitunganTotalQtyPinjamBuku();

        hapusListPinjamBukuId.style.display = "block";

        void hapusListPinjamBukuId.offsetHeight;

        hapusListPinjamBukuId.style.opacity = "1";
        hapusListPinjamBukuId.style.transform = "translateY(0)";
        

    } catch(error){
        console.error(error.message);
    }
}

window.getDataBukuByID = getDataBukuByID;


function kurangQtyBuku(btn){

    const tr = btn.closest("tr");

    let qtyBuku = tr.querySelector(".qty-buku");

    let cek_QtyBuku = parseInt(qtyBuku.value) || 1;

    if(cek_QtyBuku > 1){
        qtyBuku.value = parseInt(qtyBuku.value) - 1;

        perhitunganTotalQtyPinjamBuku();
    }
}

window.kurangQtyBuku = kurangQtyBuku;

function tambahQtyBuku(btn){
    const tr = btn.closest("tr");
    
    let qtyBuku = tr.querySelector(".qty-buku");
    let stokBuku = tr.querySelector(".qty-stok-buku");

    let maxStok = parseInt(stokBuku.dataset.stok);

    if(isNaN(maxStok)){
        maxStok = parseInt(stokBuku.textContent.replace("/\D/g", "")) || 0;
    }

    let cek_QtyBuku = parseInt(qtyBuku.value) || 1;

    if(cek_QtyBuku < maxStok){
        qtyBuku.value = cek_QtyBuku + 1;

        perhitunganTotalQtyPinjamBuku();

    } else {
        Swal.fire({
            icon: "warning",
            title: "Stok Terbatas",
            text: `Maksimal total peminjaman buku ini adalah ${maxStok}`,
            timer: 1500,
            showConfirmButton: false
        });
    }
}

window.tambahQtyBuku = tambahQtyBuku;


function hapusItemBuku(btn){
    const tr = btn.closest("tr");
    const tbody = tr.parentElement;

    tr.remove();

    perhitunganTotalQtyPinjamBuku();

    if(tbody.children.length === 0){

        tbody.innerHTML = `
            <tr id="RowsKosong">
                <td colspan="3" class="text-center text-muted py-3">
                    Belum ada buku yang dipilih
                </td>
            </tr>
        `;
    }
}

window.hapusItemBuku = hapusItemBuku;


function hapusListPinjamBuku(btn){
    const tbody = document.getElementById("listPinjamBuku");

    if(tbody){
        // tbody.replaceChildren();

        if(btn){
            btn.style.display = "none";
            btn.style.transform = "translateY(-8px)";
            btn.style.opacity = "0";
        }
        
        tbody.innerHTML = `
            <tr id="RowsKosong">
                <td colspan="3" class="text-center text-muted py-3">
                    Belum ada buku yang dipilih
                </td>
            </tr>
        `;

        perhitunganTotalQtyPinjamBuku();
    }
}

window.hapusListPinjamBuku = hapusListPinjamBuku;


function setTransisiBuatDetail(id){
    id.style.display = "block";

    void id.offsetHeight;

    id.style.opacity = "1";
    id.style.transform = "translateY(0)";

}

function setTransisiBatalBuatDetail(id){
    if(!id) return;

    id.style.opacity = "0";
    id.style.transform = "translateY(-8px)";

    setTimeout(() => {
        id.style.display = "none";
    }, 400);
}

const cariMember = document.getElementById("cariMember"); 

function buatDetailPeminjamanBuku(){

    const batalBuatPeminjamanBukuId = document.getElementById("batalBuatPeminjamanBukuId");
    const buatDetailPeminjamanBukuId = document.getElementById("buatDetailPeminjamanBukuId");

    buatDetailPeminjamanBukuId.disabled = true;
    batalBuatPeminjamanBukuId.disabled = false;

    cariMember.setAttribute("disabled", true);

    const cariTambahBuku = document.getElementById("cariTambahBuku");
    const daftarBuku = document.getElementById("daftarPeminjaman");

    setTransisiBuatDetail(cariTambahBuku);
    setTransisiBuatDetail(daftarBuku);
}

window.buatDetailPeminjamanBuku = buatDetailPeminjamanBuku;

function batalBuatPeminjamanBuku(btn){
    const cariTambahBuku = document.getElementById("cariTambahBuku");
    const daftarBuku = document.getElementById("daftarPeminjaman");

    const batalBuatPeminjamanBukuId = document.getElementById("batalBuatPeminjamanBukuId");
    const buatDetailPeminjamanBukuId = document.getElementById("buatDetailPeminjamanBukuId");

    const cariBuku = document.getElementById("cariBuku");

    batalBuatPeminjamanBukuId.disabled = true;
    buatDetailPeminjamanBukuId.disabled = false;

    setTransisiBatalBuatDetail(cariTambahBuku);
    setTransisiBatalBuatDetail(daftarBuku);

    cariBuku.value = "";

    hideListBuku();

    hapusListPinjamBuku();

    cariMember.removeAttribute("disabled");
}

window.batalBuatPeminjamanBuku = batalBuatPeminjamanBuku;

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

function prosesPinjamBuku(){

    const tbody = document.getElementById("listPinjamBuku");
    const listBuku = tbody.querySelectorAll("tr[data-id]");
    const no_pinjam = document.getElementById("idPeminjamanBuku");
    const qty_pinjam = document.getElementById("totalPinjamBuku");
    const member_id = document.getElementById("IDMemberInfo");

    const userAktif = document.getElementById("userAktif");

    const hasilGetListBuku = [];

    const tanggalISO = setTanggalISO();

    listBuku.forEach((data) => {
        const idBuku = parseInt(data.dataset.id);

        hasilGetListBuku.push({
            buku_id: idBuku
        });
    });

    const hasilProsesPinjamBuku = {
        no_pinjam: no_pinjam,
        member_id: member_id,
        qty_pinjam: qty_pinjam,
        tanggal_pinjam: tanggalISO.tanggalPinjam,
        tanggal_kembali: tanggalISO.tanggalKembali,
        created_at: new Date(Date.now()).toISOString(),
        created_by: userAktif.innerText,
        details: hasilGetListBuku

    }

    console.log(hasilProsesPinjamBuku);

}

window.prosesPinjamBuku = prosesPinjamBuku;