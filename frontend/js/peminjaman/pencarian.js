
import { cek_auth_token } from "./../token/cek_token.js";

const cariMember = document.getElementById("cariMember");
const dropDownListNamaMember = document.getElementById("dropDownListNamaMember");
const alertHasil = document.getElementById("hasil-cari-nama-member");

let queryPencarianMember;

function showAlertMember(data){
    const namaMember = document.getElementById("namaMember");
    const namaMemberInfo = document.getElementById("namaMemberInfo");
    const alamatMemberInfo = document.getElementById("alamatMemberInfo");
    const notelpMemberInfo = document.getElementById("notelpMemberInfo");
    const statusMemberInfo = document.getElementById("statusMemberInfo");
    
    namaMember.innerText = `${data.id} - ${data.nama}`;

    namaMemberInfo.innerHTML = data.nama;
    alamatMemberInfo.innerHTML = data.alamat;
    notelpMemberInfo.innerHTML = data.no_telp;
    statusMemberInfo.innerHTML = data.status ? "Aktif" : "Tidak Aktif";

    alertHasil.style.display = "grid";
    alertHasil.className="row-gap-2 p-3";

    setTimeout(() => {
        alertHasil.style.opacity = "1";
        alertHasil.style.transform = "translateY(0)";
    }, 10);
}

function hideAlertMember(){
    alertHasil.style.opacity = "0";
    alertHasil.style.transform = "translateY(-8px)";

    setTimeout(() => {
        alertHasil.style.display = "none";
    }, 400);
}

cariMember.addEventListener("input", async function(event){

    const text = event.target.value.trim();

    clearTimeout(this.queryPencarianMember);

    if(!text){
        hideAlertMember();
        dropDownListNamaMember.innerHTML = "";
        return;
    }

    queryPencarianMember = setTimeout(async () => {

        let url = "/member?";

        if(!isNaN(text) && text !== ""){
            url += `id=${encodeURIComponent(text)}`;
        } else {
            url += `nama=${encodeURIComponent(text)}`;
        }

        try{
            const response = await cek_auth_token(url);

            if(!response.ok){
                hideAlertMember();
                dropDownListNamaMember.style.display = "block";
                dropDownListNamaMember.innerHTML = `<div class="list-group-item text-muted">Member tidak ditemukan</div>`;
            }

            const hasil = await response.json();
            const hasil_cari_member = hasil.data;

            dropDownListNamaMember.innerHTML = "";

            // console.log(hasil_cari_member);

            if(!Array.isArray(hasil_cari_member) || hasil_cari_member.length === 0){
                
                dropDownListNamaMember.style.display = "block";
                dropDownListNamaMember.innerHTML = `<div class="list-group-item text-muted" style="background-color: #ff5c5c; color: #fff !important;">Member tidak ditemukan</div>`;

            } else {

                dropDownListNamaMember.style.display = "block";
                
                hasil_cari_member.forEach(member => {
                    if(member.status == true){
                        const li = document.createElement("li");
                        li.className = "list-group-item list-group-item-action cursor-pointer py-2";
                        li.innerText = `ID: ${member.id} ${member.nama}`;

                        li.onclick = function(){
                            // namaMember.innerText = member.nama;
                            showAlertMember(member);
                            cariMember.value = member.nama;
                            dropDownListNamaMember.innerHTML = "";
                            dropDownListNamaMember.style.display = "none";
                        };

                        dropDownListNamaMember.appendChild(li);
                    }
                });                
            }

        } catch(error){
            console.error(error);

            dropDownListNamaMember.style.display = "block";
            dropDownListNamaMember.innerHTML = `<div class="list-group-item text-muted" style="background-color: #ff5c5c; color: #fff !important;">Member tidak ditemukan</div>`;
        }

    }, 200);
});


const cariBuku = document.getElementById("cariBuku");
let queryPencarianBuku;
const listBuku = document.getElementById("listBuku");

function showListBuku(){
    listBuku.innerHTML = "";
    listBuku.style.display = "grid";
    listBuku.className = "container";

    setTimeout(() => {
        listBuku.style.opacity = "1";
        listBuku.style.transform = "translateY(0)";
    }, 200);
}

function hideListBuku(){
    listBuku.innerHTML = "";
    listBuku.style.opacity = "0";
    listBuku.style.transform = "translateY(-8px)";

    setTimeout(() => {
        listBuku.style.display = "none";
        
    }, 300);
}

cariBuku.addEventListener("input", async function(event){

    const text = event.target.value.trim();

    clearTimeout(queryPencarianBuku);

    if(!text){
        hideListBuku();
        listBuku.innerHTML = "";
        return;
    }

    queryPencarianBuku = setTimeout(async ()=>{

        let url = `/buku?`;

        if(!isNaN(text) && text !== ""){
            url += `id=${text}`;
        } else {
            url += `judul=${text}`;
        }

        try{
            const response = await cek_auth_token(url)

            if(!response) return;

            showListBuku();

            if(!response.ok){
                const htmlRowsKosong = `
                    <div class="col">
                        <div class="card h-100 border rounded-3 p-2 d-flex flex-row align-items-center" style="background-color: #ff5c5c;">
                            <p class="text-muted fs-6 m-0" style="color: #fff !important;">Data Buku Tidak Ditemukan</p>
                        </div>
                    </div>
                `

                listBuku.innerHTML = htmlRowsKosong;

                return;
            }

            const result = await response.json();

            const data_buku = result.data;

            if(!data_buku || !Array.isArray(data_buku) || data_buku.length === 0){

                const htmlRowsKosong = `
                    <div class="col">
                        <div class="card h-100 border rounded-3 p-2 d-flex flex-row align-items-center" style="background-color: #ff5c5c; color: #fff !important;">
                            <p class="text-muted fs-6 m-0" style="color: #fff !important;">Data Buku Tidak Ditemukan</p>
                        </div>
                    </div>
                `

                listBuku.innerHTML = htmlRowsKosong;

                return;

            } else {

                const htmlRows = document.createElement("div");

                htmlRows.className = "row row-cols-1 row-cols-md-2 g-3";

                htmlRows.innerHTML = data_buku.map(item => `
                    <div class="col-6">
                        <div class="card h-100 border rounded-3 p-2 d-flex flex-row align-items-center">
                            <div class="bg-light p-3 rounded me-3 text-center text-primary" style="width: 70px;">
                                <i class="bi bi-book fs-3"></i>
                            </div>
                            <div class="flex-grow-1 overflow-hidden">
                                <h6 class="mb-1 text-truncate fw-bold text-dark">${item.judul}</h6>
                                <p class="mb-0 text-muted small"><span style="width:100px;">Penulis</span>: ${item.penulis}</span></p>
                                <p class="mb-0 text-muted small"><span style="width:100px;">Genre</span>: ${item.genre}</span></p>
                                <p class="mb-0 text-muted small"><span style="width:100px;">Stok</span>:<span id="stokBuku" class="badge bg-success p-1 ms-2">${item.qty}</span></p>
                            </div>
                            <button class="btn btn-sm btn-primary rounded-circle ms-2" data-id="${item.id}" title="Tambah ke transaksi peminjaman" onclick="getDataBukuByID(this);">
                                <i class="bi bi-plus-lg"></i>
                            </button>
                        </div>
                    </div>

                `).join("");

                listBuku.appendChild(htmlRows);
            }
        } catch(error){
            console.error("Terjadi error saat load data list buku ", error.message);

            const htmlRowsKosong = `
                <div class="col">
                    <div class="card h-100 border rounded-3 p-2 d-flex flex-row align-items-center" style="background-color: #ff5c5c; color: #fff !important;">
                        <p class="text-muted fs-6 m-0" style="color: #fff !important;">Data Buku Tidak Ditemukan</p>
                    </div>
                </div>
            `

            listBuku.innerHTML = htmlRowsKosong;
        }

    }, 300);

});

async function getDataBukuByID(data){
    const idBuku = data.dataset.id;

    console.log("id buku : ", idBuku);

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

        const htmlRows = document.createElement("tr");

        htmlRows.setAttribute("data-id", data_buku.id);

        htmlRows.innerHTML = `
            <td>
                <div class="text-dark text-truncate" style="max-width: 180px;">
                    <span class="fs-6 fw-bold">
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
                <button class="btn btn-sm text-danger"><i class="bi bi-x-lg" onclick="hapusItemBuku(this);"></i></button>
            </td>
        `

        tbody.appendChild(htmlRows);
        

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